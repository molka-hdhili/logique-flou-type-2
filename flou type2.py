import numpy as np
import tkinter as tk
from tkinter import Label, Entry, Button
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Fonction pour calculer l'estimation du risque et le niveau de risque
def calcul_risque_et_niveau(tc_value, nc_value, pi_value):
    """
    Calcule l'estimation du risque et détermine le niveau de risque en fonction des entrées.
    
    tc_value : float : Valeur pour la technologie (20-80)
    nc_value : float : Valeur pour les normes (9-70)
    pi_value : float : Valeur pour la portée (5-50)
    
    retourne : tuple : (risque_estime, niveau_risque)
    """
    # 1. Calcul de l'estimation du risque
    risque_estime = (tc_value - 50) * -1 + (nc_value - 40) * -1 + (pi_value - 25) * -1
    # Limiter le risque entre [-80, 70]
    risque_estime = np.clip(risque_estime, -80, 70)

    # 2. Déterminer le niveau de risque en fonction de l'estimation
    if -80 <= risque_estime < -50:
        niveau_risque = "Très fort"
    elif -50 <= risque_estime < -10:
        niveau_risque = "Fort"
    elif -10 <= risque_estime < 40:
        niveau_risque = "Moyen"
    elif 40 <= risque_estime <= 70:
        niveau_risque = "Faible"
    else:
        niveau_risque = "Invalide"

    return risque_estime, niveau_risque

# Tracer les courbes des fonctions d'appartenance floues
def plot_membership_functions(risque_estime):
    # Définition des intervalles des fonctions d'appartenance floues
    rc_range = np.arange(-80, 71, 1)  # Plage pour le niveau de risque

    def trimf(x, a, b, c):
        return np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))

    # Fonctions d'appartenance
    def interval_type2(mf_lower, mf_upper):
        return {"lower": mf_lower, "upper": mf_upper}

    membership_functions = {
        "Très fort": interval_type2(
            trimf(rc_range, -80, -60, -50),  # Bande inférieure ajustée
            trimf(rc_range, -75, -55, -45)   # Bande supérieure ajustée
        ),
        "Fort": interval_type2(
            trimf(rc_range, -50, -30, -10),   # Bande inférieure ajustée
            trimf(rc_range, -45, -25, -5)     # Bande supérieure ajustée
        ),
        "Moyen": interval_type2(
            trimf(rc_range, -10, 10, 30),     # Bande inférieure ajustée
            trimf(rc_range, -5, 15, 35)       # Bande supérieure ajustée
        ),
        "Faible": interval_type2(
            trimf(rc_range, 10, 30, 50),      # Bande inférieure ajustée
            trimf(rc_range, 15, 35, 55)       # Bande supérieure ajustée
        )
    }

    plt.figure(figsize=(12, 6))

    # Tracer les fonctions d'appartenance
    for label, mf in membership_functions.items():
        plt.fill_between(rc_range, mf["lower"], mf["upper"], alpha=0.3, label=f"{label} (Incertitude)")
        plt.plot(rc_range, mf["lower"], '--', label=f"{label} - Bande inférieure")
        plt.plot(rc_range, mf["upper"], '-', label=f"{label} - Bande supérieure")

    # Tracer la ligne pour l'estimation du risque
    plt.axvline(risque_estime, color="red", linestyle="--", label=f"Risque estimé: {risque_estime:.2f}")

    # Configurer le graphique
    plt.title("Fonctions d'appartenance floues")
    plt.xlabel("Valeur de risque")
    plt.ylabel("Degré d'appartenance")
    plt.legend()
    plt.grid(True)
    plt.show()

# Interface graphique avec Tkinter
def interactive_fuzzy_system():
    # Initialisation de la fenêtre Tkinter
    root = tk.Tk()
    root.title("Système de Risque Estimé")
    root.geometry("800x600")

    # Ajouter une image de fond (vous pouvez la supprimer si vous ne l'avez pas)
    try:
        bg_image = Image.open("C:/Users/user/Desktop/capture/Capture.png")  # Assurez-vous que le chemin est correct
        bg_image = bg_image.resize((800, 600))
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
    except:
        pass  # Ignorer l'erreur si l'image de fond n'existe pas

    # Widgets d'entrée pour les trois variables
    Label(root, text="Technologie (20-80):", bg="white").grid(row=0, column=0, padx=10, pady=10)
    tc_entry = Entry(root)
    tc_entry.grid(row=0, column=1)

    Label(root, text="Normes (9-70):", bg="white").grid(row=1, column=0, padx=10, pady=10)
    nc_entry = Entry(root)
    nc_entry.grid(row=1, column=1)

    Label(root, text="Portée (5-50):", bg="white").grid(row=2, column=0, padx=10, pady=10)
    pi_entry = Entry(root)
    pi_entry.grid(row=2, column=1)

    # Labels pour afficher les résultats
    result_label = Label(root, text="Risque estimé: -", bg="white")
    result_label.grid(row=3, column=0, columnspan=2, pady=10)

    risk_label = Label(root, text="Niveau de risque: -", bg="white")
    risk_label.grid(row=4, column=0, columnspan=2, pady=10)

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

            # Calcul du risque et du niveau de risque
            risque_estime, niveau_risque = calcul_risque_et_niveau(tc_value, nc_value, pi_value)

            # Afficher les résultats dans l'interface
            result_label.config(text=f"Risque estimé: {risque_estime:.2f}")
            risk_label.config(text=f"Niveau de risque: {niveau_risque}")

            # Tracer les courbes des fonctions d'appartenance
            plot_membership_functions(risque_estime)

        except ValueError:
            result_label.config(text="Erreur: Entrée invalide")

    # Bouton pour soumettre les valeurs
    Button(root, text="Calculer", command=on_submit).grid(row=5, column=0, columnspan=2, pady=20)

    # Lancer l'interface
    root.mainloop()

# Lancer l'interface utilisateur
interactive_fuzzy_system()
