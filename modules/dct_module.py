# modules/dct_module.py

import numpy as np
from scipy.fft import dct, idct

def dct2(bloc):
    """
    Applique la Transformée en Cosinus Discrète 2D au bloc.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc 8x8 de l'image.
        
    Retour:
        numpy.ndarray: Bloc 8x8 transformé.
    """
    return dct(dct(bloc.T, norm='ortho').T, norm='ortho')

def idct2(bloc):
    """
    Applique la Transformée en Cosinus Discrète Inverse 2D au bloc.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc 8x8 transformé.
        
    Retour:
        numpy.ndarray: Bloc 8x8 reconstruit.
    """
    return idct(idct(bloc.T, norm='ortho').T, norm='ortho')
