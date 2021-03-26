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

    accuracy = 1
    rangs = np.array([-32,-32])
    rang6= np.array([32,32])
    m=0
    factor=2**(L-1)
    e = 0.0000000000000000000001
    
    #initial motion vectors
    mv_x = 0
    mv_y = 0
    dx =[]
    dy=[]
    ox = []
    oy=[]

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
    targetDown2[0:int(frameH/2),0:int(frameW/2)] = targetFrame[0:frameH:2,0:frameW:2]
    targetDown3 = np.zeros([int(frameH/4),int(frameW/4)], dtype = np.uint16)
    targetDown3[0:int(frameH/4),0:int(frameW/4)] = targetDown2[0:int(frameH/2):2,0:int(frameW/2):2]
    
    anchorDown2 = np.zeros([int(frameH/2),int(frameW/2)], dtype = np.uint16)
    anchorDown2[0:int(frameH/2),0:int(frameW/2)] = anchorFrame[0:frameH:2,0:frameW:2]
    anchorDown3 = np.zeros([int(frameH/4),int(frameW/4)], dtype = np.uint16)
    anchorDown3[0:int(frameH/4),0:int(frameW/4)] = anchorDown2[0:int(frameH/2):2,0:int(frameW/2):2]
    
    
    #Search fields range for each level
    rangs = rangs/(factor+e)
    rang6 =rang6/(factor+e)
    frameH = int(frameH/(factor+e))
    frameW = int(frameW/(factor+e))
    rangestart = [0,0]
    rangeEnd =[0,0]  
    
    errorarray =[]
    for i in range(0, frameH-blocksize+1, blocksize):
        
        rangestart[0] = int(i + rangs[0])
        rangeEnd[0] = int(i + blocksize + rang6[0]) #-1
        
        if rangestart[0] < 0:
            rangestart[0] =0
                
        if rangeEnd[0]> frameH:
            rangeEnd[0] = frameH
            
        for j in range(0, frameW-blocksize+1, blocksize):
            
            rangestart[1] = int(j + rangs[1])
            rangeEnd[1] = int(j + blocksize + rang6[1]) #-1
        
            if rangestart[1] < 0:
                rangestart[1] =0
                
            if rangeEnd[1]> frameW*accuracy:
                rangeEnd[1] = int(frameW*accuracy)
            
            
            
            tmpt = np.zeros(targetDown3.shape, dtype = np.int16)
            tmpa = np.zeros(targetDown3.shape, dtype = np.int16)
            tmpt[:,:] = targetDown3[:,:]
            tmpa[:,:] = anchorDown3[:,:]
            
            #EBMA SCRIPT
            anchorBlock = np.zeros([blocksize,blocksize], np.int16)
            anchorBlock = tmpa[i:i+blocksize, j:j+blocksize]
            
            
        
            for y in range(rangestart[0], rangeEnd[0]-blocksize+1):
                for x in range(rangestart[1], rangeEnd[1]-blocksize+1):    
                    downtargetFrame = tmpt[y:y+accuracy*blocksize:accuracy, x:x+accuracy*blocksize:accuracy]
                    #calculate error
                    
                    temp_error = np.sum(np.absolute(anchorBlock -downtargetFrame))
                    errorarray.append(temp_error)
                    if temp_error < error:
                        
                        error = temp_error
                        while len(dx)<=m:
                            dx.append(0)
                            dy.append(0)
                            
                        mv_x = x/accuracy-j
                        mv_y = y/accuracy-i
                        dx[m]= mv_x
                        dy[m]= mv_y
                        print(dy)
            
            ox.append(j)
            oy.append(i)
            m= m+1
            print(m)
    
    for ii in range(L-1 , 1, -1):
          dx= dx*2   
          dy = dy*2
          framH = frameH*2
          
          lineW = np.floor(frameW/blocksize)
          frameW = frameW*2
          
            
    return errorarray

    


    




if __name__ == "__main__":
    
    anchorframe = cv2.imread('foremanY69.png',0)
    targetframe = cv2.imread('foremanY72.png',0)
    anchorframe = anchorframe.astype('uint16')
    targetframe = targetframe.astype('uint16')
    frameH, frameW = anchorframe.shape
    newFrame= HBMA(targetframe, anchorframe, 16,3)
    