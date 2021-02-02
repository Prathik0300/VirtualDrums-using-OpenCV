'''
Project : VirtualDrums uisng OpenCV(in python)
Author: Prathik Pugazhenthi
MIT License
'''
import cv2 as cv
import numpy as np

def Empty(x):
    pass
def caliberation():
    video = cv.VideoCapture(0)
    Lower,Upper =[],[]

    #creation of a named window with different trackbars to caliberate the required stick of our choice.
    '''
    L_HSV --> Lower HSV
    L_SAT --> Lower Saturation
    L_VAL --> Lower Value
    U_HSV --> Upper HSV
    U_SAT --> Upper Saturation
    U_VAL --> Upper Value
    '''
    window = cv.namedWindow("Caliberation")
    L_HSV = cv.createTrackbar("L_HSV","Caliberation",0,179,Empty)
    L_SAT = cv.createTrackbar("L_SAT","Caliberation",0,255,Empty)
    L_VAL = cv.createTrackbar("L_VAL","Caliberation",0,255,Empty)

    U_HSV = cv.createTrackbar("U_HSV","Caliberation",0,179,Empty)
    U_SAT = cv.createTrackbar("U_SAT","Caliberation",0,255,Empty)
    U_VAL = cv.createTrackbar("U_VAL","Caliberation",0,255,Empty)

    # the default position of the Upper values would be set at max value of each trackbar
    U_HSV = cv.setTrackbarPos("U_HSV","Caliberation",179)
    U_SAT = cv.setTrackbarPos("U_SAT","Caliberation",255)
    U_VAL = cv.setTrackbarPos("U_VAL","Caliberation",255)

    while cv.waitKey(1)==-1:
        ret,frame = video.read()
        frame=cv.flip(frame,1)
        cv.imshow("Frame",frame)
        hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

        #getting the trackbar value based on the position of the pointer in trackbar.
        l_hsv = cv.getTrackbarPos("L_HSV","Caliberation")
        l_sat = cv.getTrackbarPos("L_SAT","Caliberation")
        l_val = cv.getTrackbarPos("L_VAL","Caliberation")

        u_hsv = cv.getTrackbarPos("U_HSV","Caliberation")
        u_sat = cv.getTrackbarPos("U_SAT","Caliberation")
        u_val = cv.getTrackbarPos("U_VAL","Caliberation")

        Lower = np.array([l_hsv,l_sat,l_val])
        Upper = np.array([u_hsv,u_sat,u_val])

        mask = cv.inRange(hsv,Lower,Upper)
        cv.imshow("Mask",mask)
    video.release()
    cv.destroyAllWindows()

    #return the list of Lower and Upper values of the image which will be used to create a mask and track the object.
    return Lower,Upper
if __name__ == '__main__':
    print(caliberation())
    
