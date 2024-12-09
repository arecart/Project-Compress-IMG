# modules/quantization.py

import numpy as np

def quantization(bloc, matrice_quant):
    """
    Quantifie les coefficients DCT avec la matrice de quantification.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc 8x8 en domaine fréquentiel.
        matrice_quant (numpy.ndarray): Matrice de quantification 8x8.
        
    Retour:
        numpy.ndarray: Bloc quantifié 8x8.
    """
    return np.round(bloc / matrice_quant).astype(int)

def inverse_quantization(bloc, matrice_quant):
    """
    Effectue la quantification inverse des coefficients DCT.
    
    Paramètres:
        bloc (numpy.ndarray): Bloc quantifié 8x8.
        matrice_quant (numpy.ndarray): Matrice de quantification 8x8.
        
    Retour:
        numpy.ndarray: Bloc déquantifié 8x8.
    """
    return (bloc * matrice_quant).astype(float)
