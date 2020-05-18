# -*- coding: utf-8 -*-
"""
Created on Mon May 18 10:59:52 2020

@author: anusk

This file contains the functions for two different texture filters.

stfilt: standar deviation filter
        input: uint8 gray scale image
        output : uint8 graysclae image

entropyfilt: entropy filter with padding of 9.
        input: uint8 gray scale image
        output : uint8 graysclae image
"""

import numpy as np
import copy
import cv2
from math import log, e

    
def entropy2(labels):
    """ Computes entropy of label distribution. """
 
    n_labels = labels.size
    
    if n_labels <= 1:
        return 0
    
    counts = np.bincount(labels)
    probs = counts / n_labels
    
    #n_classes = np.count_nonzero(probs)
    n_classes = 256
    #print('nclases  ' + str(n_classes))
    if n_classes <= 1:
        return 0
    
    ent = 0.
    
    # Compute standard entropy.
    for i in probs:
        if i != 0:
        
            ent -= i * log(i, n_classes)
    
    
    return ent

def entropyfilt(img):
    
    h, w = img.shape

    J = copy.deepcopy(img)
    J = np.float64(J)
    J = np.pad(J, ((4, 4), (4, 4)), 'reflect')
    
    for i in range(4, h-4):
            for j in range(4, w-4):
                
                x = img[i-4:i+5,j-4:j+5]
                x = np.reshape(x, 81)
                
                #print(x.dtype)

                J[i,j]= entropy2(x)
                
    
    J = J[4:h-4, 4:w-4]
    J = J/J.max()
    
                
    return np.uint8(255*J) 


def stdfilt(img):

    img = img / 255.0
    
    # c = imfilter(I,h,'symmetric');
    h = np.ones((3,3))
    n = h.sum()
    n1 = n - 1
    c1 = cv2.filter2D(img**2, -1, h/n1, borderType=cv2.BORDER_REFLECT)
    c2 = cv2.filter2D(img, -1, h, borderType=cv2.BORDER_REFLECT)**2 / (n*n1)
    J = np.sqrt( np.maximum(c1-c2,0) )
    
    return np.uint8(255*J)

