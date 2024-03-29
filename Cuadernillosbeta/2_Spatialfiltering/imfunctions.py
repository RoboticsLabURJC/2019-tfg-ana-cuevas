# -*- coding: utf-8 -*-
"""
Función para añadir ruido

parameters:
    img: uint8 black and white img
    noise: The type of noise, the options are 'gauss' for Gaussian noise,
        'sandp' for salt and pepper noise
    par: This are the parameters that define the noise, in the case of
        Gaussian is a Touple of mean and variance and in salt and pepper
        is density
"""
import numpy as np
import cv2
import math
from matplotlib import pyplot as plt

def im2double(im):
    info = np.iinfo(im.dtype) # Get the data type of the input image
    return im.astype(np.float) / info.max # Divide all values by the largest
                                          #possible value in the datatype
                                          
def imdoublefloat2uint8(im):
    
    h, w = im.shape
    
    
    for i in range(0, h):
        for j in range(0, w):
            
            if im[i,j]<=0.0:
                
                im[i,j]= 0;
                
            if im[i,j]>1.0:
                im[i,j]= 1.0;
    im = im*255
    
    return im.astype(np.uint8)

def addnoise(imgd, noise, par):
    
    imgd = im2double(imgd)
    h,w = imgd.shape
    
    if noise == "gauss":
        
        m, v = par
        nmat = np.random.standard_normal(size=(h,w))
        nmat = math.sqrt(v)*nmat + m
        noisy = imgd + nmat
        noisy = imdoublefloat2uint8(noisy)
        return noisy
        
    elif noise == "sandp":
        d = par*0.5   #The parameter indicates total density, divide by two
                      # to get salt density and pepper density
        numpix =np.ceil(d* imgd.size) #The total number of pixels affected
        
        numpix = numpix.item()
        out = np.copy(imgd)
        
        #get noise coords
        
        saltx = np.random.randint(0, h-1, int(numpix))
        salty = np.random.randint(0, w-1, int(numpix))
        pepperx = np.random.randint(0, h-1, int(numpix))
        peppery = np.random.randint(0, w-1, int(numpix))
        
        for i in range(0, int(numpix)-1):
            
            out[saltx[i],salty[i]] = 1
        
            out[pepperx[i],peppery[i]] = 0
        
        #print('out double')
        #print(out)
        out = imdoublefloat2uint8(out)
        #print('out uint 8')
        #print(out)
        return(out)
    
    elif noise == "speckle":
        
        v = par
        
        nmat = np.random.uniform(-0.5, 0.5, (h,w))
        #print(nmat.shape)
        noisy = imgd + math.sqrt(12*v)*np.multiply(imgd,nmat);
        noisy = imdoublefloat2uint8(noisy)
        return noisy
        
    else:
        print("Incorrect argument fo noise")
        return(img)

def checkcolor(img):

    channels = len(img.shape)
    if channels == 2:
        color = False
 
    if channels == 3:
        color = True
    return color

def imnoise(img, noise = "gauss", par = [0,0.01]):
    
    color =checkcolor(img)
    
    if color:
        channels = cv2.split(img)
        colors = []
        i = 0
        for channel in channels:
            colors.append(addnoise(channel, noise, par))
            i += 1
        noisy = cv2.merge((colors[0],colors[1],colors[2]))
        
    else:
       noisy = addnoise(img, noise, par) 
    
    return noisy
        
#img = np.matrix([[127, 32, 24, 36, 80, 95],[127, 32, 46, 36, 80, 95],[127, 32, 100, 36, 80, 95],[64, 255, 8, 12, 25, 67]], dtype = 'uint8')
#print(img)
#imnoise(img, "speckle", 0.1)
    
if __name__ == "__main__":
    img = cv2.imread('frame1.jpg')
    out = imnoise(img, "gauss",[0,0.005])
    cv2.imwrite('noise.jpg', out)