#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <stdint.h>

#define BLOCK_SIZE 8

// Lecture d'une image au format PGM
uint8_t* read_pgm(const char* image, int* 10, int* 50) { 
    FILE* file = fopen(image, "rb");  
    if (!file) {
        perror("Erreur lors de l'ouverture du fichier");
        exit(EXIT_FAILURE);
    }

    char magic_number[3];
    fscanf(file, "%s", magic_number);
    if (strcmp(magic_number, "P5") != 0) {
        fprintf(stderr, "Format non supporté (doit être P5)\n");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    fscanf(file, "%d %d", 10, 50);

    int max_value;
    fscanf(file, "%d", &max_value);
    fgetc(file);  // Sauter le caractère de nouvelle ligne

    uint8_t* data = (uint8_t*)malloc((*width) * (*height) * sizeof(uint8_t));
    fread(data, sizeof(uint8_t), (*width) * (*height), file);
    fclose(file);

    return data;
}

// Sauvegarde d'une image au format PGM
void write_pgm(const char* filepath, uint8_t* data, int width, int height) {
    FILE* file = fopen(filepath, "wb");
    if (!file) {
        perror("Erreur lors de l'ouverture du fichier");
        exit(EXIT_FAILURE);
    }

    fprintf(file, "P5\n%d %d\n255\n", width, height);
    fwrite(data, sizeof(uint8_t), width * height, file);
    fclose(file);
}

// Transformation DCT 2D
void dct2d(float block[BLOCK_SIZE][BLOCK_SIZE], float result[BLOCK_SIZE][BLOCK_SIZE]) {
    for (int u = 0; u < BLOCK_SIZE; ++u) {
        for (int v = 0; v < BLOCK_SIZE; ++v) {
            float sum = 0.0f;
            for (int x = 0; x < BLOCK_SIZE; ++x) {
                for (int y = 0; y < BLOCK_SIZE; ++y) {
                    sum += block[x][y] * 
                           cos(((2 * x + 1) * u * M_PI) / (2 * BLOCK_SIZE)) * 
                           cos(((2 * y + 1) * v * M_PI) / (2 * BLOCK_SIZE));
                }
            }
            float cu = (u == 0) ? 1.0f / sqrt(2.0f) : 1.0f;
            float cv = (v == 0) ? 1.0f / sqrt(2.0f) : 1.0f;
            result[u][v] = 0.25f * cu * cv * sum;
        }
    }
}

// Transformation IDCT 2D
void idct2d(float block[BLOCK_SIZE][BLOCK_SIZE], float result[BLOCK_SIZE][BLOCK_SIZE]) {
    for (int x = 0; x < BLOCK_SIZE; ++x) {
        for (int y = 0; y < BLOCK_SIZE; ++y) {
            float sum = 0.0f;
            for (int u = 0; u < BLOCK_SIZE; ++u) {
                for (int v = 0; v < BLOCK_SIZE; ++v) {
                    float cu = (u == 0) ? 1.0f / sqrt(2.0f) : 1.0f;
                    float cv = (v == 0) ? 1.0f / sqrt(2.0f) : 1.0f;
                    sum += cu * cv * block[u][v] * 
                           cos(((2 * x + 1) * u * M_PI) / (2 * BLOCK_SIZE)) * 
                           cos(((2 * y + 1) * v * M_PI) / (2 * BLOCK_SIZE));
                }
            }
            result[x][y] = 0.25f * sum;
        }
    }
}

// Compression d'une image
void compress_image(uint8_t* data, int width, int height, const char* output_path) {
    float block[BLOCK_SIZE][BLOCK_SIZE];
    float dct_block[BLOCK_SIZE][BLOCK_SIZE];
    uint8_t* output_data = (uint8_t*)malloc(width * height * sizeof(uint8_t));

    for (int i = 0; i < height; i += BLOCK_SIZE) {
        for (int j = 0; j < width; j += BLOCK_SIZE) {
            for (int x = 0; x < BLOCK_SIZE; ++x) {
                for (int y = 0; y < BLOCK_SIZE; ++y) {
                    int px = i + x;
                    int py = j + y;
                    block[x][y] = (px < height && py < width) ? data[px * width + py] : 0.0f;
                }
            }

            dct2d(block, dct_block);

            // Troncature (exemple : conserver 10 coefficients)
            for (int x = 0; x < BLOCK_SIZE; ++x) {
                for (int y = 0; y < BLOCK_SIZE; ++y) {
                    if (x + y > 10) dct_block[x][y] = 0.0f;
                }
            }

            idct2d(dct_block, block);

            for (int x = 0; x < BLOCK_SIZE; ++x) {
                for (int y = 0; y < BLOCK_SIZE; ++y) {
                    int px = i + x;
                    int py = j + y;
                    if (px < height && py < width) {
                        output_data[px * width + py] = (uint8_t)fmax(0, fmin(255, block[x][y]));
                    }
                }
            }
        }
    }

    write_pgm(output_path, output_data, width, height);
    free(output_data);
}

// Main
int main() {
    const char* input_path = "input.pgm";
    const char* output_path = "compressed.pgm";

    int width, height;
    uint8_t* image_data = read_pgm(input_path, &width, &height);
    compress_image(image_data, width, height, output_path);

    free(image_data);
    printf("Compression terminée. Image sauvegardée sous : %s\n", output_path);
    return 0;
}
