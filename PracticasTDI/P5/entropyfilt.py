# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:17:09 2020

@author: anusk
"""

import numpy as np
from scipy.stats import entropy
from math import log, e
import pandas as pd
import copy
import cv2



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

def entropyfilter(img):
    

    J = copy.deepcopy(img)
    F = np.zeros(J.shape, dtype=np.float64)
     
    J = np.pad(J, ((4, 4), (4, 4)), 'reflect')
    h, w = J.shape
    
    for i in range(4, h-4):
            for j in range(4, w-4):
                
                x = J[i-4:i+5,j-4:j+5]           
                x = np.reshape(x, 81)
                F[i-4,j-4]= entropy2(x)
                
    F = F/F.max()
    
                
    return np.uint8(255*F) 

if __name__ == "__main__":
    
    img = cv2.imread('cormoran_rgb.jpg', True)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    J = entropyfilter(img)

    cv2.imshow('stdfilt', J)
    cv2.waitKey(0)
    cv2.destroyWindow('stdfilt')          
