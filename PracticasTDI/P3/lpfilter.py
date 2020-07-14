# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:17:20 2020

@author: anusk
"""

import numpy as np
import math
import cv2

def dftuv(M, N):
    
    u = np.arange(M)
    v = np.arange(N)
    print(u)
    print(v)
    idx = np.nonzero(u > M/2)
    u[idx] = u[idx] -M
    print(idx)
    idy = np.nonzero(v > N/2)
    print(idy)
    v[idy] = v[idy] -N
    V, U = np.meshgrid(v,u)
    
    return U, V

def lpfilter(tipo, M, N, Do):
    
    U, V = dftuv(M,N)
    D = np.sqrt(U**2 + V**2)
    print(D)
    if tipo == 'ideal':
        H = np.matrix(D<=Do)
        H = np.float32(H)
    elif tipo == 'gaussian':
        H = np.exp(-(D**2)/(2*(Do**2)))
    else: 
        print('Unknown filter type.')
    
    return H
        
if __name__ == "__main__":
    
    filt = lpfilter('gaussian', 20, 20, 6 )
    print(filt)
    