# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 00:41:58 2020

@author: anusk
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from matplotlib import colors as mpc

def rgb2ind(img, n):
    
    print("entra en la función")
    I_R,I_G,I_B = cv2.split(img)
    nrows, ncols = I_B.shape

    I_B_res = np.reshape(I_B, (nrows*ncols,1))
    I_R_res = np.reshape(I_R, (nrows*ncols,1))
    I_G_res = np.reshape(I_G, (nrows*ncols,1))
    print("hace el reshape")
    
    I_res = np.concatenate((I_R_res,I_G_res, I_B_res),axis=1)
    kmeans = KMeans(n_clusters=n)
    pred_y = kmeans.fit_predict(I_res)
    eti = kmeans.labels_
    print(eti.shape)
    colormap = kmeans.cluster_centers_
    print(colormap.shape)
    pixel_labels = np.reshape(eti, (nrows, ncols))
    return [pixel_labels, colormap]

if __name__ == "__main__":
    
    img = cv2.imread('lena.jpg', True)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lena255, cmap= rgb2ind(img, 5)
    
    newcmp = mpc.ListedColormap(cmap/255)
    print(newcmp)
    plt.figure('Colormap 255 levels')
    plt.imshow(lena255, cmap = newcmp)
    plt.xticks([]), plt.yticks([])
    for spine in plt.gca().spines.values():  #hide image border
        spine.set_visible(False)
    plt.show()