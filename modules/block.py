# modules/block.py

import numpy as np

def crea_bloc(image, block_size=8):
    """
    Divise l'image en blocs de taille block_size x block_size.
    
    Paramètres:
        image (numpy.ndarray): Image en niveaux de gris ou canal unique.
        block_size (int): Taille du bloc (par défaut 8).
        
    Retour:
        list: Liste de blocs découpés.
    """
    h, w = image.shape
    blocs = []
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            bloc = image[i:i + block_size, j:j + block_size]
            # Compléter le bloc avec des zéros si nécessaire
            if bloc.shape[0] != block_size or bloc.shape[1] != block_size:
                bloc = np.pad(bloc, ((0, block_size - bloc.shape[0]), 
                                      (0, block_size - bloc.shape[1])), 'constant')
            blocs.append(bloc)
    return blocs
