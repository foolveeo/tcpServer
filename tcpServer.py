import socket
from sunposition import sunpos
from datetime import datetime
import os


   
def Main(ip, port, sessionID): 
    
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
        matrixStr, gpsStr = receivedDataStr.split('?')
        
        fileTxt = open(sessionID + "ARKitWorld_2_ARKitCam.txt", "a+")
        fileTxt.write(matrixStr)
        fileTxt.close()
        
        lat, lon, alt, horAcc, timeStamp = gpsStr.split("!")
        time = datetime.utcnow()
        az, zen, ra, dec, h = sunpos(time,float(lat),float(lon),float(alt))
        
        sunPosStr = str(az) + "!" + str(zen)
        fileTxt = open(sessionID + "Zenith_Azimuth.txt", "a+")
        fileTxt.write(sunPosStr)
        fileTxt.close()
        
        fileTxt = open(sessionID + "GPS_Coord.txt", "a+")
        fileTxt.write("latitude: " + lat + "\nlongitude: " + lon +  "\naltitude: " + alt + "\nhorizontal accuracy: " + horAcc + "\ntime stamp: " + timeStamp)
        fileTxt.close()
        
        print("from connected user:\n" + receivedDataStr)
        break
    
    s.close()
    print("shut down")

if __name__ == '__main__':
    ipHost = "172.20.10.2"
    portHost = 5004
    
    sessionID = input("Enter session ID: ")
    imgPath = "../Sessions/" + sessionID + "/"
    if not os.path.exists(imgPath):
        os.makedirs(imgPath)
        os.makedirs(imgPath + "iPhone/")
        Main(ipHost, portHost, imgPath + "iPhone/")
    else:
        print("Directory with same session ID already exist!")
