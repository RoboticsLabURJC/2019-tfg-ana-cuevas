# -*- coding: utf-8 -*-
"""
RGB2HSI: funcion para cambiar espacio de color

parámetros:
    In: Imagen en RGB rango 0-255
    Out: Imagen HSI rango 0-1
                          
"""
import numpy as np
import cv2
import math

def RGB2HSI(Img):
    
    eps = 0.00000000001
    Ist = Img/255
    print(Ist.dtype)
    I_R,I_G,I_B = cv2.split(Ist)
    
    
    
    R = I_R / 255
    G = I_G / 255
    B = I_B / 255
    
    h, w = R.shape

    #H
    dividendo = ((R-G)+(R-B))/2
    
    divisor = np.sqrt((R-G)*(R-G) + (R-B)*(G-B)) + eps
    
    theta = np.arccos(dividendo/divisor)
    H = theta
    
    for i in range(0, h):
        for j in range(0, w): 
            if B[i,j] > G[i,j]:
                H[i,j] = 2*math.pi - theta[i,j]

    H = H/(2*math.pi)

    #I
    I = (R+G+B)/3
    
    #S
    S = 1- (3*np.minimum(R, G, B))/(R+G+B+ eps)
    
    I_HSI = cv2.merge((H,S,I))
    
    return I_HSI
    