clear all, close all, clc;
I=imread('minimos.png');
I_gray=rgb2gray(I);
I_neg=imcomplement(I_gray);
imshow(I_neg)

I_max = imregionalmax(I_neg);
figure(2);imshow(I_max)