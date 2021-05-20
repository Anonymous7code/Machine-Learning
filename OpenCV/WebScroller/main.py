import cv2 as cv
import numpy as np
import pyautogui as pg

cap = cv.VideoCapture(0)
# w= cap.set(3, 1280)
# h =cap.set(4, 720)
# Define upper and lower bound for color range
blue_lower = np.array([100, 150, 0], np.uint8)
blue_upper = np.array([140, 255, 255], np.uint8)

prev_y = 0

while True:
    ret, frame = cap.read()

    # BGR --> HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Masking for detection of upper and lower bound
    mask = cv.inRange(hsv, blue_lower, blue_upper)
    # Detecting and drawing contour over frame
    contours, hirearchy = cv.findContours(
        mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # Removing the noise from contour and drawing major color presence  area
    for c in contours:
        area = cv.contourArea(c)
        # print(area)
        if area > 500:
            # cv.drawContours(frame,contours,-1,(0,255,0),2)
            # Drawing rectangle for detected surface
            x, y, w, h = cv.boundingRect(c)
            cv.rectangle(frame, (x, y), ((x+w//2), (y+h//2)), (0, 255, 0), 2)
            if y < prev_y:
                # print('Moving Down')
                pg.press('space')
            prev_y = y

    # cv.imshow('MASK', mask)
    cv.imshow('Frame', frame)

    if cv.waitKey(10) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
