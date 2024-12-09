# modules/zigzag.py

import numpy as np

# Ordre Zig-Zag pour un bloc 8x8
ZIGZAG_ORDER = [
     0,  1,  5,  6, 14, 15, 27, 28,
     2,  4,  7, 13, 16, 26, 29, 42,
     3,  8, 12, 17, 25, 30, 41, 43,
     9, 11, 18, 24, 31, 40, 44, 53,
    10, 19, 23, 32, 39, 45, 52, 54,
    20, 22, 33, 38, 46, 51, 55, 60,
    21, 34, 37, 47, 50, 56, 59, 61,
    35, 36, 48, 49, 57, 58, 62, 63
]

def zigzag_order_function(bloc):
    """
    Réorganise les coefficients du bloc en ordre zig-zag.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc 8x8 quantifié.
        
    Retour:
        list: Vecteur 1x64 en ordre zig-zag.
    """
    return [bloc.flatten()[i] for i in ZIGZAG_ORDER]

def inverse_zigzag_order(vector):
    """
    Reconstruit le bloc 8x8 à partir des coefficients en ordre zig-zag.
    
    Paramètres:
        vector (list): Vecteur 1x64 en ordre zig-zag.
        
    Retour:
        numpy.ndarray: Bloc 8x8 reconstruit.
    """
    bloc = np.zeros(64, dtype=int)
    for i, val in enumerate(vector):
        if i < len(ZIGZAG_ORDER):
            bloc[ZIGZAG_ORDER[i]] = val
    return bloc.reshape((8, 8))
