# -*- coding: utf-8 -*-
"""
Created on Sat May 12 16:00:00 2018

@author: Fulvio Bertolini
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May  3 19:15:41 2018

@author: Fulvio Bertolini
"""

import socket
import cv2
import os
import numpy as np

# zed intrinsic parameters
cameraMatrix_ZED = np.zeros((3,3), np.float64)
cameraMatrix_ZED[0,0] = 660.445
cameraMatrix_ZED[0,2] = 650.905
cameraMatrix_ZED[1,1] = 660.579
cameraMatrix_ZED[1,2] = 327.352
cameraMatrix_ZED[2,2] = 1

distCoeff_ZED = np.zeros((1,5), np.float64)
distCoeff_ZED[0,0] = -0.00174692
distCoeff_ZED[0,1] = -0.0174969	
distCoeff_ZED[0,2] = -0.000182398
distCoeff_ZED[0,3] = -0.00751098
distCoeff_ZED[0,4] =  0.0219687

# iphone intrinsic parameters
cameraMatrix_iPhone = np.zeros((3,3), np.float64)
cameraMatrix_iPhone[0,0] = 3513.23
cameraMatrix_iPhone[0,2] = 1542.31
cameraMatrix_iPhone[1,1] = 3519.98
cameraMatrix_iPhone[1,2] = 2089.89
cameraMatrix_iPhone[2,2] = 1

distCoeff_iPhone = np.zeros((1,5), np.float64)
distCoeff_iPhone[0,0] = 0.293461	
distCoeff_iPhone[0,1] = -1.3054	
distCoeff_iPhone[0,2] = 0.0132138	
distCoeff_iPhone[0,3] = 0.00104743
distCoeff_iPhone[0,4] = 2.50754


ZEDCam_2_Chkb = np.zeros((4,4), np.float)
iPhoneCam_2_Chkb = np.zeros((4,4), np.float)
Chkb_2_ZEDCam = np.zeros((4,4), np.float)
Chkb_2_iPhoneCam = np.zeros((4,4), np.float)


def getCameraExtrinsic(images, mtx, dist):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*9,3), np.float32)
    objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
    objp = np.multiply(objp, 0.0246)
    
   
   
    tvecs = []
    rvecs = [] 
    
    
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
    
        # If found, add object points, image points (after refining them)
        if ret == True:
            
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
            
            _, rvec, tvec, inliers = cv2.solvePnPRansac(objp,corners2, mtx, dist)
            rvecs.append(rvec)
            tvecs.append(tvec)
            
            cv2.namedWindow("img", cv2.WINDOW_NORMAL )        # Create window with freedom of dimensions
            cv2.resizeWindow("img", 2400, 1200)              # Resize window to specified dimensions
    
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,6), corners,ret)
            cv2.imshow('img',img)
            cv2.waitKey(10)
    
    cv2.destroyAllWindows()
    
    
    return (rvecs, tvecs)

def getCameraMatrix(rvec, tvec):
    Cam_2_Chkb = np.zeros((4,4), np.float)
    Chkb_2_Cam = np.zeros((4,4), np.float)
    
    
    rotM_Chkb_2_Cam = cv2.Rodrigues(rvec)[0]
    
    Chkb_2_Cam[0:3, 0:3] = rotM_Chkb_2_Cam
    Chkb_2_Cam[0:3, 3] = tvec.ravel()
    Chkb_2_Cam[3,3] = 1
    
    Cam_2_Chkb = np.linalg.inv(Chkb_2_Cam)
    
    
    return Cam_2_Chkb, Chkb_2_Cam
    
    
    
    
    
    
def writeMatrix(matrix):
    
    string:str = ""
    for i in range(0,matrix.shape[0]):
        for j in range(0,matrix.shape[1]):
            string += "{:.9f}".format(matrix[i,j])
            if(j != 3):
                string += "="
        if(i != 3):
                string += "!"
    
    return string


def Main(ip, port, sessionPath):
    
    s = socket.socket()
    s.bind((ip,port))
    s.listen(1)
    print("listening")
    c, addr = s.accept()
    print ("Connection from: " + str(addr))
    
    receivedData = c.recv(16777216)
    
    
    #receivedData =  np.asarray(bytearray(receivedData), dtype=np.uint8)
    x = np.frombuffer(receivedData, dtype='uint8')
    
    #decode the array into an image
    img = cv2.imdecode(x, 1)
    
    cv2.imwrite(sessionPath + 'ZED/checkerBoard.png', img)
    
    image_ZED = [sessionPath + "ZED/checkerBoard.png"]
    image_iPhone = [sessionPath + "iPhone/checkerBoard.png"]

    # get extrinsics iPhone and  ZED
    rvecs_ZED, tvecs_ZED = getCameraExtrinsic(image_ZED, cameraMatrix_ZED, distCoeff_ZED)
    rvecs_iPhone, tvecs_iPhone = getCameraExtrinsic(image_iPhone, cameraMatrix_iPhone, distCoeff_iPhone)
    
    
    # get single camera2checkerboard matrices
    ZEDCam_2_Chkb[:,:], Chkb_2_ZEDCam[:,:] = getCameraMatrix(rvecs_ZED[0], tvecs_ZED[0])
    iPhoneCam_2_Chkb[:,:], Chkb_2_iPhoneCam[:,:] = getCameraMatrix(rvecs_iPhone[0], tvecs_iPhone[0])
    
    # get matrix from iPhone to Zed
    iPhoneCam_2_ZEDCam = np.matmul(Chkb_2_ZEDCam[:,:], iPhoneCam_2_Chkb[:,:])

    # encode the matrix in string
    iPhoneCam_2_ZEDCam_matrix_string = writeMatrix(iPhoneCam_2_ZEDCam)
   
    
    # read the other strings from file:
    #    1) ARKitWorld_2_ARKitCam
    #    1) azimuth and zenith angles
    arkitMatrixFile = open(sessionPath + "iPhone/ARKitWorld_2_ARKitCam.txt", "r")
    arkitMatrixString = arkitMatrixFile.readlines()
    arkitMatrixFile.close()
    
    
    anglesFile = open(sessionPath + "iPhone/Zenith_Azimuth.txt", "r")
    anglesString = anglesFile.readlines()
    anglesFile.close()
    
    
    sendDataEncoded = (iPhoneCam_2_ZEDCam_matrix_string + "?" + arkitMatrixString[0] +"?" + anglesString[0]).encode('utf-8')
    c.send(sendDataEncoded)
        
    #c.close()
    #s.shutdown(socket.SHUT_RDWR)
    s.close()

if __name__ == '__main__':
   


   
    ipHost = "127.0.0.1"
    portHost = 5001
    
    sessionID = input("Enter session ID: ")
    imgPath = "../Sessions/" + sessionID + "/"
    if os.path.exists(imgPath):
        os.makedirs(imgPath + "ZED/")
        Main(ipHost, portHost, imgPath)
    else:
        print("Directory with session ID doesn't exist!")
    
    

