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
    #counts = 256
    probs = counts / n_labels
    #print('probs' + str(probs))
    n_classes = np.count_nonzero(probs)
    #print('nclases  ' + str(n_classes))
    if n_classes <= 1:
        return 0
    
    ent = 0.
    
    # Compute standard entropy.
    for i in probs:
        if i != 0:
            #ent -= i * math.log(i, base=n_classes)
            ent -= i * log(i, n_classes)
    
    #print('entropia' + str(ent))
    return ent

if __name__ == "__main__":
    
    img = cv2.imread('cormoran_rgb.jpg', True)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    h, w = img.shape

    J = copy.deepcopy(img)
    J = np.float64(J)
    
    for i in range(4, h-4):
            for j in range(4, w-4):
                
                x = img[i-4:i+5,j-4:j+5]
                x = np.reshape(x, 81)
                
                #print(x.dtype)

                J[i,j]= entropy2(x)
                
                
                
    cv2.imshow('stdfilt', J)
    cv2.waitKey(0)
    cv2.destroyWindow('stdfilt')