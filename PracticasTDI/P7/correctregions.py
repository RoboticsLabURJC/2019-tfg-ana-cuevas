# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:25:52 2021

@author: anusk
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max

def correctregions(img, markers):
    
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

if __name__ == "__main__":
    
    img = cv2.imread('prueba_min.png',0)
    img = 255-img
    frameH, frameW = img.shape
    conn = np.ones((3,3))
    imgfilter =  cv2.medianBlur(img, 11)
    binary = peak_local_max(imgfilter, footprint=conn, indices=False, exclude_border=0)
    binary = np.uint8(binary)*255
    ret, markers = cv2.connectedComponents(binary)
    
    newmarkers = correctregions(img, markers)
    border = findborder(newmarkers)
    new = np.zeros([frameH,frameW,3], np.uint8)
    
    for x in range(0, len(border)):
        a=border[x][0]
        b=border[x][1]
        new[a,b] = [255,0,0]
        
    plt.figure('border')
    plt.imshow(new)
    
    plt.figure('image')
    plt.imshow(img, cmap='gray')
    
    plt.figure('filter')
    plt.imshow(imgfilter, cmap='gray')
    
    plt.figure('markers')
    plt.imshow(markers, cmap=plt.cm.get_cmap('nipy_spectral'))
    plt.figure('new markers')
    plt.imshow(new)
    plt.imshow(newmarkers, cmap=plt.cm.get_cmap('nipy_spectral'))
    