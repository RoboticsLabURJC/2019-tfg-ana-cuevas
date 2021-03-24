# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 10:59:47 2021

@author: anusk
"""

import cv2
import numpy as np

def HBMA(targetFrame, anchorFrame, blocksize,L):
    
    anchorframe = anchorFrame.astype('uint16')
    targetframe = targetFrame.astype('uint16')
    accuracy = 1
    p =16
    frameH, frameW = anchorFrame.shape
    print(anchorFrame.shape)
    accuracy = 1
    rangs = np.array([-32,-32])
    rang6= np.array([32,32])
    m=1
    factor=2^(L-1)
    e = 0.0000000000000000000001

    error = 255*blocksize*blocksize*100
    
    #Upownsample
    upanchorframe = np.zeros([frameH*2,frameW*2], dtype = np.uint16)
    upanchorframe[0:(frameH*2-1):2, 0:(frameW*2-1):2] = anchorFrame
    upanchorframe[0:(frameH*2-1):2, 1:(frameW*2-2):2] = (anchorFrame[:,0:frameW-1]+anchorFrame[:,1:frameW])/2
    upanchorframe[1:(frameH*2-2):2, 0:(frameW*2-1):2] = (anchorFrame[0:frameH-1, :]+anchorFrame[1:frameH, :])/2
    upanchorframe[1:(frameH*2-2):2, 1:(frameW*2-2):2] = (anchorFrame[0:frameH-1,0:frameW-1]+ anchorFrame[0:frameH-1, 1:frameW]+anchorFrame[1:frameH, 0:frameW-1]+anchorFrame[1:frameH,1:frameW])/4
    
    #Downsample

    anchorDown1 = anchorFrame
    targetDown1 = targetFrame
    targetDown2 = np.zeros([int(frameH/2),int(frameW/2)], dtype = np.uint16)
    targetDown2[0:int(frameH/2),0:int(frameW/2)] = targetFrame[0:frameH-1:2,0:frameW-1:2]
    targetDown3 = np.zeros([int(frameH/4),int(frameW/4)], dtype = np.uint16)
    targetDown3[0:int(frameH/4),0:int(frameW/4)] = targetFrame[0:int(frameH/2)-1:2,0:int(frameW/2)-1:2]
    
    anchorDown2 = np.zeros([int(frameH/2),int(frameW/2)], dtype = np.uint16)
    anchorDown2[0:int(frameH/2),0:int(frameW/2)] = anchorFrame[0:frameH-1:2,0:frameW-1:2]
    anchorDown3 = np.zeros([int(frameH/4),int(frameW/4)], dtype = np.uint16)
    anchorDown3[0:int(frameH/4),0:int(frameW/4)] = anchorFrame[0:int(frameH/2)-1:2,0:int(frameW/2)-1:2]
    
    
    #Search fields range for each level
    rangs = rangs/(factor+e)
    rang6 =rang6/(factor+e)
    frameH = int(frameH/(factor+e))
    frameW = int(frameW/(factor+e))
    
    return targetDown3

    


    #anchorDown2(1:frameHeight/2,1:frameWidth/2) = anchorFrame(1:2:frameHeight,1:2:frameWidth);
    #anchorDown3(1:frameHeight/4,1:frameWidth/4) = anchorDown2(2:2:frameHeight/2,1:2:frameWidth/2);
    #predictFrame = anchorFrame;




if __name__ == "__main__":
    
    anchorframe = cv2.imread('foremanY69.png',0)
    targetframe = cv2.imread('foremanY72.png',0)
    anchorframe = anchorframe.astype('uint16')
    targetframe = targetframe.astype('uint16')
    frameH, frameW = anchorframe.shape
    newFrame= HBMA(targetframe, anchorframe, 16,3)