# modules/quantification.py

import numpy as np

def quantification(bloc, matrice_quant):
    """
    Quantifie les coeff avec la matrice de quant.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc 8x8 fréquentiel.
        matrice_quant (numpy.ndarray): Matrice de quant 8x8.
        
    Retour:
        numpy.ndarray: Bloc quantifié 8x8.
    """
    return np.round(bloc / matrice_quant).astype(int)

def inverse_quantification(bloc, matrice_quant):
    """
    Effectue la quantification inverse des coeff.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc quantifié 8x8.
        matrice_quant (numpy.ndarray): Matrice de quant 8x8.
        
    Retour:
        numpy.ndarray: Bloc déquantifié 8x8.
    """
    return (bloc * matrice_quant).astype(float)
