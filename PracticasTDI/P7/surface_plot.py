# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:54:10 2020
https://gist.github.com/CMCDragonkai/dd420c0800cba33142505eff5a7d2589

"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2

def surface_plot (matrix, **kwargs):
    # acquire the cartesian coordinate matrices from the matrix
    # x is cols, y is rows
    (x, y) = np.meshgrid(np.arange(matrix.shape[1]), np.arange(matrix.shape[0]))
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(x, y, matrix, **kwargs)
    return (fig, ax, surf)

if __name__ == "__main__":
    
    img = cv2.imread('pueba3d.png',0)
    (fig2, ax2, surf) = surface_plot(img, cmap=plt.cm.coolwarm)

    fig2.colorbar(surf)
    
    ax2.set_xlabel('X (cols)')
    ax2.set_ylabel('Y (rows)')
    ax2.set_zlabel('Z (values)')
    
    plt.show()
