# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 10:39:22 2020

@author: anusk
"""

import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

def getframes(movie):
    
    if not isinstance(movie, str):
        print('movie must be an string')
    
    vidcap = cv2.VideoCapture(movie)
    success,image = vidcap.read()
    count = 0
    frames = []
    while success:
      frames.append(image)     # save frame as JPEG file      
      success,image = vidcap.read()
      #print('Read a new frame: ', success)
      count += 1
    vidcap.release()
    
    return(frames)

def tempNoiseFilter(movie, out, numAvgFrames):
    
    Frames = getframes(movie)
    newFrames = []
    channels = len(Frames[0].shape)
    if channels == 2:
        height, width = Frames[0].shape
 
    if channels == 3:
        height, width, layers = Frames[0].shape
        
    size = (width,height)
    print(Frames[0].dtype)
    #cv2.imshow('pruebacv2', Frames[0])
    for k in range(len(Frames)):
    
        print(k)
        if k >= numAvgFrames:
            sumFrames = np.zeros( Frames[0].shape)
            for m in range(numAvgFrames):
                sumFrames =+ Frames[k-m]
                #cv2.imshow('%d'%(m), Frames[k-m])
            newFrames.append(sumFrames/numAvgFrames)
            meanFrames = sumFrames/numAvgFrames
            print(meanFrames.dtype)
            print(meanFrames.shape)
            
            meanFrames = np.uint8(meanFrames)
            #cv2.imshow('mean', meanFrames)
        else:
            newFrames.append(Frames[k])
                
    out = cv2.VideoWriter(out,cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
 
    for i in range(len(newFrames)):
        out.write(newFrames[i])
    out.release()

if __name__ == "__main__":
    movie = 'noisegrandma.avi'
    tempNoiseFilter(movie, 'filteredgrandma.avi', 5)
    print('done')