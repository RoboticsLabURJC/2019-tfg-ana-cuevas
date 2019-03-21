# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 12:13:53 2019

@author: Ana
"""

import numpy as np
import cv2

def RGB2ind(img):
    
    h,w,d = img.shape
    R,G,B = cv2.split(img)
    
    colors = []
    
   # for i in range(0, h-1):
        #for j in range(0, w-1):
    for i in range(0, 15):
        for j in range(0, 15):
            val = [R[i,j], G[i,j], B[i,j]]
            new = True
            
            for color in colors:
                
                if color[1] == val:
                    color[0] += 1
                    new = False
                    break
            if new:
                c = [0, val]
                colors.append(c)
    
    colors.sort(reverse= True)
    print(colors)
    return img, colors

if __name__ == "__main__":
    imgcolor = cv2.imread('lena.jpg')
    imgRGB = cv2.cvtColor(imgcolor, cv2.COLOR_BGR2RGB)
    
    [m, n] = RGB2ind(imgRGB)