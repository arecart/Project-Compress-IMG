image 512 x 512
1)
Création de blocs de 8x8

2)
DCT 2 (Transformation en cos: Discret Cosinus Transform 2)

3)
Quantification 

4)
Lecture en Zizag

5)

Compression (on regroupe les zeros attention bien vérifier qu'on regroupe une suite de zero on zero isoler il faut soit mettre une vérification qui l'ignore soit le remplace ar 0,1 par exemple (float))

6)
Decompression (faire l'inverse reconsitition des blocs)

7)
Quantification inverse (perte de donnée obligatoire)

8)
Reconstition de l'image


Limite potentielle

Nota bene pour la couleur 

Matrice Y 8x8 ycb et ycr 4x4


Faire un petit rapport bien décrire toute les kfonction avec :
paramètre entrée = ex: image
paramètre sortie = ex: 4096 bloc

Decoupe l'image en 4096 blocs de 8X8 




Fonction nom obligatoire:

Crea bloc

DCT2
paramètre entrée = bloc 8x8 int = bloc image
paramètre sortie = bloc 8x8 int = bloc freq

Quantification
param entrée =  bloc 8x8(fréquentiel)
				bloc quantification (8x8)

ZiZag
param entrée = bloc 8x8
param sortie = Vecteur(1x64)

                                                        MAIN
																

Compress
param entrée = vecteur 1x64
param sortie = vecteur

[Tab.bloc] = Creabloc image
Pour i=1 à Taille.Tab-bloc
BlocImage = Tab-bloc(i)
Blocfreq = DCT2 (BlocImage)
BlocfreqQuant = Quantification (Blocfreq)
Vectfreq = ZigZag (BlocfreqQuant)
Vectfind = Vectfinal + compress (Vertfeq)


Pour i = 1 à 64 step 8
pour j 1 à 64 step 8
l= i 
Cal = j
ChargeBloc = (i,j)
