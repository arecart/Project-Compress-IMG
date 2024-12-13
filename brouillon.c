#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image.h"
#include "stb_image_write.h"

#define BLOCK_SIZE 8

// Matrice de quantification standard
int quant_matrix[BLOCK_SIZE][BLOCK_SIZE] = { 
    {16, 11, 10, 16, 24, 40, 51, 61},
    {12, 12, 14, 19, 26, 58, 60, 55},
    {14, 13, 16, 24, 40, 57, 69, 56},
    {14, 17, 22, 29, 51, 87, 80, 62},
    {18, 22, 37, 56, 68, 109, 103, 77},
    {24, 35, 55, 64, 81, 104, 113, 92},
    {49, 64, 78, 87, 103, 121, 120, 101},
    {72, 92, 95, 98, 112, 100, 103, 99}
};

// Transformation Discrète en Cosinus 2D (DCT2)
void DCT2(int bloc[BLOCK_SIZE][BLOCK_SIZE], float bloc_freq[BLOCK_SIZE][BLOCK_SIZE]) {
    float alpha, beta, sum;
    for (int u = 0; u < BLOCK_SIZE; u++) {
        for (int v = 0; v < BLOCK_SIZE; v++) {
            sum = 0.0;
            for (int x = 0; x < BLOCK_SIZE; x++) {
                for (int y = 0; y < BLOCK_SIZE; y++) {
                    sum += bloc[x][y] * 
                           cos(((2 * x + 1) * u * M_PI) / (2.0 * BLOCK_SIZE)) * 
                           cos(((2 * y + 1) * v * M_PI) / (2.0 * BLOCK_SIZE));
                }
            }
            alpha = (u == 0) ? sqrt(1.0 / BLOCK_SIZE) : sqrt(2.0 / BLOCK_SIZE);
            beta = (v == 0) ? sqrt(1.0 / BLOCK_SIZE) : sqrt(2.0 / BLOCK_SIZE);
            bloc_freq[u][v] = alpha * beta * sum;
        }
    }
}

// Quantification
void quantification(float bloc_freq[BLOCK_SIZE][BLOCK_SIZE], int bloc_quant[BLOCK_SIZE][BLOCK_SIZE]) {
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            bloc_quant[i][j] = round(bloc_freq[i][j] / quant_matrix[i][j]);
        }
    }
}

// Compression par blocs
void process_image(int width, int height, unsigned char *input, unsigned char *output) {
    int num_blocks_x = width / BLOCK_SIZE;
    int num_blocks_y = height / BLOCK_SIZE;

    for (int by = 0; by < num_blocks_y; by++) {
        for (int bx = 0; bx < num_blocks_x; bx++) {
            int bloc[BLOCK_SIZE][BLOCK_SIZE];
            float bloc_freq[BLOCK_SIZE][BLOCK_SIZE];
            int bloc_quant[BLOCK_SIZE][BLOCK_SIZE];

            // Extraction d'un bloc
            for (int i = 0; i < BLOCK_SIZE; i++) {
                for (int j = 0; j < BLOCK_SIZE; j++) {
                    int x = bx * BLOCK_SIZE + j;
                    int y = by * BLOCK_SIZE + i;
                    bloc[i][j] = input[y * width + x];
                }
            }

            // Appliquer DCT et quantification
            DCT2(bloc, bloc_freq);
            quantification(bloc_freq, bloc_quant);

            // Sauvegarde du bloc compressé dans l'image de sortie
            for (int i = 0; i < BLOCK_SIZE; i++) {
                for (int j = 0; j < BLOCK_SIZE; j++) {
                    int x = bx * BLOCK_SIZE + j;
                    int y = by * BLOCK_SIZE + i;
                    output[y * width + x] = bloc_quant[i][j];
                }
            }
        }
    }
}

int main() {
    // Charger l'image d'entrée
    int width, height, channels;
    unsigned char *input_image = stbi_load("input_image.png", &width, &height, &channels, 1); // Charge en niveaux de gris
    if (!input_image) {
        fprintf(stderr, "Erreur: Impossible de charger l'image\n");
        return 1;
    }

    // Vérifier que l'image est divisible par BLOCK_SIZE
    if (width % BLOCK_SIZE != 0 || height % BLOCK_SIZE != 0) {
        fprintf(stderr, "Erreur: Les dimensions de l'image doivent être divisibles par %d\n", BLOCK_SIZE);
        stbi_image_free(input_image);
        return 1;
    }

    // Préparer l'image de sortie
    unsigned char *output_image = malloc(width * height);
    if (!output_image) {
        fprintf(stderr, "Erreur: Allocation mémoire échouée\n");
        stbi_image_free(input_image);
        return 1;
    }

    // Traiter l'image
    process_image(width, height, input_image, output_image);

    // Sauvegarder l'image compressée
    if (!stbi_write_png("output_image.png", width, height, 1, output_image, width)) {
        fprintf(stderr, "Erreur: Impossible de sauvegarder l'image\n");
        free(output_image);
        stbi_image_free(input_image);
        return 1;
    }

    printf("Traitement terminé. L'image compressée est sauvegardée dans 'output_image.png'.\n");

    // Libération des ressources
    free(output_image);
    stbi_image_free(input_image);

    return 0;
}
