#include "image.h"
#include "compression.h"
#include <stdio.h>
#include <stdlib.h>

int main() {
    const char* filename = "image.jpg";
    int* image = NULL;
    int width, height;

    // Charger l'image
    LoadImage(filename, &image, &width, &height);
    if (!image) {
        printf("Erreur : l'image n'a pas pu être chargée.\n");
        return 1;
    }

    printf("Image chargée : %d x %d\n", width, height);

    // Calculer le nombre de blocs
    int numBlocsX = (width + 7) / 8;
    int numBlocsY = (height + 7) / 8;
    int numBlocs = numBlocsX * numBlocsY;

    // Allouer la mémoire pour les blocs
    int(*blocs)[8][8] = malloc(numBlocs * sizeof(int[8][8]));
    if (!blocs) {
        printf("Erreur : mémoire insuffisante pour les blocs.\n");
        free(image);
        return 1;
    }

    // Découper l'image en blocs
    Creabloc(image, width, height, blocs);

    // Compression des blocs
    for (int b = 0; b < numBlocs; b++) {
        double freqBloc[8][8];
        int quantBloc[8][8];
        int vecteur[64];
        int compressed[64];

        DCT2(blocs[b], freqBloc);
        Quantification(freqBloc, quantBloc);
        ZigZag(quantBloc, vecteur);
        int compressedSize = Compress(vecteur, compressed);
        printf("Bloc %d compressé, taille : %d\n", b, compressedSize);
    }
    SaveAsBMP("compressed_image.bmp", image, width, height);
    // Libérer la mémoire
    free(image);
    free(blocs);


    return 0;
}
