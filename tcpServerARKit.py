# -*- coding: utf-8 -*-
"""
Created on Thu May  3 19:15:25 2018

@author: Fulvio Bertolini
"""

import socket
import numpy as np
import os
import cv2


def Main(ip, port,sessionPath):
    
    s = socket.socket()
    s.bind((ip,port))
    s.listen(1)
    print("listening")
    c, addr = s.accept()
    print ("Connection from: " + str(addr))
    while 1:
        receivedData = c.recv(16777216)
    
        x = np.frombuffer(receivedData, dtype='uint8')
        
        #decode the array into an image
        img = cv2.imdecode(x, 1)
        imgTransposed = np.zeros((img.shape[1], img.shape[0]), np.uint8)
        
        imgTransposed = cv2.transpose(img);
        imgTransposed = cv2.flip(imgTransposed, 0);
        cv2.imwrite(sessionPath + 'checkerBoard.png', imgTransposed)
    
    
    s.close()
    print("shut down")


if __name__ == '__main__':
   


   
    ipHost = "172.20.10.2"
    portHost = 5005
    
    sessionID = input("Enter session ID: ")
    imgPath = "../Sessions/" + sessionID + "/"
    if os.path.exists(imgPath + "iPhone/"):
        Main(ipHost, portHost, imgPath  + "iPhone/")
    else:
        print("Directory with session ID doesn't exist!")
    
   