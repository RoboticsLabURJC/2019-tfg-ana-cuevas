# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 10:22:55 2021

@author: anusk
"""

def EBMA(targetFrame, anchorFrame, blocksize):
    
    accuracy = 1
    p =16
    frameH, frameW = anchorFrame.shape
    print(anchorFrame.shape)
    predictFrame = np.zeros(anchorFrame.shape)
    
    k=0
    dx =[]
    dy=[]
    ox = []
    oy =[]
    
    rangestart = [0,0]
    rangeEnd =[0,0]
    
    
    
    m= 100
        
    rangestart[1] = m*accuracy -p*accuracy
    rangeEnd[1] = m*accuracy + blocksize*accuracy + p*accuracy

    if rangestart[1] < 0:
        rangestart[1] =0
        
    if rangeEnd[1]> frameW*accuracy:
        rangeEnd[1] = frameW*accuracy
    
    n=100
    print('n')
    print(n)
    rangestart[0] = n*accuracy -p*accuracy
    rangeEnd[0] = n*accuracy + blocksize*accuracy + p*accuracy

    if rangestart[0] < 0:
        rangestart[0] =0
        
    if rangeEnd[0]> frameH*accuracy:
        rangeEnd[0] = frameH*accuracy
    
    """
    EBMA ALGORITHM
    """
    anchorblock = anchorFrame[n:n+blocksize, m:m+blocksize]
    mv_x = 0
    mv_y = 0
    dx.append(0)
    dy.append(0)
    
    error = 255*blocksize*blocksize*100
    
    for x in range(rangestart[1], rangeEnd[1]-blocksize):
        for y in range(rangestart[0], rangeEnd[0]-blocksize):
            targetblock = targetFrame[y:y+blocksize, x:x+blocksize]
            
            temp_error = np.sum(np.absolute(np.subtract(anchorblock, targetblock)))
            if temp_error < error:
                error = temp_error
                mv_x = y/accuracy-n
                mv_y = x/accuracy-m
                
                predictFrame[n:n+blocksize, m:m+blocksize] = targetblock
                dx[k]= mv_x
                dy[k]= mv_y
    
    ox.append(n)
    oy.append(m)
    k = k + 1
    
    #mv_d = [np.array(dx); np.array(dy)]
    #mv_o = [np.array(ox); np.array(oy)]
    return np.uint8(targetblock)

if __name__ == "__main__":
    
    anchorframe = cv2.imread('foremanY69.png',0)
    targetframe = cv2.imread('foremanY72.png',0)
    
    targetblock= EBMA(targetframe, anchorframe, 16)
    print(targetblock.shape)
    cv2.imshow('new frame', targetblock)
    cv2.waitKey(0)
    cv2.destroyWindow('new frame') 
    cv2.imwrite('targetblock.png', targetblock)