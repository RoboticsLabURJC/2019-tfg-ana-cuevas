%
%   Práctica 7
%
%% 1. Preprocesado
clear all, close all, clc;
I=imread('cells.jpg');
I_gray=rgb2gray(I);

EE_C1=strel('disk',2);
EE_C2=strel('disk',4);
EE_C3=strel('disk',6);

OPN1=imopen(I_gray,EE_C1);
CLO1=imclose(OPN1,EE_C1);
OPN2=imopen(CLO1,EE_C2);
CLO2=imclose(OPN2,EE_C2);
OPN3=imopen(CLO2,EE_C3);
I_ASF3=imclose(OPN3,EE_C3);

% Plots I
figure
subplot(3,2,1), imshow(OPN1), title('Apertura r=1');
subplot(3,2,2), imshow(CLO1), title('Cierre r=1');
subplot(3,2,3), imshow(OPN2), title('Apertura r=2');
subplot(3,2,4), imshow(CLO2), title('Cierre r=2');
subplot(3,2,5), imshow(OPN3), title('Apertura r=3');
subplot(3,2,6), imshow(I_ASF3), title('Cierre r=3(I-ASF3)');

%% 2. Segmentación por watershed
% a. Obtención de los marcadores de célula
I_neg=imcomplement(I_ASF3);
I_marker=imerode(I_neg,strel('disk',21));
I_rec=imreconstruct(I_marker,I_neg);
I_max_reg=imregionalmax(I_rec);
I_max_reg2=imclearborder(I_max_reg);
% Umbralizamos las celulas cuya intensidad media sea >= 150
I_max_reg3=I_max_reg2;
cc=bwlabel(I_max_reg2);
n_objetos=max(cc(:));
stats=regionprops(cc,I_rec,'MeanIntensity');
for nob=1:n_objetos
    if stats(nob).MeanIntensity <= 75
        [r,c] = find(cc == nob);
        I_max_reg3(r,c)=0;
    end
end % for nob

% b. Obtención del marcador externo
I_dilate=imdilate(logical(I_max_reg3),strel('disk',7));
D=bwdist(I_dilate);
DL=watershed(D);
bgm=(DL==0); 

% c. Combinar los marcadores internos y los externos
I_minimos=bgm | I_max_reg3;

% d. Obtener el módulo del gradiente de la imagen original
h=fspecial('sobel');
I_celulas_grad=imfilter(double(I_gray),h);

% e. Imponer como únicos mínimos regionales las regiones de primer plano de I_minimos
I_celulas_grad_mrk=imimposemin(I_celulas_grad,I_minimos);

% f. Watershed de nuevo
DL2=watershed(I_celulas_grad_mrk);
L_frontera=(DL2==0);

% Plots II
% a.
figure
subplot(3,2,1), imshow(I_neg), title('Negativo de I-ASF3');
subplot(3,2,2), imshow(I_marker), title('Erosión de I-Neg(I-marker)');
subplot(3,2,3), imshow(I_rec), title('Reconstrucción de I-Neg(con I-marker)');
subplot(3,2,4), imshow(I_max_reg), title('Máximos regionales de I-rec');
subplot(3,2,5), imshow(I_max_reg2), title('Máximos regionales, primer procesado');
subplot(3,2,6), imshow(I_max_reg3), title('Máximos regionales, segundo procesado');

% b.
figure
subplot(2,2,1), mesh(I_dilate), colormap(gray), title('I-Dilate');
subplot(2,2,2), mesh(D), colormap(gray), title('D (bwdist)');
subplot(2,2,3), mesh(double(DL)), colormap(gray), title('DL (watershed)');
subplot(2,2,4), mesh(bgm), colormap(gray), title('bgm (fonteras watershed)');
figure
imshow(imadd(255*uint8(bgm),I_gray)), title('Imagen original con fronteras de watershed');

% c.
figure
imshow(I_minimos), title('Marcadores internos y externos');

% d.
figure
subplot(1,2,1), imshow(I_celulas_grad), title('Módulo del gradiente de la Imagen original');

% e.
subplot(1,2,2), imshow(I_celulas_grad_mrk), title('Imponemos nuevos mínimos regionales');

% f. y g. Superponer watershed a la imagen original
figure
imshow(imadd(255*uint8(L_frontera),I_gray)), title('Imagen original con fronteras del segundo watershed');