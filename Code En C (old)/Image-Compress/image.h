#ifndef IMAGE_H
#define IMAGE_H

void LoadImage(const char* filename, int** image, int* width, int* height);
void Creabloc(int* image, int width, int height, int blocs[][8][8]);
void SaveAsBMP(const char* filename, int* image, int width, int height);

#endif
