import cv2 as cv
import numpy as np

def nothing(x):
    pass
cap= cv.VideoCapture('pranay1.avi')
fourcc= cv.VideoWriter_fourcc('X', 'V', 'I', 'D')
out= cv.VideoWriter('final1.avi', fourcc, 20.0, (640,480) )
#cv.namedWindow('Tracking')
#cv.createTrackbar('l_h', 'Tracking', 0, 255, nothing)
#cv.createTrackbar('l_s', 'Tracking', 0, 255, nothing)
#cv.createTrackbar('l_v', 'Tracking', 0, 255, nothing)
#cv.createTrackbar('u_h', 'Tracking', 255, 255, nothing)
#cv.createTrackbar('u_s', 'Tracking', 255, 255, nothing)
#cv.createTrackbar('u_v', 'Tracking', 255, 255, nothing)
while(True):
    ret, frame= cap.read()
    frame= cv.resize(frame, (640,480))
    hsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    #lh = cv.getTrackbarPos('l_h', 'Tracking')
    #ls = cv.getTrackbarPos('l_s', 'Tracking')
    #lv = cv.getTrackbarPos('l_v', 'Tracking')
    #uh = cv.getTrackbarPos('u_h', 'Tracking')
    #us = cv.getTrackbarPos('u_s', 'Tracking')
    #uv = cv.getTrackbarPos('u_v', 'Tracking')
    lh= 82
    ls= 51
    lv= 51
    uh= 133
    us= 255
    uv= 255
    lhb= 0
    lsb= 0
    lvb= 0
    uhb= 255
    usb= 255
    uvb= 0
    lbb= np.array([lhb, lsb, lvb])
    ubb= np.array([uhb, usb, uvb])
    lb= np.array([lh,ls,lv])
    ub= np.array([uh,us,uv])
    backg= cv.imread('pranay42.JPG')
    backg= cv.resize(backg, (640,480))
    mask= cv.inRange(hsv, lb, ub)
    masknot= cv.bitwise_not(mask)
    res= cv.bitwise_and(frame, frame, mask = masknot)
    a= cv.bitwise_and(backg, backg, mask=mask)
    fres= cv.addWeighted(res,1,a,1,1)
    cv.imshow('frame', frame)
    cv.imshow('fres', fres)
    key= cv.waitKey(1)
    if ret==True:
        out.write(fres)
    if key == 27:
        break
cap.release()
cv.destroyAllWindows()
