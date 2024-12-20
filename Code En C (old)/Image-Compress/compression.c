#include "compression.h"
#include <math.h>
#include <stdio.h>

#define BLOCK_SIZE 8

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

int quantMatrix[BLOCK_SIZE][BLOCK_SIZE] = {
    {16, 11, 10, 16, 24, 40, 51, 61},
    {12, 12, 14, 19, 26, 58, 60, 55},
    {14, 13, 16, 24, 40, 57, 69, 56},
    {14, 17, 22, 29, 51, 87, 80, 62},
    {18, 22, 37, 56, 68, 109, 103, 77},
    {24, 35, 55, 64, 81, 104, 113, 92},
    {49, 64, 78, 87, 103, 121, 120, 101},
    {72, 92, 95, 98, 112, 100, 103, 99}
};

void DCT2(int bloc[BLOCK_SIZE][BLOCK_SIZE], double freqBloc[BLOCK_SIZE][BLOCK_SIZE]) {
    for (int u = 0; u < BLOCK_SIZE; u++) {
        for (int v = 0; v < BLOCK_SIZE; v++) {
            double sum = 0.0;
            for (int x = 0; x < BLOCK_SIZE; x++) {
                for (int y = 0; y < BLOCK_SIZE; y++) {
                    sum += bloc[x][y] *
                        cos(((2 * x + 1) * u * M_PI) / (2 * BLOCK_SIZE)) *
                        cos(((2 * y + 1) * v * M_PI) / (2 * BLOCK_SIZE));
                }
            }
            double cu = (u == 0) ? sqrt(1.0 / BLOCK_SIZE) : sqrt(2.0 / BLOCK_SIZE);
            double cv = (v == 0) ? sqrt(1.0 / BLOCK_SIZE) : sqrt(2.0 / BLOCK_SIZE);
            freqBloc[u][v] = cu * cv * sum;
        }
    }
}

void Quantification(double freqBloc[BLOCK_SIZE][BLOCK_SIZE], int quantBloc[BLOCK_SIZE][BLOCK_SIZE]) {
    for (int i = 0; i < BLOCK_SIZE; i++) {
        for (int j = 0; j < BLOCK_SIZE; j++) {
            quantBloc[i][j] = (int)round(freqBloc[i][j] / quantMatrix[i][j]);
        }
    }
}

void ZigZag(int quantBloc[BLOCK_SIZE][BLOCK_SIZE], int vecteur[BLOCK_SIZE * BLOCK_SIZE]) {
    int index = 0;
    int i = 0, j = 0;
    int direction = 1;
    while (index < BLOCK_SIZE * BLOCK_SIZE) {
        vecteur[index++] = quantBloc[i][j];
        if (direction == 1) {
            if (j == BLOCK_SIZE - 1) {
                i++;
                direction = -1;
            }
            else if (i == 0) {
                j++;
                direction = -1;
            }
            else {
                i--;
                j++;
            }
        }
        else {
            if (i == BLOCK_SIZE - 1) {
                j++;
                direction = 1;
            }
            else if (j == 0) {
                i++;
                direction = 1;
            }
            else {
                i++;
                j--;
            }
        }
    }
}

int Compress(int vecteur[BLOCK_SIZE * BLOCK_SIZE], int compressed[BLOCK_SIZE * BLOCK_SIZE]) {
    int writeIndex = 0, zeroCount = 0;
    for (int i = 0; i < BLOCK_SIZE * BLOCK_SIZE; i++) {
        if (vecteur[i] == 0) {
            zeroCount++;
        }
        else {
            if (zeroCount > 0) {
                compressed[writeIndex++] = 0;
                compressed[writeIndex++] = zeroCount;
                zeroCount = 0;
            }
            compressed[writeIndex++] = vecteur[i];
        }
    }
    if (zeroCount > 0) {
        compressed[writeIndex++] = 0;
        compressed[writeIndex++] = zeroCount;
    }
    return writeIndex;
}
