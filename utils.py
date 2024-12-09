# utils.py

import numpy as np

def reconstruire_image(blocs, largeur, hauteur, block_size=8):
    """
    Reconstruit l'image à partir des blocs.
    
    Paramètres:
        blocs (list): Liste de blocs décompressés.
        largeur (int): Largeur de l'image originale.
        hauteur (int): Hauteur de l'image originale.
        block_size (int): Taille du bloc (par défaut 8).
        
    Retour:
        numpy.ndarray: Image reconstruite.
    """
    image = np.zeros((hauteur, largeur), dtype=np.uint8)
    index = 0
    for i in range(0, hauteur, block_size):
        for j in range(0, largeur, block_size):
            image[i:i + block_size, j:j + block_size] = blocs[index]
            index += 1
    return image
