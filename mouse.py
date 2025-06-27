import pyautogui
import cv2
import mediapipe as mp
import math
import time

screenWidth, screenHeight = pyautogui.size()
mp_hands=mp.solutions.hands.Hands()
mp_drawing=mp.solutions.drawing_utils
camera=cv2.VideoCapture(0)

x1=x2=y1=y2=0
prev_mouse_x, prev_mouse_y = 0, 0
smoothening = 2
current_time=0
cooldown_time=0.7


while True:
    ret,image=camera.read()
    if not ret:
        break
    image=cv2.flip(image,1)
    resized_image=cv2.resize(image,(900,720))
    height,width,_=resized_image.shape
    
    rgb_image=cv2.cvtColor(resized_image,cv2.COLOR_BGR2RGB)
    capture_hands=mp_hands.process(rgb_image)
    all_hands=capture_hands.multi_hand_landmarks
    if all_hands:
        for hand in all_hands:
            mp_drawing.draw_landmarks(resized_image,hand)
            one_hand_landmark=hand.landmark


            for id,lm in enumerate(one_hand_landmark):
                x=int(lm.x*width)
                y=int(lm.y*height)
                
                if id==8:
                    mouse_x=int(screenWidth/width*x)
                    mouse_y=int(screenHeight/height*y)
                    cv2.circle(resized_image,(x,y),12,(0,255,0),2)
                    mouse_x = prev_mouse_x + (mouse_x - prev_mouse_x)//smoothening
                    mouse_y = prev_mouse_y + (mouse_y - prev_mouse_y)//smoothening
                    prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

                    pyautogui.moveTo(mouse_x,mouse_y)
                    x1=x
                    y1=y
                if id==4:
                    cv2.circle(resized_image,(x,y),12,(0,255,0),2)
               
                    x2=x
                    y2=y
            dist=math.sqrt((y2-y1)**2+(x2-x1)**2)
            print(dist)
            if dist<32 and (time.time()-current_time)>cooldown_time:
                pyautogui.click()
                current_time = time.time()
                

    cv2.imshow("hand_gesture_mouse",resized_image)
    key=cv2.waitKey(10)
    if key==27:
        break

cv2.destroyAllWindows()