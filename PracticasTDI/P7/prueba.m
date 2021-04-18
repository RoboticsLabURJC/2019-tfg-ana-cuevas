clear all, close all, clc;
I=imread('prueba_min.png');
I_gray=rgb2gray(I);
I_neg=imcomplement(I_gray);
imshow(I_gray)

I_max = imregionalmax(I_gray);
figure(2);imshow(I_max)