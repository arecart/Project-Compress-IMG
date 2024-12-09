# modules/__init__.py

from .block import crea_bloc
from .dct_module import dct2, idct2
from .quantization import quantization, inverse_quantization
from .zigzag import zigzag_order_function, inverse_zigzag_order
from .compression import run_length_encode, run_length_decode, compresser, decompresser
