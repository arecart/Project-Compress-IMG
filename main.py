# main.py

import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

# Importer les modules depuis le dossier 'modules'
from modules import crea_bloc, dct2, idct2, quantization, inverse_quantization
from modules import zigzag_order_function, inverse_zigzag_order
from modules import run_length_encode, run_length_decode, compresser, decompresser
from utils import reconstruire_image

def traiter_image_couleur(chemin_entree, chemin_sortie, matrice_quant_Y, matrice_quant_C, qualite=50):
    """
    Compresse et décompresse l'image couleur, puis enregistre l'image compressée.
    
    Paramètres:
        chemin_entree (str): Chemin de l'image d'entrée.
        chemin_sortie (str): Chemin pour enregistrer l'image compressée.
        matrice_quant_Y (numpy.ndarray): Matrice de quantification pour le canal Y.
        matrice_quant_C (numpy.ndarray): Matrice de quantification pour les canaux Cb et Cr.
        qualite (int): Facteur de qualité (1-100).
    """
    # Charger l'image et la convertir en YCbCr
    img = Image.open(chemin_entree).convert("YCbCr")
    img_ycbcr = np.array(img, dtype=np.float32)
    hauteur, largeur, _ = img_ycbcr.shape

    # Séparer les canaux Y, Cb et Cr
    Y = img_ycbcr[:, :, 0]
    Cb = img_ycbcr[:, :, 1]
    Cr = img_ycbcr[:, :, 2]

    # Compresser chaque canal
    blocs_Y = crea_bloc(Y)
    blocs_Cb = crea_bloc(Cb)
    blocs_Cr = crea_bloc(Cr)

    data_compresse_Y = compresser(blocs_Y, matrice_quant_Y)
    data_compresse_Cb = compresser(blocs_Cb, matrice_quant_C)
    data_compresse_Cr = compresser(blocs_Cr, matrice_quant_C)

    # Décompresser chaque canal
    blocs_decomp_Y = decompresser(data_compresse_Y, matrice_quant_Y)
    blocs_decomp_Cb = decompresser(data_compresse_Cb, matrice_quant_C)
    blocs_decomp_Cr = decompresser(data_compresse_Cr, matrice_quant_C)

    # Reconstruire chaque canal
    image_restaurée_Y = reconstruire_image(blocs_decomp_Y, largeur, hauteur)
    image_restaurée_Cb = reconstruire_image(blocs_decomp_Cb, largeur, hauteur)
    image_restaurée_Cr = reconstruire_image(blocs_decomp_Cr, largeur, hauteur)

    # Empiler les canaux restaurés
    img_restaurée_ycbcr = np.stack((image_restaurée_Y, image_restaurée_Cb, image_restaurée_Cr), axis=2)

    # Convertir de YCbCr à RGB
    img_restaurée_rgb = Image.fromarray(img_restaurée_ycbcr.astype(np.uint8), 'YCbCr').convert('RGB')

    # Enregistrer l'image compressée
    img_restaurée_rgb.save(chemin_sortie, "JPEG", quality=qualite)

    messagebox.showinfo("Compression réussie", f"L'image compressée a été enregistrée sous :\n{chemin_sortie}")

def principal():
    root = tk.Tk()
    root.withdraw()

    # Matrice de quantification JPEG standard pour la luminance (Y)
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
    
    # Matrice de quantification pour les chrominances (Cb et Cr)
    MATRICE_QUANT_C = (MATRICE_QUANT_Y * 1.5).astype(int)

    # Demander à l'utilisateur de sélectionner une image
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

    # facteur de qualité
    qualite = 50  # Qualité par défaut
    try:
        qualite_input = simpledialog.askstring("Qualité", "Entrez la qualité (1-100) :", initialvalue="50")
        if qualite_input:
            qualite = int(qualite_input)
            if not (1 <= qualite <= 100):
                raise ValueError
    except:
        messagebox.showwarning("Avertissement", "Facteur de qualité invalide. Utilisation de la qualité par défaut (50).")
        qualite = 50

    # Ajuster la matrice de quantification en fonction de la qualité
    if qualite < 50:
        scale = 5000 / qualite
    else:
        scale = 200 - 2 * qualite
    MATRICE_QUANT_Y_adj = np.floor((MATRICE_QUANT_Y * scale + 50) / 100).astype(int)
    MATRICE_QUANT_Y_adj[MATRICE_QUANT_Y_adj == 0] = 1
    MATRICE_QUANT_C_adj = np.floor((MATRICE_QUANT_C * scale + 50) / 100).astype(int)
    MATRICE_QUANT_C_adj[MATRICE_QUANT_C_adj == 0] = 1

    # Traiter l'image
    traiter_image_couleur(chemin_entree, chemin_sortie, MATRICE_QUANT_Y_adj, MATRICE_QUANT_C_adj, qualite)

if __name__ == "__main__":
    principal()
