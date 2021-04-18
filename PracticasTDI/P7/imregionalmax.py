# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:08:28 2021

@author: anusk
"""

import numpy as np
import cv2
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
import matplotlib.pyplot as plt

def correctregions(img, markers):
    
    frameH, frameW = markers.shape
    
    for i in range(0, frameH):
        for j in range(0,frameW):
            if markers[i,j] != 0:
                for m in range(-1,2):
                    for n in range(-1,2):
                        if 0<i+m<frameH:
                            if 0<j+n<frameW:
                                if markers[i+m,j+n] != markers[i,j]:
                            
                                    if img[i,j]==img[i+m,j+n]:
                                        markers[i+m,j+n] = markers[i,j]
                        
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
    ret, markers = cv2.connectedComponents(binary)
    
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
    
            
    plt.figure('Segmented image')
    plt.imshow(markers2, cmap=plt.cm.get_cmap('nipy_spectral'))

if __name__ == "__main__":
    
    img = cv2.imread('prueba_min.png',0)
    #I_neg = 255-img
    imregionalmax(img)
    