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


# Fonction d'appartenance pour les différentes catégories de risque
def trimf(x, a, b, c):
    """ Fonction de type triangle pour calculer le degré d'appartenance """
    return np.maximum(0, np.minimum((x - a) / (b - a), (c - x) / (c - b)))


# Tracer la courbe de risque et afficher uniquement le risque estimé
def plot_membership_functions(risque_estime, deg_appartenance):
    # Plage des valeurs pour le niveau de risque
    rc_range = np.arange(-80, 71, 1)

    # Fonctions d'appartenance pour chaque niveau de risque
    def interval_type2(mf_lower, mf_upper):
        return {"lower": mf_lower, "upper": mf_upper}

    # Définition des fonctions d'appartenance pour chaque niveau de risque
    membership_functions = {
        "Très fort": interval_type2(
            trimf(rc_range, -80, -60, -50),
            trimf(rc_range, -75, -55, -45)
        ),
        "Fort": interval_type2(
            trimf(rc_range, -50, -30, -10),
            trimf(rc_range, -45, -25, -5)
        ),
        "Moyen": interval_type2(
            trimf(rc_range, -10, 10, 30),
            trimf(rc_range, -5, 15, 35)
        ),
        "Faible": interval_type2(
            trimf(rc_range, 10, 30, 50),
            trimf(rc_range, 15, 35, 55)
        )
    }

    # Tracer la courbe de risque et les fonctions d'appartenance
    plt.figure(figsize=(12, 6))
    for label, mf in membership_functions.items():
        plt.fill_between(rc_range, mf["lower"], mf["upper"], alpha=0.3, label=f"{label} (Incertitude)")
        plt.plot(rc_range, mf["lower"], '--', label=f"{label} - Bande inférieure")
        plt.plot(rc_range, mf["upper"], '-', label=f"{label} - Bande supérieure")

    # Tracer la ligne du risque estimé (ligne continue noire)
    plt.plot([risque_estime, risque_estime], [0, deg_appartenance["Très fort"]], color="black", linewidth=2,
             label=f"Risque estimé: {risque_estime:.2f}")

    # Calculer la projection du risque estimé sur l'axe des ordonnées
    projection_value = deg_appartenance["Très fort"]  # Initialiser la projection
    for label, mf in membership_functions.items():
        if mf["lower"][np.where(rc_range == risque_estime)[0][0]] > 0:
            projection_value = mf["lower"][np.where(rc_range == risque_estime)[0][0]]
            break

    # Tracer la ligne perpendiculaire (projection) du risque estimé (trait continu noir)
    plt.plot([risque_estime, risque_estime], [0, projection_value], color="black", linewidth=2, linestyle='-',
             label=f"Projection du risque: {projection_value:.2f}")

    # Ajouter le texte pour le degré d'appartenance sur l'axe des ordonnées
    plt.text(risque_estime, projection_value + 0.05, f"{projection_value:.2f}", color="black", ha="center", fontsize=12,
             fontweight='bold')

    # Configurer le graphique
    plt.title("Fonctions d'appartenance du Risque")
    plt.xlabel("Valeur du risque")
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

            # Calcul des degrés d'appartenance
            deg_appartenance = {
                "Très fort": trimf(np.array([risque_estime]), -80, -60, -50)[0],
                "Fort": trimf(np.array([risque_estime]), -50, -30, -10)[0],
                "Moyen": trimf(np.array([risque_estime]), -10, 10, 30)[0],
                "Faible": trimf(np.array([risque_estime]), 10, 30, 50)[0],
            }

            # Tracer les courbes des fonctions d'appartenance
            plot_membership_functions(risque_estime, deg_appartenance)

        except ValueError:
            result_label.config(text="Erreur: Entrée invalide")

    # Bouton pour soumettre les valeurs
    Button(root, text="Calculer", command=on_submit).grid(row=6, column=0, columnspan=2, pady=20)

    # Lancer l'interface
    root.mainloop()


# Lancer l'interface utilisateur
interactive_fuzzy_system()
