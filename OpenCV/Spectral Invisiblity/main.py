import cv2 as cv
import numpy as np

# Initializing camera
cap = cv.VideoCapture(0)
bars = cv.namedWindow('Bars')

def hello():
    pass


cv.createTrackbar('upperHue', 'Bars', 110, 180, hello)
cv.createTrackbar('upperSaturation', 'Bars', 255, 255,hello)
cv.createTrackbar('upperValue', 'Bars', 255, 255, hello)
cv.createTrackbar('lowerHue', 'Bars', 68, 180, hello)
cv.createTrackbar('lowerSaturation', 'Bars', 55, 255, hello)
cv.createTrackbar('lowerValue', 'Bars', 54, 255, hello)


# Getting initial frame
while True:
    cv.waitKey(1000)
    ret, initial = cap.read()

    if (ret):
        break


# Capturing frames
while True:
    ret, frame = cap.read()

    # Converting to HSV format
    hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Getting the HSV values
    upper_hue = cv.getTrackbarPos('upperHue', 'Bars')
    lower_hue = cv.getTrackbarPos('lowerHue', 'Bars')
    upper_sat = cv.getTrackbarPos('upperSaturation', 'Bars')
    lower_sat = cv.getTrackbarPos('lowerSaturation', 'Bars')
    upper_value = cv.getTrackbarPos('upperValue', 'Bars')
    lower_value = cv.getTrackbarPos('lowerValue', 'Bars')

    # Dialating frame to reduce noise
    kernel = np.ones((3, 3), np.uint8)

    upper_hsv = np.array([upper_hue, upper_sat, upper_value])
    lower_hsv = np.array([lower_hue, lower_sat, lower_value])

    # Masking the color range
    mask = cv.inRange(hsv_frame, lower_hsv, upper_hsv)
    mask = cv.medianBlur(mask, 3)  # Removing impurities
    mask_inv = 255-mask
    mask = cv.dilate(mask, kernel, 5)

    # imposing the required frame on captured frame
    b = frame[:, :, 0]
    g = frame[:, :, 1]
    r = frame[:, :, 2]

    b = cv.bitwise_and(mask_inv, b)
    g = cv.bitwise_and(mask_inv, g)
    r = cv.bitwise_and(mask_inv, r)

    frame_inv = cv.merge((b, g, r))

    b = frame[:, :, 0]
    g = frame[:, :, 1]
    r = frame[:, :, 2]

    b = cv.bitwise_and(b, mask)
    g = cv.bitwise_and(g, mask)
    r = cv.bitwise_and(r, mask)

    blanket_surface = cv.merge((b, g, r))
    result = cv.bitwise_or(frame_inv, blanket_surface)

    cv.imshow('Cloak', result)
    cv.imshow('Original', frame)

    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
