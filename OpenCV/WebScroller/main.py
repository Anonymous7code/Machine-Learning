import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

# Define upper and lower bound for color range
blue_lower = np.array([100, 150, 0], np.uint8)
blue_upper = np.array([140, 255, 255], np.uint8)

while True:
    ret, frame = cap.read()

    # BGR --> HSV 
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Masking for detection of upper and lower bound
    mask = cv.inRange(hsv, blue_lower, blue_upper)
    

    cv.imshow('MASK', mask)
    cv.imshow('Frame', frame)

    if cv.waitKey(10) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
