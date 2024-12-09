# Projet de Compression d'Images

## Table des Matières
- [Introduction](#introduction)
- [Fonctionnalités](#fonctionnalités)
- [Lib-Utilisées](#Lib-Utilisées)
- [Installation](#installation)
- [Lancement](#Lancement)
- [Structure](#Structure)
- [Fichiers](#Fichiers)
- [Fonctions-Principales](#Fonctions-Principales)

## Introduction

Bienvenue dans le **Projet de Compression d'Images** ! Ce projet implémente un algorithme de compression d'image simple inspiré du standard JPEG. Il utilise la Transformation en Cosinus Discrète (DCT), la quantification, l'ordre zig-zag et le codage par longueur d'exécution (RLE) pour compresser et décompresser les images.


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

## Installer les Dépendances


- **pip install -r requirements.txt**

## Optionnel 

- Vous pouvez aussi le faire sous un environnement virtuel avec : 

- **python -m venv venv**
- **source venv/bin/activate  # Sur Windows : venv\Scripts\activate**

- puis : 

- **pip install -r requirements.txt**

## Lancement 

- **python(3) main.py**

## Structure

- image_compression/
- │
- ├── main.py
- ├── modules/
- │   ├── __init__.py
- │   ├── block.py
- │   ├── compression.py
- │   ├── dct_module.py
- │   ├── quantization.py
- │   └── zigzag.py
- ├── utils.py
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
- **utils.py** : Fonctions utilitaires pour reconstruire l'image.
- **requirements.txt** : Liste des dépendances Python.
- **README.md** : Vous êtes ici :).

## Fonctions Principales

- **crea_bloc (modules/block.py)**
- Description : Divise l'image en blocs de 8x8 pixels.
- Entrée : Image sous forme de tableau NumPy.
- Sortie : Liste de blocs 8x8.

- **dct2 et idct2 (modules/dct_module.py)**
- Description : Applique la Transformation en Cosinus Discrète et son inverse.
- Entrée : Bloc 8x8.
- Sortie : Bloc transformé ou reconstruit.

- **quantization et inverse_quantization (modules/quantization.py)**
- Description : Quantifie et déquantifie les coefficients DCT.
- Entrée : Bloc DCT et matrice de quantification.
- Sortie : Bloc quantifié ou déquantifié.

- **zigzag_order_function et inverse_zigzag_order (modules/zigzag.py)**
- Description : Réorganise les coefficients en ordre zig-zag et inverse.
- Entrée : Bloc 8x8 ou vecteur 1x64.
- Sortie : Vecteur zig-zag ou bloc reconstruit.

- **compresser et decompresser (modules/compression.py)**
- Description : Compresse et décompresse les blocs en utilisant RLE.
- Entrée : Blocs et matrice de quantification ou données compressées.
- Sortie : Données compressées ou blocs décompressés.

- **reconstruire_image (utils.py)**
- Description : Reconstitue l'image à partir des blocs décompressés.
- Entrée : Liste de blocs, largeur et hauteur de l'image.
- Sortie : Image reconstruite sous forme de tableau NumPy.