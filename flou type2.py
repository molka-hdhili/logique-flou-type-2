import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button
from PIL import Image, ImageTk

# Univers de discours
rc_range = np.arange(-80, 71, 1)  # Intervalle pour le niveau de risque

# Définir les fonctions d'appartenance floues ajustées
def create_type2_membership_functions():
    def trimf(x, a, b, c):
        return np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

    def interval_type2(mf_lower, mf_upper):
        return {"lower": mf_lower, "upper": mf_upper}

    # Plages ajustées pour les fonctions d'appartenance floues
    rc_mf = {
        "Très faible": interval_type2(
            trimf(rc_range, -80, -70, -60),  # Bande inférieure
            trimf(rc_range, -75, -65, -55)  # Bande supérieure
        ),
        "Faible": interval_type2(
            trimf(rc_range, -10, 10, 40),    # Faible couvrant entre -10 et 40
            trimf(rc_range, 0, 20, 40)      # Faible ajusté pour une couverture plus large
        ),
        "Moyen": interval_type2(
            trimf(rc_range, 10, 40, 70),    # Moyen couvrant entre 10 et 70
            trimf(rc_range, 15, 45, 75)     # Moyen avec une légère extension vers 75
        ),
        "Fort": interval_type2(
            trimf(rc_range, 10, 40, 70),
            trimf(rc_range, 15, 45, 75)
        ),
        "Très fort": interval_type2(
            trimf(rc_range, 20, 50, 70),
            trimf(rc_range, 25, 55, 75)
        )
    }
    return rc_mf

# Initialiser les fonctions d'appartenance
membership_functions = create_type2_membership_functions()

# Calcul des degrés d'appartenance
def calculate_type2_membership(value, interval):
    lower_degree = np.interp(value, rc_range, interval["lower"])
    upper_degree = np.interp(value, rc_range, interval["upper"])
    return lower_degree, upper_degree

# Interface utilisateur
def interactive_fuzzy_system_type2():
    root = Tk()
    root.title("Système Flou Type 2")
    root.geometry("800x600")

    # Ajouter un fond à l'interface
    bg_image = Image.open("C:/Users/user/Desktop/capture/Capture.png")  # Assurez-vous que le chemin est correct
    bg_image = bg_image.resize((800, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Ajouter des widgets
    Label(root, text="Technologie (20-80):", bg="white").grid(row=0, column=0, padx=10, pady=10)
    tc_entry = Entry(root)
    tc_entry.grid(row=0, column=1)

    Label(root, text="Normes (9-70):", bg="white").grid(row=1, column=0, padx=10, pady=10)
    nc_entry = Entry(root)
    nc_entry.grid(row=1, column=1)

    Label(root, text="Portée (5-50):", bg="white").grid(row=2, column=0, padx=10, pady=10)
    pi_entry = Entry(root)
    pi_entry.grid(row=2, column=1)

    result_label = Label(root, text="Risque estimé: -", bg="white")
    result_label.grid(row=3, column=0, columnspan=2, pady=10)

    risk_label = Label(root, text="Niveau de risque: -", bg="white")
    risk_label.grid(row=4, column=0, columnspan=2, pady=10)

    def plot_membership_type2(risk_value):
        plt.figure(figsize=(12, 6))

        for label, mf in membership_functions.items():
            plt.fill_between(rc_range, mf["lower"], mf["upper"], alpha=0.3, label=f"{label} (Incertitude)")
            plt.plot(rc_range, mf["lower"], '--', label=f"{label} - Bande inférieure")
            plt.plot(rc_range, mf["upper"], '-', label=f"{label} - Bande supérieure")

        plt.axvline(risk_value, color="red", linestyle="--", label=f"Risque: {risk_value:.2f}")
        plt.title("Fonctions d'appartenance - Type 2")
        plt.xlabel("Valeur de risque")
        plt.ylabel("Degré d'appartenance")
        plt.legend()
        plt.grid()
        plt.show()

    def on_submit():
        try:
            # Lire les entrées
            tc_value = float(tc_entry.get())
            nc_value = float(nc_entry.get())
            pi_value = float(pi_entry.get())

            # Vérification des limites
            if not (20 <= tc_value <= 80):
                result_label.config(text="Erreur: Technologie hors limites")
                return
            if not (9 <= nc_value <= 70):
                result_label.config(text="Erreur: Normes hors limites")
                return
            if not (5 <= pi_value <= 50):
                result_label.config(text="Erreur: Portée hors limites")
                return

            # Calcul du risque ajusté
            risk_value = (tc_value + nc_value + pi_value) / 3

            # Calcul des degrés d'appartenance flous de type 2
            memberships = {
                label: calculate_type2_membership(risk_value, mf)
                for label, mf in membership_functions.items()
            }

            # Identifier le niveau de risque dominant
            dominant_label = max(memberships, key=lambda label: memberships[label][1])
            lower, upper = memberships[dominant_label]

            # Afficher les résultats
            result_label.config(text=f"Risque estimé: {risk_value:.2f}")
            risk_label.config(text=f"Niveau de risque: {dominant_label}\n"
                                   f"Incertitude: [{lower:.2f}, {upper:.2f}]")

            # Tracer les courbes de type 2
            plot_membership_type2(risk_value)

        except ValueError:
            result_label.config(text="Erreur: Entrée invalide")

    Button(root, text="Calculer", command=on_submit).grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()

# Lancer l'interface utilisateur
interactive_fuzzy_system_type2()
