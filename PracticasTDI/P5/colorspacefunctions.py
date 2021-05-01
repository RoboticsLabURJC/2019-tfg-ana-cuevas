# -*- coding: utf-8 -*-
"""
Created on Sat May  1 10:27:05 2021

@author: anusk
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt

def rgb2xyz(img):
    
    img = np.double(img)/255
    r,g,b = cv2.split(img)
    x = 0.4887180*r + 0.3106803*g + 0.2006017*b
    y = 0.1762044*r + 0.8129847*g + 0.0108109*b
    z = 0.0000000*r + 0.0102048*g + 0.9897952*b
    
    xyz =cv2.merge((x,y,z))
    
    return xyz, x, y, z

def rgb2lab76(rgb):
    
    xyz, x, y, z = rgb2xyz(rgb)
    
    l = np.zeros(x.shape, dtype = np.double)
    a = np.zeros(x.shape, dtype = np.double)
    b = np.zeros(x.shape, dtype = np.double)
    
    x0 = 0.4887180 + 0.3106803 + 0.2006017
    y0 = 0.1762044 + 0.8129847 + 0.0108109
    z0 = 0.0000000 + 0.0102048 + 0.9897952
    
    xn = x/x0
    yn = y/y0
    zn = z/z0
    
    id1 =  np.zeros(x.shape, dtype = np.bool_)
    id1[xn > (6/29)**3] = True
    id2 =  np.zeros(x.shape, dtype = np.bool_)
    id2[xn <= (6/29)**3] = True
    id3 =  np.zeros(x.shape, dtype = np.bool_)
    id3[np.logical_and(xn > (6/29)**3,yn > (6/29)**3)] = True
    id4 =  np.zeros(x.shape, dtype = np.bool_)
    id4[np.logical_and((xn > (6/29)**3), (yn <= (6/29)**3))] = True
    id5 =  np.zeros(x.shape, dtype = np.bool_)
    id5[np.logical_and((xn <= (6/29)**3), (yn > (6/29)**3))] = True
    id6 =  np.zeros(x.shape, dtype = np.bool_)
    id6[np.logical_and((xn <= (6/29)**3),(yn <= (6/29)**3))] = True
    id7 =  np.zeros(x.shape, dtype = np.bool_)
    id7[np.logical_and((yn > (6/29)**3), (zn > (6/29)**3))] = True
    id8 =  np.zeros(x.shape, dtype = np.bool_)
    id8[np.logical_and((yn > (6/29)**3), (zn <= (6/29)**3))] = True
    id9 =  np.zeros(x.shape, dtype = np.bool_)
    id9[np.logical_and((yn <= (6/29)**3), (zn > (6/29)**3))] = True
    id10 =  np.zeros(x.shape, dtype = np.bool_)
    id10[np.logical_and((yn <= (6/29)**3), (zn <= (6/29)**3))] = True
    
    t0a = (1/3)*((29/6)**2);
    t0b = 4/29;
    
    
    l[id1] = 116*(yn[id1]**(1/3))-16
    l[id2] = 116*(t0a*yn[id2]+t0b)-16
    
    a[id3] = 500*(xn[id3]**(1/3)-yn[id3]**(1/3))
    a[id4] = 500*(xn[id4]**(1/3)-(t0a*yn[id4]+t0b))
    a[id5] = 500*((t0a*xn[id5]+t0b)-yn[id5]**(1/3))
    a[id6] = 500*((t0a*xn[id6]+t0b)-(t0a*yn[id6]+t0b))
    
    
    b[id7] = 200*(yn[id7]**(1/3)-zn[id7]**(1/3))
    b[id8] = 200*(yn[id8]**(1/3)-(t0a*zn[id8]+t0b))
    b[id9] = 200*((t0a*yn[id9]+t0b)-zn[id9]**(1/3))
    b[id10] = 200*((t0a*yn[id10]+t0b)-(t0a*zn[id10]+t0b));
    
    lab =cv2.merge((l,a,b))
    return lab
    
if __name__ == "__main__":
    
    img = cv2.imread('cormoran_rgb.jpg')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cormoran_lab = rgb2lab76(img)
    
    #plt.figure('Segmented image')
    #plt.imshow(maximos, cmap='gray')