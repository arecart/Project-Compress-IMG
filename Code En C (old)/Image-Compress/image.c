#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#include "image.h"
#include <stdlib.h>
#include <stdio.h>

#define BLOCK_SIZE 8


void SaveAsBMP(const char* filename, int* image, int width, int height) {
    FILE* file = fopen(filename, "wb");
    if (!file) {
        printf("Erreur : impossible de créer le fichier %s\n", filename);
        exit(1);
    }

    int paddedWidth = (width + 3) & ~3; 
    int fileSize = 14 + 40 + paddedWidth * height * 3;

    unsigned char bmpHeader[14] = {
        'B', 'M',                           
        fileSize & 0xFF, fileSize >> 8 & 0xFF, fileSize >> 16 & 0xFF, fileSize >> 24 & 0xFF,
        0, 0,                              
        0, 0,                              
        54, 0, 0, 0                        
    };

    unsigned char dibHeader[40] = {
        40, 0, 0, 0,                        
        width & 0xFF, width >> 8 & 0xFF, width >> 16 & 0xFF, width >> 24 & 0xFF,  
        height & 0xFF, height >> 8 & 0xFF, height >> 16 & 0xFF, height >> 24 & 0xFF, 
        1, 0,                               
        24, 0,                             
        0, 0, 0, 0,                         
        0, 0, 0, 0,                        
        0, 0, 0, 0,                         
        0, 0, 0, 0,                        
        0, 0, 0, 0,                         
        0, 0, 0, 0                         
    };

    fwrite(bmpHeader, 1, 14, file);
    fwrite(dibHeader, 1, 40, file);

    unsigned char* row = (unsigned char*)malloc(paddedWidth * 3);
    if (!row) {
        printf("Erreur : mémoire insuffisante pour l'allocation de la ligne.\n");
        fclose(file);
        exit(1);
    }

    for (int i = height - 1; i >= 0; i--) {
        for (int j = 0; j < width; j++) {
            int pixel = image[i * width + j];
            row[j * 3 + 0] = (unsigned char)(pixel);      
            row[j * 3 + 1] = (unsigned char)(pixel);      
            row[j * 3 + 2] = (unsigned char)(pixel);      
        }
        for (int j = width * 3; j < paddedWidth * 3; j++) {
            row[j] = 0; 
        }
        fwrite(row, 1, paddedWidth * 3, file);
    }

    free(row);
    fclose(file);
    printf("Image compressée enregistrée sous %s\n", filename);
}

void LoadImage(const char* filename, int** image, int* width, int* height) {
    int channels;
    unsigned char* data = stbi_load(filename, width, height, &channels, 1);
    if (!data) {
        *image = NULL;
        return;
    }

    *image = (int*)malloc((*width) * (*height) * sizeof(int));
    if (!*image) {
        printf("Erreur : mémoire insuffisante pour l'image.\n");
        stbi_image_free(data);
        return;
    }

    for (int i = 0; i < (*width) * (*height); i++) {
        (*image)[i] = (int)data[i];
    }
    stbi_image_free(data);
}

void Creabloc(int* image, int width, int height, int blocs[][8][8]) {
    int blocIndex = 0;
    for (int i = 0; i < height; i += BLOCK_SIZE) {
        for (int j = 0; j < width; j += BLOCK_SIZE) {
            for (int x = 0; x < BLOCK_SIZE; x++) {
                for (int y = 0; y < BLOCK_SIZE; y++) {
                    blocs[blocIndex][x][y] = (i + x < height && j + y < width) ? image[(i + x) * width + (j + y)] : 0;
                }
            }
            blocIndex++;
        }
    }
}
