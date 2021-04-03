# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 10:59:47 2021

@author: anusk
"""

import cv2
import numpy as np

def HBMA(targetFrame, anchorFrame, blocksize,L):
    
    anchorFrame = anchorFrame.astype('uint16')
    targetFrame = targetFrame.astype('uint16')
    predictFrame = np.zeros(anchorFrame.shape)
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
    
    anchorDown1 = np.copy(anchorFrame)
    targetDown1 = np.copy(targetFrame)
    targetDown2 = np.zeros([int(frameH/2),int(frameW/2)], dtype = np.uint16)
    targetDown2[0:int(frameH/2),0:int(frameW/2)] = targetFrame[0:frameH:2,0:frameW:2]
    targetDown3 = np.zeros([int(frameH/4),int(frameW/4)], dtype = np.uint16)
    targetDown3[0:int(frameH/4),0:int(frameW/4)] = targetDown2[0:int(frameH/2):2,0:int(frameW/2):2]
    
    anchorDown2 = np.zeros([int(frameH/2),int(frameW/2)], dtype = np.uint16)
    anchorDown2[0:int(frameH/2),0:int(frameW/2)] = anchorFrame[0:frameH:2,0:frameW:2]
    anchorDown3 = np.zeros([int(frameH/4),int(frameW/4)], dtype = np.uint16)
    anchorDown3[0:int(frameH/4),0:int(frameW/4)] = anchorDown2[0:int(frameH/2):2,0:int(frameW/2):2]
    predictFrame = np.copy(anchorFrame)
    
    #Search fields range for each level
    rangs = rangs/(factor+e)
    rang6 =rang6/(factor+e)
    frameH = int(frameH/(factor+e))
    frameW = int(frameW/(factor+e))
    rangestart = [0,0]
    rangeEnd =[0,0]  
    
    
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
                    
                    if temp_error < error:
                        
                        error = temp_error
                        while len(dx)<=m:
                            dx.append(0)
                            dy.append(0)
                            
                        mv_x = x/accuracy-j
                        mv_y = y/accuracy-i
                        dx[m]= mv_x
                        dy[m]= mv_y
            
            ox.append(j)
            oy.append(i)
            m= m+1
    dy = np.asarray(dy)
    dx = np.asarray(dx)

    for ii in range(L-1 , 0, -1):
          print(ii)
          dx= dx*2   
          dy = dy*2
          frameH = frameH*2
          
          lineW = np.floor(frameW/blocksize)
          frameW = frameW*2
          ttt = dy.size -1
          m = 0
          dxx =[]
          dyy=[]
          
          for i in range(0, frameH-blocksize+1, blocksize):            
            baseline = round(((i+1)/2)/blocksize) * lineW
            
            for j in range(0, frameW-blocksize+1, blocksize):
                mindx = int(np.floor(baseline+ round(((j+1)/2)/blocksize)+1))
                
                if mindx>ttt:
                    mindx = ttt
                
                
                rangestart[0] = np.int16(i+dy[mindx]+rangs[0])
                rangeEnd[0]= np.int16(i+dy[mindx]+blocksize+rang6[0])
                
                if rangestart[0] < 0:
                    rangestart[0] =0
                    
                if rangeEnd[0]> frameH:
                    rangeEnd[0] = frameH
                
                rangestart[1] = np.int16(j + dx[mindx]+rangs[1])
                rangeEnd[1] = np.int16(j + dx[mindx] + blocksize +rang6[1])
                
                if rangestart[1] < 0:
                    rangestart[1] =0
                    
                if rangeEnd[1]> frameW*accuracy:
                    rangeEnd[1] = int(frameW*accuracy)
                    
               #Level 2
                
                if ii==2:
                    tmpt=targetDown2[:,:]
                    tmpa = anchorDown2[:,:]
                
                if ii==1:
                    tmpt=targetDown1[:,:]
                    tmpa = anchorDown1[:,:]
                
                tmpt = np.int16(tmpt)
                tmpa = np.int16(tmpa)
                anchorBlock = tmpa[i:i+blocksize, j:j+blocksize]
                mv_x =0
                mv_y=0
                error = 255*blocksize*blocksize*100
                for y in range(rangestart[0], rangeEnd[0]-blocksize+1):
                    for x in range(rangestart[1], rangeEnd[1]-blocksize+1):
                        downtargetFrame = tmpt[y:y+accuracy*blocksize:accuracy, x:x+accuracy*blocksize:accuracy]
                        temp_error = np.sum(np.absolute(anchorBlock -downtargetFrame))
                        
                        if temp_error<error:
                            error = temp_error
                            mv_x = x/accuracy-j
                            mv_y = y/accuracy-i
                            while len(dxx)<=m:
                                dxx.append(0)
                                dyy.append(0)
                            
                            dxx[m]= mv_x
                            dyy[m]= mv_y
                            predictFrame[i:i+blocksize, j:j+blocksize] = downtargetFrame
                
                if m==351 :
                    print(m)
                
                if len(ox)<m:
                    ox[m] = i
                    oy[m] =j
                else:
                    ox.append(i)
                    oy.append(j)
                m = m+1
                
          
          dx = np.asarray(dxx)
          dy = np.asarray(dyy)
    
    mv_d = [dx,dy]
    mv_o = [np.array(ox), np.array(oy)]    
                            
                
    return [np.uint8(predictFrame), mv_o, mv_d]

    


    




if __name__ == "__main__":
    
    anchorframe = cv2.imread('foremanY69.png',0)
    targetframe = cv2.imread('foremanY72.png',0)
    anchorframe = anchorframe.astype('uint16')
    targetframe = targetframe.astype('uint16')
    frameH, frameW = anchorframe.shape
    newFrame, origin, direction= HBMA(targetframe, anchorframe, 16,3)
    cv2.imshow('new frame', newFrame)
    cv2.waitKey(0)
    cv2.destroyWindow('new frame')  