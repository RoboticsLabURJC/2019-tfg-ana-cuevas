# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 10:42:43 2020

@author: anusk
"""

import cv2
import imfunctions as imf
import numpy as np

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

def plusnoise(img, noiseType):
    
    if noiseType == "gauss":
        newimg = imf.imnoise(img,"gauss",[0,0.005])
        
    elif noiseType == "sandp":
        newimg = imf.imnoise(img,'sandp',0.01)
        
    else: 
        print('incorrect noisetype')
    
    return newimg

def getfps(movie):
    
    vidcap = cv2.VideoCapture(movie)
    fps =vidcap.get(cv2.CAP_PROP_FPS)
    vidcap.release()
    return fps
        
def addnoise(movie, out, noiseType, noisyframes):
    
    Frames = getframes(movie)
    fps = getfps(movie)
    newframes = Frames
    if len(Frames) < 1:
        print('error al leer el video')
    
    if not isinstance(noisyframes, list):
        print('noisyframes must be a list')
    
    if len(noisyframes) == 0:
        noisyframes = [i for i in range(len(Frames))]
    else:
        for item in noisyframes:
            if type(item) != int: 
                print('noisyframes must contain integers')
            if item not in range(len(Frames)):
                print('frame number out of bounds')
    
    channels = len(Frames[0].shape)
    if channels == 2:
        color = False
        height, width = Frames[0].shape
 
    if channels == 3:
        color = True
        height, width, layers = Frames[0].shape
        
    size = (width,height)
    
    for frame_number in noisyframes:
        print(frame_number)
        #frame_number = noisyframes[i]
        if not color:
            newframes[frame_number] = plusnoise(Frames[frame_number], noiseType)
        else:
            B,G,R = cv2.split(Frames[frame_number])
            newB = plusnoise(B, noiseType)
            newG = plusnoise(G, noiseType)
            newR = plusnoise(R, noiseType)
            
            newframes[frame_number] = cv2.merge((newB,newG,newR))
    
    out = cv2.VideoWriter(out,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(newframes)):
        out.write(newframes[i])
    out.release()
    
def tempNoiseFilter(movie, out, numAvgFrames):
    
    Frames = getframes(movie)
    fps = getfps(movie)
    newFrames = []
    channels = len(Frames[0].shape)
    if channels == 2:
        height, width = Frames[0].shape
 
    if channels == 3:
        height, width, layers = Frames[0].shape
        
    size = (width,height)
    
    for k in range(len(Frames)):
    #for k in range(10):
        print(k)
        if k >= numAvgFrames:
            sumFrames = np.float64(np.zeros( Frames[0].shape))
            for m in range(numAvgFrames):
                sumFrames += np.float64(Frames[k-m])
            meanFrames = sumFrames/numAvgFrames
            
            meanFrames = np.uint8(meanFrames)
            newFrames.append(meanFrames)
            
        else:
            newFrames.append(Frames[k])
                
    out = cv2.VideoWriter(out,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
 
    for i in range(len(newFrames)):
        out.write(newFrames[i])
    out.release()
        
                
if __name__ == "__main__":
    movie = 'grandma_qcif.y4m'
    addnoise(movie, 'noisegrandma.avi', "sandp", [])
    print('done addingnoise')
    
    movie = 'noisegrandma.avi'
    tempNoiseFilter(movie, 'filteredgrandma.avi', 5)
    print('done')