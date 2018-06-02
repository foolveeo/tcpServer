# -*- coding: utf-8 -*-
"""
Created on Thu May  3 19:15:41 2018

@author: Fulvio Bertolini
"""

import socket
import os
   
def Main(ip, port):
    
    s = socket.socket()
    s.bind((ip,port))
    s.listen(1)
    print("listening")
    c, addr = s.accept()
    print ("Connection from: " + str(addr))
    while 1:
        receivedData = c.recv(1024)
        if not receivedData:
            break
        receivedDataStr = receivedData.decode('utf-8')
        if(receivedDataStr == "stop"):
            print("stopping...")
            break
        
        print("from connected user:\n" + receivedDataStr)
        
        fileARMatix =  open("./ARKitWorld_2_ARKitCam.txt", "r")
        linesARMatrix = fileARMatix.readlines()
        fileARMatix.close()
        fileAR2ZEDMatrix =  open("./ARKitCam_2_ZEDCam.txt", "r")
        linesAR2ZEDMatrix = fileAR2ZEDMatrix.readlines()
        fileAR2ZEDMatrix.close()
        
        sendDataARMatrix = linesARMatrix[-1]
        sendDataAR2ZEDMatrix = linesAR2ZEDMatrix[-1]
        sendDataString = sendDataARMatrix + "?" + sendDataAR2ZEDMatrix
        sendDataEncoded = (sendDataString).encode('utf-8')
        c.send(sendDataEncoded)
        #c.close()
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    print("shut down")

if __name__ == '__main__':
   
    ipHost = "127.0.0.1"
    portHost = 5001
    sessionID = input("Enter session ID: ")
    imgPath = "../Sessions/" + sessionID + "/"
    if os.path.exists(imgPath + "iPhone/"):
        Main(ipHost, portHost, imgPath  + "iPhone/")
    else:
        print("Directory with session ID doesn't exist!")
    Main(ipHost, portHost)

