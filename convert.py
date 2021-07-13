import numpy as np
import cv2 as cv
from mss import mss
from PIL import Image

import gpiozero

import sys
import time

adr = []

adr.append(gpiozero.OutputDevice(27))
adr.append(gpiozero.OutputDevice(22))
adr.append(gpiozero.OutputDevice(10))
adr.append(gpiozero.OutputDevice(9))
adr.append(gpiozero.OutputDevice(11))
adr.append(gpiozero.OutputDevice(5))
adr.append(gpiozero.OutputDevice(6))
adr.append(gpiozero.OutputDevice(13))
adr.append(gpiozero.OutputDevice(19))
adr.append(gpiozero.OutputDevice(26))

dta = []

dta.append(gpiozero.OutputDevice(14))
dta.append(gpiozero.OutputDevice(15))
dta.append(gpiozero.OutputDevice(18))
dta.append(gpiozero.OutputDevice(23))
dta.append(gpiozero.OutputDevice(24))
dta.append(gpiozero.OutputDevice(25))
dta.append(gpiozero.OutputDevice(8))
dta.append(gpiozero.OutputDevice(7))

writeEnable = gpiozero.OutputDevice(2)


def outputAddress(addr):
    for i in range(0,10):
        if ((addr & 0b1) % 2 == 1):
            adr[9 - i].on()
        else:
            adr[9 - i].off()

        addr = addr >> 1

def outputData(data):
    for i in range(0,8):
        if ((data & 0b1) % 2  == 1):
            dta[7-i].on()
        else:
            dta[7-i].off()

        data = data >> 1

def writeToAddr(data, addr):
    outputAddress(addr)
    outputData(data)
    writeEnable.on()
    writeEnable.off()
    writeEnable.on()

def clearScreen():
    for i in range(0, 1024):
        writeToAddr(0, i)

def writeFrame(frame):
    for y in range(0, 60):
        for x in range(0, 10):
            gpuData = 0
            for bit in range(0,8):
                if frame[y,(x * 8) + bit] > 0:
                    gpuData |= 0b00000001
                else:
                    gpuData &= 0b11111110
                
                if (bit != 7):
                    gpuData = gpuData << 1
                else:
                    writeToAddr(gpuData,(((y << 4) & 0b1111110000) | (x & 0b1111)))

clearScreen()

if (len(sys.argv) >= 4):
    cap = cv.VideoCapture(str(sys.argv[3]))

while True:
    if (len(sys.argv) < 4):
        screenFrame = mss().grab({'left': 0, 'top': 0, 'width': 800, 'height': 600})
        
        frame = Image.frombytes(
            'RGB', 
            (screenFrame.width, screenFrame.height), 
            screenFrame.rgb,
        )
    else: #play video if filename is given
        ret, frame = cap.read()
    
        if not ret:
            print("No more frames, exiting")
            break
        
    gray = cv.cvtColor(np.array(frame), cv.COLOR_BGR2GRAY)
    gray = cv.resize(gray, (80, 60)) 
    #tret, black = cv.threshold(gray,127,255,cv.THRESH_BINARY)
    black = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,int(sys.argv[1]),int(sys.argv[2]))
    finalframe = cv.resize(black, (800, 600), interpolation = cv.INTER_NEAREST) 
    
    cv.imshow('frame', finalframe)
    writeFrame(black)
    
    '''
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
                else:
                    writeToAddr(gpuData[y][x],(((y << 4) & 0b1111110000) | (x & 0b1111)))
                #print(black[y,(x * 8) + bit], end='')
        #print()
        
    for line in gpuData:
        print(line)
    print("======================")
    '''
    
    if cv.waitKey(1) == ord('q'):
        break

if (len(sys.argv) >= 4):
    cap.release()
cv.destroyAllWindows()
