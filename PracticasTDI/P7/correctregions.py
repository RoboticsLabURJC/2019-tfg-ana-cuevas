# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:25:52 2021

@author: anusk
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

def correctregions(img, markers):
    
    for i in range(0, frameH):
        for j in range(0,frameW):
        
            for m in range(-1,2):
                for n in range(-1,2):
                    if 0<i+m<frameH:
                        if 0<j+n<frameW:
                            if markers[i+m,j+n] != markers[i,j]:
                        
                                if img[i,j]==img[i+m,j+n]:
                                    markers[i,j] = markers[i+m,j+n]
                        
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
    
    img = cv2.imread('minimos.png',0)
    img = 255-img
    frameH, frameW = img.shape
    conn = np.ones((3,3))
    binary = peak_local_max(img, footprint=conn, indices=False, exclude_border=0)
    binary = np.uint8(binary)*255
    ret, markers = cv2.connectedComponents(binary)
    
    markers = correctregions(img, markers)
    border = findborder(markers)
    new = np.zeros([frameH,frameW,3], np.uint8)
    
    for x in range(0, len(border)):
        a=border[x][0]
        b=border[x][1]
        new[a,b] = [255,0,0]
    
    plt.figure('new markers')
    plt.imshow(new)
    #plt.imshow(markers, cmap=plt.cm.get_cmap('nipy_spectral'))
    