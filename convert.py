import numpy as np
import cv2 as cv
from mss import mss
from PIL import Image

import sys

'''
cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        print("No more frames, exiting")
        break
        
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, (80, 60)) 
    #tret, black = cv.threshold(gray,127,255,cv.THRESH_BINARY)
    black = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,15,0)
    finalframe = cv.resize(black, (800, 600), interpolation = cv.INTER_NEAREST) 
    
    cv.imshow('frame', finalframe)
    
    gpuData = [[0 for i in range(10)] for j in range(60)]
    
    for y in range(0, 60):
        for x in range(0, 10):
            for bit in range(0,8):
                if black[y,(x * 8) + bit] > 0:
                    #print('#', end='')
                    gpuData[y][x] |= 0b00000001
                else:
                    #print('.', end='')
                    gpuData[y][x] &= 0b11111110
                
                if (bit != 7):
                    gpuData[y][x] = gpuData[y][x] << 1
                #print(black[y,(x * 8) + bit], end='')
        #print()
        
    print(gpuData)
    
    if cv.waitKey(1) == ord('q'):
        break
'''

while True:
    screenFrame = mss().grab({'left': 100, 'top': 100, 'width': 800, 'height': 600})
    
    frame = Image.frombytes(
        'RGB', 
        (screenFrame.width, screenFrame.height), 
        screenFrame.rgb,
    )
        
    gray = cv.cvtColor(np.array(frame), cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, (80, 60)) 
    #tret, black = cv.threshold(gray,127,255,cv.THRESH_BINARY)
    black = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,int(sys.argv[1]),int(sys.argv[2]))
    finalframe = cv.resize(black, (800, 600), interpolation = cv.INTER_NEAREST) 
    
    cv.imshow('frame', finalframe)
    
    gpuData = [[0 for i in range(10)] for j in range(60)]
    
    for y in range(0, 60):
        for x in range(0, 10):
            for bit in range(0,8):
                if black[y,(x * 8) + bit] > 0:
                    #print('#', end='')
                    gpuData[y][x] |= 0b00000001
                else:
                    #print('.', end='')
                    gpuData[y][x] &= 0b11111110
                
                if (bit != 7):
                    gpuData[y][x] = gpuData[y][x] << 1
                #print(black[y,(x * 8) + bit], end='')
        #print()
        
    for line in gpuData:
        print(line)
    print("======================")
    
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()