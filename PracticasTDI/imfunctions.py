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

def im2double(im):
    info = np.iinfo(im.dtype) # Get the data type of the input image
    return im.astype(np.float) / info.max # Divide all values by the largest
                                          #possible value in the datatype
                                          
def imdoublefloat2uint8(im):
    im = im*255
    return im.astype(np.uint8)

def imnoise(img, noise = "gauss", par = [0,0.01]):
    
    imgd = im2double(img)
    
    if noise == "gauss":
        h,w = img.shape
        m, v = par
        nmat = np.random.standard_normal(size=(h,w))
        nmat = v*nmat + m
        noisy = imgd + nmat
        noisy = imdoublefloat2uint8(noisy)
        return noisy
        
    elif noise == "sandp":
        d = par*0.5   #The parameter indicates total density, divide by two
                      # to get salt density and pepper density
        numpix =np.ceil(d* img.size) #The total number of pixels affected
        print(numpix)
        out = np.copy(imgd)
        print('out normal')
        print(out)
        #get noise coords
        for i in (numpix):
            coordssalt = np.random.randint(0, i - 1, 2)
            print(coordssalt)
            
            out[coordssalt[0],coordssalt[1]] = 1
            print('out modificada')
            print(out)
            coordspepper = np.random.randint(0, i - 1, 2)
            out[coordspepper[0], coordspepper[1]] = 0
        
        print('out double')
        print(out)
        imdoublefloat2uint8(out)
        print('out uint 8')
        print(out)
        return(out)
        
    else:
        print("Incorrect argument fo noise")
        return(img)
        
img = np.matrix([[127, 32, 24, 36, 80, 95],[127, 32, 46, 36, 80, 95],[127, 32, 100, 36, 80, 95],[64, 255, 8, 12, 25, 67]], dtype = 'uint8')
print(img)
imnoise(img, "sandp", 0.1)