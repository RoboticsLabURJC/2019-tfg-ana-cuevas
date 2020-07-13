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

    EE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    print(marker)
    Imrec = copy.deepcopy(marker)
    Imresult =np.zeros(mask.shape)
    i = 0
    
    while Imrec.any() != Imresult.any():
        print(Imresult)
        print('entra en el while')
        Imresult = copy.deepcopy(Imrec)
        Imdilated = cv2.dilate(Imresult, EE)
        Imrec = np.minimum(Imdilated, mask)
        if i == 40:
            break
        i += 1
        
    
    return Imresult

if __name__ == "__main__":
    
    I = cv2.imread('apples.jpg', 0)
    #I = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
    EE = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20,20))
    Ie = cv2.erode(I,EE)
    I_rec = imreconstruct(Ie, I)
    
    cv2.imshow('recontruct', I_rec)
    cv2.waitKey(0)
    cv2.destroyWindow('recontruct')  