# modules/compression.py
import numpy as np  
from .dct_module import dct2, idct2
from .quantization import quantization, inverse_quantization
from .zigzag import zigzag_order_function, inverse_zigzag_order
from .block import crea_bloc

def run_length_encode(vector):
    """
    Encode les coefficients avec le codage par longueur d'exécution (RLE).
    
    Paramètres:
        vector (list): Vecteur 1x64 en ordre zig-zag.
        
    Retour:
        list: Vecteur encodé avec RLE.
    """
    encoding = []
    zeros = 0
    for coef in vector:
        if coef == 0:
            zeros += 1
        else:
            if zeros > 0:
                encoding.append((0, zeros))
                zeros = 0
            encoding.append(coef)
    if zeros > 0:
        encoding.append((0, zeros))
    return encoding

def run_length_decode(encoded_vector):
    """
    Décode le vecteur encodé avec RLE.
    
    Paramètres:
        encoded_vector (list): Vecteur encodé avec RLE.
        
    Retour:
        list: Vecteur décodé avec 64 coefficients.
    """
    decoded = []
    for item in encoded_vector:
        if isinstance(item, tuple) and item[0] == 0:
            decoded.extend([0] * item[1])
        else:
            decoded.append(item)
    # S'assurer que le vecteur a exactement 64 coefficients
    if len(decoded) < 64:
        decoded.extend([0] * (64 - len(decoded)))
    return decoded[:64]

def compresser(blocs, matrice_quant):
    """
    Compresse les blocs d'image.
    
    Paramètres:
        blocs (list): Liste de blocs 8x8.
        matrice_quant (numpy.ndarray): Matrice de quantification 8x8.
        
    Retour:
        list: Données compressées.
    """
    data_compresse = []
    for bloc in blocs:
        bloc_dct = dct2(bloc - 128)  # Décalage de niveau
        bloc_quant = quantization(bloc_dct, matrice_quant)
        zigzag = zigzag_order_function(bloc_quant)
        rle = run_length_encode(zigzag)
        data_compresse.append(rle)
    return data_compresse

def decompresser(data_compresse, matrice_quant):
    """
    Décompresse les données compressées en blocs d'image.
    
    Paramètres:
        data_compresse (list): Données compressées.
        matrice_quant (numpy.ndarray): Matrice de quantification 8x8.
        
    Retour:
        list: Liste de blocs décompressés 8x8.
    """
    blocs_decomp = []
    for rle in data_compresse:
        zigzag = run_length_decode(rle)
        bloc_quant = inverse_zigzag_order(zigzag)
        bloc_idct = idct2(inverse_quantization(bloc_quant, matrice_quant)) + 128  # Inversion du décalage
        bloc_idct = np.clip(bloc_idct, 0, 255).astype(int)
        blocs_decomp.append(bloc_idct)
    return blocs_decomp
