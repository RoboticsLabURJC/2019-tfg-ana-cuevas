# -*- coding: utf-8 -*-
"""
Created on Fri Apr  2 18:30:03 2021

@author: anusk
"""

import cv2
import numpy as np
import scipy.interpolate as spi
from matplotlib import pyplot as plt

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
    
    #fig,ax = plt.subplots()
    #ax.quiver(matchx,matchy)  
    #plt.show()                  
    
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
    plt.show

if __name__ == "__main__":
    
    anchorframe = cv2.imread('foremanY69.png',0)
    targetframe = cv2.imread('foremanY72.png',0)
    PhaseCorrelation(anchorframe, targetframe)
    