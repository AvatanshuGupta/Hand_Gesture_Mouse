import pyautogui
import cv2
import mediapipe

camera=cv2.VideoCapture(0)
while True:
    ret,image=camera.read()
    image=cv2.flip(image,1)
    cv2.imshow("hand_gesture_mouse",image)
    key=cv2.waitKey(200)
    if key==27:
        break