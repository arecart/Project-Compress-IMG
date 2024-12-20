#ifndef COMPRESSION_H
#define COMPRESSION_H

void DCT2(int bloc[8][8], double freqBloc[8][8]);
void Quantification(double freqBloc[8][8], int quantBloc[8][8]);
void ZigZag(int quantBloc[8][8], int vecteur[64]);
int Compress(int vecteur[64], int compressed[64]);

#endif
