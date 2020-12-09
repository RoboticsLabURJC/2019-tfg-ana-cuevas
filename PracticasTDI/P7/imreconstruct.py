# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 13:07:28 2020

@author: anusk

imreconstruct
"""

import cv2
import numpy as np
import copy


def imreconstruct(marker, mask):

    EE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9,9))
    print(marker)
    Imrec = copy.deepcopy(marker)
    Imresult =np.zeros(mask.shape)
    i = 0
    
    while (Imrec != Imresult).any():
        
        Imresult = copy.deepcopy(Imrec)
        Imdilated = cv2.dilate(Imresult, EE)
        
        Imrec = np.minimum(Imdilated, mask)
        if i == 200:
            print('no sale del while')
            break
        i += 1
        
    
    return Imresult

if __name__ == "__main__":
    
    I = cv2.imread('I_celulas.bmp', 0)
    Icolor = cv2.imread('Icelulas.bmp', 1)
    EE1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    EE2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    EE3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    
    
    open1 = cv2.morphologyEx(I, cv2.MORPH_OPEN, EE1)
    clos1 = cv2.morphologyEx(open1, cv2.MORPH_CLOSE, EE1)
    open2 = cv2.morphologyEx(clos1, cv2.MORPH_OPEN, EE2)
    clos2 = cv2.morphologyEx(open2, cv2.MORPH_CLOSE, EE2)
    open3 = cv2.morphologyEx(clos2, cv2.MORPH_OPEN, EE3)
    I_ASF3 = cv2.morphologyEx(open3, cv2.MORPH_CLOSE, EE3)
    
    I_neg = 255 - I_ASF3
    
    EEnuevo = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19,19))

    I_marker = cv2.erode(I_neg,EEnuevo,iterations = 1)
    I_rec = imreconstruct(I_marker, I_neg)
    
    cv2.imshow('recontruct', I_rec)
    cv2.waitKey(0)
    cv2.destroyWindow('recontruct')  