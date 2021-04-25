# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 10:20:31 2020

@author: anusk
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

def EBMA(targetFrame, anchorFrame, blocksize):
    
    accuracy = 1
    p =16
    frameH, frameW = anchorFrame.shape
    print(anchorFrame.shape)
    predictFrame = np.zeros(anchorFrame.shape)
    
    k=0
    dx =np.zeros(int(frameH*frameW/blocksize**2))
    dy=np.zeros(int(frameH*frameW/blocksize**2))
    ox = np.zeros(int(frameH*frameW/blocksize**2))
    oy =np.zeros(int(frameH*frameW/blocksize**2))
    
    rangestart = [0,0]
    rangeEnd =[0,0]
    
    errorarray = []
    
        
    for n in range(0, frameH, blocksize):
 
        rangestart[0] = n*accuracy -p*accuracy
        rangeEnd[0] = n*accuracy + blocksize*accuracy + p*accuracy

        if rangestart[0] < 0:
            rangestart[0] =0
            
        if rangeEnd[0]> frameH*accuracy:
            rangeEnd[0] = frameH*accuracy
        
        for m in range(0, frameW, blocksize):
        
            rangestart[1] = m*accuracy -p*accuracy
            rangeEnd[1] = m*accuracy + blocksize*accuracy + p*accuracy
    
            if rangestart[1] < 0:
                rangestart[1] =0
                
            if rangeEnd[1]> frameW*accuracy:
                rangeEnd[1] = frameW*accuracy
            """
            EBMA ALGORITHM
            """
            anchorblock = anchorFrame[n:n+blocksize, m:m+blocksize]
            mv_x = 0
            mv_y = 0
            
            error = 255*blocksize*blocksize*100
            
            for x in range(rangestart[1], rangeEnd[1]-blocksize):
                for y in range(rangestart[0], rangeEnd[0]-blocksize):
                    targetblock = targetFrame[y:y+blocksize, x:x+blocksize]
                    anchorblock = np.float64(anchorblock)
                    targetblock = np.float64(targetblock)
                    temp_error = np.sum(np.uint8(np.absolute(anchorblock -targetblock)))
                    if temp_error < error:
                        error = temp_error
                        mv_x = x/accuracy-m
                        mv_y = y/accuracy-n
                        errorarray.append(error)
                        predictFrame[n:n+blocksize, m:m+blocksize] = targetblock
                        dx[k]= mv_x
                        dy[k]= mv_y
            
            ox[k] = m
            oy[k] = n
            k = k + 1
    
    mv_d = [dx, dy]
    mv_o = [ox, oy]
    return np.uint8(predictFrame), mv_o, mv_d, errorarray
                    
if __name__ == "__main__":
    
    anchorframe = cv2.imread('foremanY69.png',0)
    targetframe = cv2.imread('foremanY72.png',0)
    
    newFrame, origin, direction, error= EBMA(targetframe, anchorframe, 32)
    cv2.imshow('new frame', newFrame)
    cv2.waitKey(0)
    cv2.destroyWindow('new frame')  