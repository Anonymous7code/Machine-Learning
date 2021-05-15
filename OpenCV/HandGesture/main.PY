import cv2 as cv
import time
import numpy as np
import handdetecting as hd

wcap, hcap = 1280, 720
present_time = 0
cap = cv.VideoCapture(0)
cap.set(3, wcap)
cap.set(4, hcap)

detector = hd.handDetector(detectionCon=0.8)
while True:
    ret, frame = cap.read()
    frame = detector.findHands(frame)

    current_time = time.time()
    fps = 1/(current_time-present_time)
    present_time = current_time

    cv.putText(frame, f'FPS :{int(fps)}', (20, 30),
               cv.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
    cv.imshow('Frame', frame)

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
