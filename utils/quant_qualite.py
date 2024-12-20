# utils/quant_utils.py
import numpy as np

def ajuster_matrice_quantification(MATRICE_QUANT_Y, MATRICE_QUANT_C, qualite):
    """ Ajuster la matrice de quant en fonction de la qualité choisit. """
    if qualite < 50:
        scale = 5000 / qualite
    else:
        scale = 200 - 2 * qualite

    MATRICE_QUANT_Y_adj = np.floor((MATRICE_QUANT_Y * scale + 50) / 100).astype(int)
    MATRICE_QUANT_Y_adj[MATRICE_QUANT_Y_adj == 0] = 1

    MATRICE_QUANT_C_adj = np.floor((MATRICE_QUANT_C * scale + 50) / 100).astype(int)
    MATRICE_QUANT_C_adj[MATRICE_QUANT_C_adj == 0] = 1

    return MATRICE_QUANT_Y_adj, MATRICE_QUANT_C_adj
