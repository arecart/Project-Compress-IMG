# main.py

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import numpy as np

from modules.image_couleur import traiter_image_couleur
from utils.quant_qualite import ajuster_matrice_quantification

def principal():
    root = tk.Tk()
    root.withdraw()

    # Matrice de quant JPEG basique pour Y
    MATRICE_QUANT_Y = np.array([
        [16,11,10,16,24,40,51,61],
        [12,12,14,19,26,58,60,55],
        [14,13,16,24,40,57,69,56],
        [14,17,22,29,51,87,80,62],
        [18,22,37,56,68,109,103,77],
        [24,35,55,64,81,104,113,92],
        [49,64,78,87,103,121,120,101],
        [72,92,95,98,112,100,103,99]
    ])

    # Matrice de quant pour les chrominances (Cb et Cr)
    MATRICE_QUANT_C = (MATRICE_QUANT_Y * 1.5).astype(int)

    # simple demande de choix d'image on limite à du jpeg et png
    chemin_entree = filedialog.askopenfilename(
        title="Sélectionnez une image à compresser",
        filetypes=[("Fichiers images", "*.jpg *.jpeg *.png")]
    )
    if not chemin_entree:
        messagebox.showwarning("Avertissement", "Aucune image sélectionnée.")
        return

    # Définir le chemin de sortie
    nom_base = os.path.splitext(os.path.basename(chemin_entree))[0]
    dossier_sortie = os.path.dirname(chemin_entree)
    chemin_sortie = os.path.join(dossier_sortie, f"{nom_base}_compress.jpg")

    # qualité
    qualite = 50
    try:
        qualite_input = simpledialog.askstring("Qualité", "Entrez la qualité (1-100) :", initialvalue="50")
        if qualite_input:
            qualite = int(qualite_input)
            if not (1 <= qualite <= 100):
                raise ValueError
    except:
        messagebox.showwarning("Qualité choisit impossible.")
        qualite = 50

    # Ajuster la matrice de quant en fonction de la qualité choisit
    MATRICE_QUANT_Y_adj, MATRICE_QUANT_C_adj = ajuster_matrice_quantification(MATRICE_QUANT_Y, MATRICE_QUANT_C, qualite)

    traiter_image_couleur(chemin_entree, chemin_sortie, MATRICE_QUANT_Y_adj, MATRICE_QUANT_C_adj, qualite)

    messagebox.showinfo("Compression réussie", f"L'image compressée a été enregistrée sous :\n{chemin_sortie}")


if __name__ == "__main__":
    principal()
