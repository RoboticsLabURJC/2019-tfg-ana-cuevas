# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 18:26:10 2021

@author: anusk
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def rangefilt(img):
    EE = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    E = cv2.erode(img,EE,iterations = 1)
    D =cv2.dilate(img, EE)
    
    J = D-E
    return J

    
if __name__ == "__main__":
    
    img = cv2.imread('cormoran_rgb.jpg', True)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    J = rangefilt(img)
    plt.figure('Segmented image')
    plt.imshow(J, cmap='gray')