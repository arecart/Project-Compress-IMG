# Projet de Compression d'Images

## Table des Matières
- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Lib-Utilisées](#Lib-Utilisées)
- [Installation](#installation)
- [Structure](#Structure)
- [Fichiers](#Fichiers)
- [Fonctions-Principales](#Fonctions-Principales)

## Introduction

Bienvenue dans notre **Projet de Compression d'Images** ! Ce projet implémente un algorithme de compression d'image simple . Il utilise la Transformation en Cosinus Discrète (DCT2), la quantification, la lecture en zig-zag et RLE.


## Fonctionnalités

- **Compression en Couleur** : Supporte les images en couleur en utilisant YCbCr.
- **Ajustement de la Qualité** : Permet de choisir le niveau de compression (1-100).


## Lib Utilisées

- **Python 3.x**
- **NumPy**
- **Pillow (PIL)**
- **SciPy**
- **Tkinter**

## Installation

1. **Cloner le Répertoire**

   ```bash
   git clone https://github.com/skylostt/Project-Compress-IMG.git
   cd projet-compression-image

2. **Installer les Dépendances**
    ```bash
    pip install -r requirements.txt

3. **Optionnel**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows : venv\Scripts\activate

4. **Installation lib**
    ```bash
    pip install -r requirements.txt

5. **Lancement**
    ```bash
    python(3) main.py

## Structure

- Project-Compress-IMG/
- │
- ├── main.py
- ├── modules/
- │   ├── __init__.py
- │   ├── block.py
- │   ├── compression.py
- │   ├── dct_module.py
- │   ├── quantization.py
- │   └── zigzag.py
- ├── utils/
- │   ├── __init__.py
- │   ├── quant_qualite.py
- │   └── reconstruire_image.py
- ├── requirements.txt
- └── README.md

## Fichiers

- **main.py** : Fichier principal.
- **modules/** : Contient les modules pour chaque étape de la compression.
- **block.py** : Divise l'image en blocs de 8x8.
- **dct_module.py** : Applique la DCT et son inverse.
- **quantization.py** : Gère la quantification des coefficients DCT.
- **zigzag.py** : Réorganise les coefficients en ordre zig-zag.
- **compression.py** : Gère le codage et décodage RLE.
- **utils/** : Contient les fonctions pour ajuster la matrice de quant en fonction de la qualité et reconstruire l'image.
- **requirements.txt** : Liste des dépendances Python.
- **README.md** : Vous êtes ici :).

## Fonctions Principales

- **crea_bloc (modules/block.py)**
    ```bash
    Description : Divise image en blocs de 8x8 pixels.
    Entrée : Image sous forme de tableau NumPy.
    Sortie : Liste de blocs 8x8.

- **dct2 et idct2 (modules/dct_module.py)**
    ```bash
    Description : Applique la Transformation en Cosinus Discrète et son inverse.
    Entrée : Bloc 8x8.
    Sortie : Bloc transformé ou reconstruit.

- **quantization et inverse_quantization (modules/quantization.py)**
    ```bash
    Description : Quantifie et déquantifie les coefficients DCT.
    Entrée : Bloc DCT et matrice de quantification.
    Sortie : Bloc quantifié ou déquantifié.

- **zigzag_order_function et inverse_zigzag_order (modules/zigzag.py)**
    ```bash
    Description : Réorganise les coefficients en ordre zig-zag et inverse.
    Entrée : Bloc 8x8 ou vecteur 1x64.
    Sortie : Vecteur zig-zag ou bloc reconstruit.

- **compresser et decompresser (modules/compression.py)**
    ```bash
    Description : Compresse et décompresse les blocs en utilisant RLE.
    Entrée : Blocs et matrice de quantification ou données compressées.
    Sortie : Données compressées ou blocs décompressés.

- **reconstruire_image (utils/reconstruire_image.py)**
    ```bash
    Description : Reconstitue image à partir des blocs décompressés.
    Entrée : Liste de blocs, largeur et hauteur de image.
    Sortie : Image reconstruite sous forme de tableau NumPy.