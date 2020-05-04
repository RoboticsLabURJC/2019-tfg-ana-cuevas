# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:32:50 2020

@author: anusk
"""

import numpy as np
import cv2
import math

def RGB2HSI(Img):
    
    eps = 0.00000000001
    Ist = Img/255
    Ist = np.float32(Ist)
    print('Ist type')
    print(Ist.dtype)
    I_R,I_G,I_B = cv2.split(Ist)
    
    
    
    R = I_R / 255
    G = I_G / 255
    B = I_B / 255
    print(I_R)
    print(I_R[0][0])
    np.savetxt('dataR.csv', I_R, delimiter=',')
    np.savetxt('dataG.csv', I_G, delimiter=',')
    np.savetxt('dataB.csv', I_B, delimiter=',')
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
    

if __name__ == "__main__":
    
    I = cv2.imread('Board_Recorte.tif')
    I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    
    I_func = RGB2HSI(I)
    np.savetxt('dataS.csv', I_func, delimiter=',')