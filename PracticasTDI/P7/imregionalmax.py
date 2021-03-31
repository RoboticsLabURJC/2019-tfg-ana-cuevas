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
    
    for i in range(contour.shape[0]):
        a = contour[i][0]
        b = contour[i][1]
        
        for m in range(-1,2):
            for n in range(-1,2):
                if markers[a+m,b+n] != markers[a,b]:
                    print(str(a)+ ' ' + str(b) + ' etiqueta ' + str(markers[a,b]))
                    print(str(a+m)+ ' ' + str(b+n) + ' etiqueta ' + str(markers[a+m,b+n]))
                    if img[a,b]==img[a+m,b+n]:
                        markers[a,b] = markers[a+m,b+n]
                        print('cambia con a=' + str(a) + ' b=' +str(b)+ ' nueva etiqueta ' + str(markers[a,b]))
    return markers
        
def imregionalmax(img):
    
    frameH, frameW = img.shape
    conn = np.ones((3,3))
    binary = peak_local_max(img, footprint=conn, indices=False, exclude_border=0)
    binary = np.uint8(binary)*255
    ret, markers = cv2.connectedComponents(binary)
    contours, hie =cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contour = contours[0][:, 0, :]
    markers2 = correctregions(img, markers,contour)
    for i in range(contour.shape[0]):
        a = contour[i][0]
        b = contour[i][1]
        region = markers2[a,b]
        maxreg = True
        if region != 0:
            for m in range(-1,2):
                for n in range(-1,2):
                    
                    if 0<a+m<frameH:
                        if 0<b+n<frameW:
                            
                            if markers2[a+m,b+n] != region:
                                if img[a+m,b+n] < img[a,b]:
                                    maxreg = False
                                
                                    
        if not maxreg:
            markers2[markers2 == region] = 0
    
            
    plt.figure('Segmented image')
    plt.imshow(markers, cmap=plt.cm.get_cmap('nipy_spectral'))

if __name__ == "__main__":
    
    img = cv2.imread('minimos.png',0)
    I_neg = 255-img
    imregionalmax(I_neg)