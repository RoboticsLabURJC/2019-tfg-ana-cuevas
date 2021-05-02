# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 20:26:05 2021

@author: anusk
"""

import numpy as np
import cv2
from skimage.morphology import reconstruction
import matplotlib.pyplot as plt

def imregionalmax(img):
    
    marker = np.int32(img) -1
    I_rec = reconstruction(marker, img)
    img = np.int32(img)
    I_rec = np.int32(I_rec)
    resta = img - I_rec
    maximos = np.zeros(resta.shape)
    maximos[resta != 0] = 255
    
    return maximos

if __name__ == "__main__":
    
    
    
    img = cv2.imread('I_rec.png',0)
    
    maximos = imregionalmax(img)
    
    plt.figure('Segmented image')
    plt.imshow(maximos, cmap='gray')