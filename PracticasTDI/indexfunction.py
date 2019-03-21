# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:13:31 2019

@author: Ana
"""

import numpy as np
import cv2

def RGB2ind(img):
    
    h,w,d = img.shape
    R,G,B = cv2.split(img)
    
    colors = {}
    
    for i in range(0, h-1):
        for j in range(0, w-1):
            
            val = (R[i,j], G[i,j], B[i,j])
            
            if val in colors:
                colors[val] +=1
            else:
                colors[val] = 1
    
    colorsorder = [(k, colors[k]) for k in sorted(colors, key=colors.get, reverse=True)]
    colormap = []
    #print(colorsorder)
    count= 0
    for i in range(0, 255):
        count += colorsorder[i][1]
    print(count)
    print(h*w)
    
    for i in range(0, 255):
        k= colorsorder[i][0]
        l = list(k)
        print(l)

    return [img, colors]

if __name__ == "__main__":
    imgcolor = cv2.imread('lena.jpg')
    imgRGB = cv2.cvtColor(imgcolor, cv2.COLOR_BGR2RGB)
    
    [m, n] = RGB2ind(imgRGB)