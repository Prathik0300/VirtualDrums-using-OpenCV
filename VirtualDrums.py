'''
Project : Virtual Drums using OpenCV (Python)
Author : Prathik Pugazhenthi

This project use OpenCV to create a virtual drum set. It uses color detection in a region of interest
and plays the corresponding drum beat wrt the speed of the sticks moved between co-ordinates which represents the intensity of the sound. the sticks can be of any color and there is no requirement of sticks to be of the same color but the sticks should be colored. after caliberating the sticks the frame would show a green line which denotes the start of the drum region below it. 

Left Side: High
Right Side: Snare
'''

#importing necessary libraries
import cv2 as cv
import numpy as np
from caliberation import caliberation as calib
from pygame import mixer
import time
import math

# CalcSpeed function is used to find the intensity with which the sound would be played. when the sticks are hit hard then the sticks would be moved between the co-ordinates with a greater speed and vice versa. based on the speed of the movement of the stick,the intensity would vary.
def CalcSpeed(start,new_y,old_y,new_x,old_x):
    end = time.time()
    time_diff = end-start
    diff_x = abs(new_x-old_x)
    diff_y = abs(new_y-old_y)
    distance = math.sqrt(diff_x**2 + diff_y**2)
    try:
        speed = distance/time_diff
    except:
        speed = 0
    if speed<2:
        return 0
    elif speed<4:
        return 1
    return 2

#Caliberation of the both left and right sticks (the sticks can be of any color and it is not necessary that both sticks should be of same color)
lower_right,upper_right = calib()
lower_left,upper_left = calib()

#initialization of the mixer library. this is responsible to play the sound files which will play after we give the path to the sound tracks.(line 32-38)
mixer.init()
drum_high1 = mixer.Sound("./sounds/high_hat_1.ogg")
drum_high2 = mixer.Sound("./sounds/high_hat_2.wav")
drum_high3 = mixer.Sound("./sounds/high_hat_3.wav")
drum_snare1 = mixer.Sound("./sounds/snare_1.wav")
drum_snare2 = mixer.Sound("./sounds/snare_2.wav")

#dictionary with different drum sounds as value and the corresponding key will be generated through the CalcSpeed function which will decide the index based on the speed of the stick moved between the co-ordinates.
drum_snare_dict = {0:drum_snare1,1:drum_snare2}
drum_high_dict = {0:drum_high1,1:drum_high2,2:drum_high3}

video = cv.VideoCapture(0)

#initialization of the (x,y) co-ordinates for both left and right sticks
old_left_bottom =-1
old_right_bottom =-1
old_left_x=-1
old_right_x=-1

while cv.waitKey(1)==-1:
    ret,frame = video.read()
    frame = cv.flip(frame,1)

    #mid_point will be required to segment the frame into two parts and playing the drum_high and drum_snare respectively based on the side of the frame where stick is placed
    mid_point_x,mid_point_y = frame.shape[0]//2,frame.shape[1]//2

    hsv = cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    #individual masks for the left and right sticks using the caliberated value done in the first step 
    mask_left = cv.inRange(hsv,np.array(lower_left),np.array(upper_left))
    mask_right = cv.inRange(hsv,np.array(lower_right),np.array(upper_right))

    kernel = np.ones((5,5),np.uint8)
    start_time=time.time()
    erode_left = cv.erode(mask_left,kernel,iterations=1)
    erode_right = cv.erode(mask_right,kernel,iterations=1)
    contour_left,_ = cv.findContours(erode_left,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    contour_right,_= cv.findContours(erode_right,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    
    #this is for the left stick
    if contour_left:
        c = max(contour_left,key=cv.contourArea)
        x,y,w,h = cv.boundingRect(c)
        cnt_mid_point_left = (x+w//2,y+h//2)

        #if the left stick is in the left part of the frame
        if x < mid_point_x or cnt_mid_point_left[0] <mid_point_x:

            #if the old position of the stick is -1 i.e either it was out of the frame for some time or it is coming in the frame for the first time
            
            if old_left_bottom==-1:
                old_left_bottom = y+h
                old_left_x = x+w//2
            
            #if the stick was already in frame and is entering into the zone of drums

            elif old_left_bottom<360 and y+h>360:

                #calculating the speed of the stick moved through the co-ordinates i.e old_position and new_position which is denoted by (x,y,w,h)
                x = CalcSpeed(start_time,y+h,old_left_bottom,x+w//2,old_left_x)

                #the CalcSpeed returns an integer which is related to the range of speed of the stick and that integer will be used as an index to play the required sound from the dictionaries.
                try:
                    drum_high_dict[x].play()
                except:
                    drum_high_dict[2].play()
                time.sleep(0.01)
                old_left_bottom=y+h
                old_left_x=x+w//2

        #if the left stick is in the right part of the frame
        elif x > mid_point_x or cnt_mid_point_left[0] > mid_point_x:

            #if the old position of the stick is -1 i.e either it was out of the frame for some time or it is coming in the frame for the first time

            if old_left_bottom==-1:
                old_left_bottom=y+h
                old_left_x = x+w//2
            
            #if the stick was already in frame and is entering into the zone of drums

            elif old_left_bottom<360 and y+h>360:

                #calculating the speed of the stick moved through the co-ordinates i.e old_position and new_position which is denoted by (x,y,w,h)
                x = CalcSpeed(start_time,y+h,old_left_bottom,x+w//2,old_left_x)

                #the CalcSpeed returns an integer which is related to the range of speed of the stick and that integer will be used as an index to play the required sound from the dictionaries.
                try:
                    drum_snare_dict[x].play()
                except:
                    drum_snare_dict[1].play()
                time.sleep(0.01)
                old_left_bottom = y+h
                old_left_x=x+w//2

    #if there are no contours found i.e. the stick is out of frame then the position of the stick would be set to -1 again

    else:
        old_left_bottom=-1
        old_left_x=-1
    
    #this is for the right stick

    if contour_right:
        c = max(contour_right,key=cv.contourArea)
        x,y,w,h = cv.boundingRect(c)
        cnt_mid_point_right = (x+w//2,y+h//2)

        #if the right stick is in the left part of the frame

        if x < mid_point_x or cnt_mid_point_right[0] < mid_point_x:

            #if the old position of the stick is -1 i.e either it was out of the frame for some time or it is coming in the frame for the first time

            if old_right_bottom==-1:
                old_right_bottom = y+h
                old_right_x = x+w//2

            #if the stick was already in frame and is entering into the zone of drums

            elif old_right_bottom<360 and y+h>360:

                #calculating the speed of the stick moved through the co-ordinates i.e old_position and new_position which is denoted by (x,y,w,h)

                x = CalcSpeed(start_time,y+h,old_right_bottom,x+w//2,old_right_x)

                #the CalcSpeed returns an integer which is related to the range of speed of the stick and that integer will be used as an index to play the required sound from the dictionaries.
                try:
                    drum_high_dict[x].play()
                except:
                    drum_high_dict[2].play()
                time.sleep(0.01)
                old_right_bottom=y+h
                old_right_x = x+w//2
            
            #if the right stick is in the right part of the frame

        elif x > mid_point_x or cnt_mid_point_right[0] > mid_point_x:

            #if the old position of the stick is -1 i.e either it was out of the frame for some time or it is coming in the frame for the first time

            if old_right_bottom==-1:
                old_right_bottom=y+h
                old_right_x = x+w//2

            #if the stick was already in frame and is entering into the zone of drums

            elif old_right_bottom<360 and y+h>360:

                #calculating the speed of the stick moved through the co-ordinates i.e old_position and new_position which is denoted by (x,y,w,h)
                x = CalcSpeed(start_time,y+h,old_right_bottom,x+w//2,old_right_x)

                #the CalcSpeed returns an integer which is related to the range of speed of the stick and that integer will be used as an index to play the required sound from the dictionaries.
                try:
                    drum_snare_dict[x].play()
                except:
                    drum_snare_dict[1].play()
                time.sleep(0.01)
                old_right_bottom = y+h
                old_right_x = x+w//2

    #if there are no contours found i.e. the stick is out of frame then the position of the stick would be set to -1 again

    else:
        old_right_bottom=-1
        old_right_x = -1

    #printing a green line in the frame so that the user gets to know the point after which the stick would be tracked and the sound would be played
    cv.line(frame,(0,360),(800,360),(0,255,0),2)
    cv.imshow("frame",frame)
video.release()
cv.destroyAllWindows()