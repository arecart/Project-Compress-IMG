# modules/image_processing.py

import numpy as np
from PIL import Image
from .block import crea_bloc
from .compression import compresser, decompresser
from utils.reconstruire_image import reconstruire_image

def traiter_image_couleur(chemin_entree, chemin_sortie, matrice_quant_Y, matrice_quant_C, qualite=50):
    """
    Compresse et décompresse l'image couleur, puis enregistre l'image compressée.
    
    Paramètres:
        chemin_entree (str): Chemin de l'image d'entrée.
        chemin_sortie (str): Chemin pour enregistrer l'image compressée.
        matrice_quant_Y (numpy.ndarray): Matrice de quantification pour le canal Y.
        matrice_quant_C (numpy.ndarray): Matrice de quantification pour les canaux Cb et Cr.
        qualite (int): Qualité (1-100).
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
