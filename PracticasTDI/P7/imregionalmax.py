# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 18:12:54 2021

@author: anusk
"""

import numpy as np
import cv2
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import matplotlib.pyplot as plt
import time

def correctregions(img, markers):
    
    frameH, frameW = markers.shape
    border = findborder(markers)
    for i in range(len(border)):
        a = border[i][0]
        b = border[i][1]
        if markers[a,b] != 0:
            for m in range(-1,2):
                for n in range(-1,2):
                    if 0<a+m<frameH:
                        if 0<b+n<frameW:
                            if markers[a+m,b+n] != markers[a,b]:
                        
                                if img[a,b]==img[a+m,b+n]:
                                    markers[a+m,b+n] = markers[a,b]
                        
    return markers


def findborder(markers):
    
    frameH, frameW = markers.shape
    borders = []
    for i in range(0, frameH):
        for j in range(0,frameW):
            isborder = False
            if markers[i,j] != 0:
                
                for m in range(-1,2):
                    for n in range(-1,2):
                    
                        if 0<i+m<frameH:
                            if 0<j+n<frameW:
                                if markers[i+m,j+n] != markers[i,j]:
                                    isborder = True
                
                if isborder:
                    borders.append([i,j])
    return borders

def imregionalmax(img):
    
    frameH, frameW = img.shape
    conn = np.ones((3,3))
    binary = peak_local_max(img, footprint=conn, indices=False, exclude_border=0)
    binary = np.uint8(binary)*255
    ret, markers = cv2.connectedComponents(binary, connectivity=8)
    
    markers2 = correctregions(img, markers)
    border = findborder(markers2)
    
    for i in range(len(border)):
        a = border[i][0]
        b = border[i][1]
        region = markers2[a,b]
        maxreg = True
        if region != 0:
            for m in range(-1,2):
                for n in range(-1,2):
                    
                    if 0<a+m<frameH:
                        if 0<b+n<frameW:
                            
                            if markers2[a+m,b+n] != region:
                                if img[a+m,b+n] > img[a,b]:
                                    maxreg = False
                                
                                    
        if not maxreg:
            markers2[markers2 == region] = 0
            
    fin = markers2.astype(np.uint8)
    fin[fin!=0] =255
    return fin

if __name__ == "__main__":
    start_time = time.time()
    img = cv2.imread('prueba_min.png',0)
    I_neg = 255-img
    I_maxreg = imregionalmax(I_neg)
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.figure('Segmented image')
    plt.imshow(I_maxreg, cmap='gray')