# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 11:19:37 2021

@author: anusk
"""

import cv2
import numpy as np
import scipy.interpolate as spi
from matplotlib import pyplot as plt

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
                        predictFrame[n:n+blocksize, m:m+blocksize] = targetblock
                        dx[k]= mv_x
                        dy[k]= mv_y
            
            ox[k] = m
            oy[k] = n
            k = k + 1
    
    mv_d = [dx, dy]
    mv_o = [ox, oy]
    return np.uint8(predictFrame), mv_o, mv_d

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
    ox = np.zeros(int(frameH*frameW/blocksize**2))
    oy=np.zeros(int(frameH*frameW/blocksize**2))

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
            
            ox[m] =i
            oy[m] =j
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
          dxx =np.zeros(int(frameH*frameW/blocksize**2))
          dyy=np.zeros(int(frameH*frameW/blocksize**2))
          
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

                            dxx[m]= mv_x
                            dyy[m]= mv_y
                            predictFrame[i:i+blocksize, j:j+blocksize] = downtargetFrame
                
                
                    ox[m] = j
                    oy[m] =i

                    
                m = m+1
                
          
          dx = dxx
          dy = dyy
    
    mv_d = [dx,dy]
    mv_o = [ox, oy]    
                            
                
    return [np.uint8(predictFrame), mv_o, mv_d]

def PhaseCorrelation(anchorFrame, targetFrame):
    
    anchorFrame =np.double(anchorFrame)
    targetFrame =np.double(targetFrame)
    frame = np.dstack((anchorFrame, targetFrame))
    
    dimy = anchorFrame.shape[0]
    dimx = anchorFrame.shape[1]
    
    blockx = 16
    blocky = 16
    
    matchy=np.zeros([int(dimy/blocky),int(dimx/blockx)], np.double)
    matchx=np.zeros([int(dimy/blocky),int(dimx/blockx)], np.double)
    halfy=np.zeros([int(dimy/blocky),int(dimx/blockx)], np.double)
    halfx=np.zeros([int(dimy/blocky),int(dimx/blockx)], np.double)
    
    #window de fft
    T = 32
    winv=np.arange(32)
    alpha=0
    a =(winv-(T/2))/T
    b = np.cos(alpha*np.pi*((winv-(T/2))/T))
    c = 1-np.square(2*alpha*(winv-(T/2))/T)
    window= np.array([np.sinc(a*b/c)])
    windowT = window.T
    windowT.T
    window = windowT @ window
    
    for loopi in range(2,int(dimy/blocky)):
        
        for loopj in range(2,int(dimx/blockx)):
            ybound1 = (loopi-1)*blocky
            ybound2 = loopi*blocky
            xbound1 = (loopj-1)*blockx
            xbound2 = loopj*blockx
            
            #divide frame into blocks
            previous = anchorFrame[ybound1-8:ybound2+8, xbound1-8:xbound2+8]
            block = targetFrame[ybound1-8:ybound2+8, xbound1-8:xbound2+8]
            B_prev = np.fft.fft2(previous,[blocky*2,blockx*2])
            B_curr = np.fft.fft2(block*window,[blocky*2,blockx*2])
            mul = B_curr*np.conj(B_prev)
            mag = np.abs(mul)
            mag[mag==0] = 1e-31
            C = mul/mag
            c=np.fft.fftshift(np.abs(np.fft.ifft2(C)))
            [tempy,tempx] = np.where(c==c.max())
            matchy[loopi-1,loopj-1]=tempy[0]-blocky
            matchx[loopi-1,loopj-1]=tempx[0]-blockx
            
            if tempy[0]>=1 and tempy[0]+1<=31:
                tt = np.arange(-1,2)
                ppy = np.array([c[tempy[0]-1,tempx[0]],
                                c[tempy[0],tempx[0]],
                                c[tempy[0]+1,tempx[0]]])
                ii=np.arange(-1,1.5,0.5)
                iiy= spi.interp1d(tt,ppy,kind="quadratic", fill_value="extrapolate")(ii)
                if iiy[1]>c[tempy[0],tempx[0]]:
                    halfy[loopi-1,loopj-1]=-1
                elif iiy[3]>c[tempy[0],tempx[0]]:
                    halfy[loopi-1,loopj-1]=-1
                     
            if tempx[0]>=1 and tempx[0]+1<31:
                tt = np.arange(-1,2)
                ppx = np.array([c[tempy[0],tempx[0]-1],
                                c[tempy[0],tempx[0]],
                                c[tempy[0],tempx[0]+1]])
                ii=np.arange(-1,1.5,0.5)
                iix= spi.interp1d(tt,ppx,kind="quadratic", fill_value="extrapolate")(ii)
                if iix[1]>c[tempy[0],tempx[0]]:
                    halfx[loopi-1,loopj-1]=-1
                elif iix[3]>c[tempy[0],tempx[0]]:
                    halfx[loopi-1,loopj-1]=-1
    
    fig,ax = plt.subplots()
    ax.quiver(matchx,matchy)  
    plt.show()                  
    
    #MC prediction
    predict = np.zeros([dimy,dimx], np.double) 
            
    for loopi in range(1, int(dimy/blocky)+1):
        for loopj in range(1, int(dimx/blockx)+1):
            ybound1 = (loopi-1)*blocky
            ybound2 = loopi*blocky
            xbound1 = (loopj-1)*blockx
            xbound2 = loopj*blockx
            
            offy = -matchy[loopi-1,loopj-1]
            offx = -matchx[loopi-1,loopj-1]
            
            pred = anchorFrame[abs(int(ybound1+offy)):abs(int(ybound2+offy)), abs(int(xbound1+offx)):abs(int(xbound2+offx))]
            
            if halfy[loopi-1,loopj-1] == 1:
                average = anchorFrame[abs(int(ybound1+offy))-1:abs(int(ybound2+offy))-1,
                                      abs(int(xbound1+offx)):abs(int(xbound2+offx))]
                pred = 0.5*(pred+average)
            elif halfy[loopi-1,loopj-1] ==-1:
                average = anchorFrame[abs(int(ybound1+offy))+1:abs(int(ybound2+offy))+1,
                                      abs(int(xbound1+offx)):abs(int(xbound2+offx))]
                pred = 0.5*(pred+average)
            
            predict[ybound1:ybound2,xbound1:xbound2] = pred
            
    plt.figure()
    plt.imshow(predict,cmap='gray')
    plt.show()
    
    matchyy= matchy +0.5*halfy
    matchxx = matchx +0.5*halfx
    
    dy = matchyy[1:int(dimy/blocky)-1, 1:int(dimx/blockx)-1]
    dx = matchxx[1:int(dimy/blocky)-1, 1:int(dimx/blockx)-1]

    rangey = np.arange(np.min(dy), np.max(dy)+0.5,.05)
    