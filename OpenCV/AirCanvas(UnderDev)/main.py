# Importing libraries
import numpy as np
import cv2 as cv
from collections import deque

# default called trackbar function


def setValues(x):
    pass


def set_res(cap, x, y):
    cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, int(x))
    cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, int(y))
    return str(cap.get(cv.CV_CAP_PROP_FRAME_WIDTH)), str(cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))


# Creating the trackbars needed for adjusting the marker colour
cv.namedWindow("Color detectors")
cv.createTrackbar("Upper Hue", "Color detectors", 153, 180, setValues)
cv.createTrackbar("Upper Saturation", "Color detectors", 255, 255, setValues)
cv.createTrackbar("Upper Value", "Color detectors", 255, 255, setValues)
cv.createTrackbar("Lower Hue", "Color detectors", 64, 180, setValues)
cv.createTrackbar("Lower Saturation", "Color detectors", 72, 255, setValues)
cv.createTrackbar("Lower Value", "Color detectors", 49, 255, setValues)


# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
blpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0
black_index = 0

# The kernel to be used for dilation purpose
kernel = np.ones((7, 7), np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (0, 0, 0)]
colorIndex = 0

# Here is code for Canvas setup
paintWindow = np.zeros((720, 1280, 3)) + 255
paintWindow = cv.rectangle(paintWindow, (40, 1), (140, 65), (0, 0, 0), 2)
paintWindow = cv.rectangle(paintWindow, (160, 1), (255, 65), colors[0], -1)
paintWindow = cv.rectangle(paintWindow, (275, 1), (370, 65), colors[1], -1)
paintWindow = cv.rectangle(paintWindow, (390, 1), (485, 65), colors[2], -1)
paintWindow = cv.rectangle(paintWindow, (505, 1), (600, 65), colors[3], -1)
paintWindow = cv.rectangle(paintWindow, (620, 1), (720, 65), colors[4], -1)

cv.putText(paintWindow, "CLEAR", (49, 33),
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv.LINE_AA)
cv.putText(paintWindow, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX,
           0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(paintWindow, "GREEN", (298, 33),
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(paintWindow, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX,
           0.5, (255, 255, 255), 2, cv.LINE_AA)
cv.putText(paintWindow, "YELLOW", (520, 33),
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1, cv.LINE_AA)
cv.putText(paintWindow, "BLACK", (640, 33),
           cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv.LINE_AA)
cv.namedWindow('Paint', cv.WINDOW_AUTOSIZE)


# Loading the default webcam of PC.
cap = cv.VideoCapture(0)



# width = cap.get(3)  # float `width`
# height = cap.get(4)

# print(height)
# print(width)
# Keep looping
while True:
    # Reading the frame from the camera
    cap.set(3, 1280)
    cap.set(4, 720)
    ret, frame = cap.read()
    frame = cv.rotate(frame, cv.ROTATE_90_COUNTERCLOCKWISE)
    # width = cap.get(3)  # float `width`
    # height = cap.get(4)

    # print(height)
    # print(width)
    # Flipping the frame to see same side of yours
    frame = cv.flip(frame, 1)
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    u_hue = cv.getTrackbarPos("Upper Hue", "Color detectors")
    u_saturation = cv.getTrackbarPos("Upper Saturation", "Color detectors")
    u_value = cv.getTrackbarPos("Upper Value", "Color detectors")
    l_hue = cv.getTrackbarPos("Lower Hue", "Color detectors")
    l_saturation = cv.getTrackbarPos("Lower Saturation", "Color detectors")
    l_value = cv.getTrackbarPos("Lower Value", "Color detectors")
    Upper_hsv = np.array([u_hue, u_saturation, u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])

    # Adding the colour buttons to the live frame for colour access
    frame = cv.rectangle(frame, (40, 1), (140, 65), (122, 122, 122), -1)
    frame = cv.rectangle(frame, (160, 1), (255, 65), colors[0], -1)
    frame = cv.rectangle(frame, (275, 1), (370, 65), colors[1], -1)
    frame = cv.rectangle(frame, (390, 1), (485, 65), colors[2], -1)
    frame = cv.rectangle(frame, (505, 1), (600, 65), colors[3], -1)
    frame = cv.rectangle(frame, (620, 1), (720, 65), colors[4], -1)
    cv.putText(frame, "CLEAR ALL", (49, 33),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv.LINE_AA)
    cv.putText(frame, "BLUE", (185, 33), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(frame, "GREEN", (298, 33), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(frame, "RED", (420, 33), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)
    cv.putText(frame, "YELLOW", (520, 33), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (150, 150, 150), 1, cv.LINE_AA)
    cv.putText(frame, "BALCK", (640, 33), cv.FONT_HERSHEY_SIMPLEX,
               0.5, (255, 255, 255), 1, cv.LINE_AA)

    # Identifying the pointer by making its mask
    Mask = cv.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv.erode(Mask, kernel, iterations=1)
    Mask = cv.morphologyEx(Mask, cv.MORPH_OPEN, kernel)
    Mask = cv.dilate(Mask, kernel, iterations=1)

    # Find contours for the pointer after idetifying it
    cnts, _ = cv.findContours(Mask.copy(), cv.RETR_EXTERNAL,
                              cv.CHAIN_APPROX_SIMPLE)
    center = None

    # Ifthe contours are formed
    if len(cnts) > 0:
        # sorting the contours to find biggest
        cnt = sorted(cnts, key=cv.contourArea, reverse=True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Calculating the center of the detected contour
        M = cv.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

        # Now checking if the user wants to click on any button above the screen
        if center[1] <= 65:
            if 40 <= center[0] <= 140:  # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
                blpoints = [deque(maxlen=512)]

                blue_index = 0
                black_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0

                paintWindow[67:, :, :] = 255
            elif 160 <= center[0] <= 255:
                colorIndex = 0  # Blue
            elif 275 <= center[0] <= 370:
                colorIndex = 1  # Green
            elif 390 <= center[0] <= 485:
                colorIndex = 2  # Red
            elif 505 <= center[0] <= 600:
                colorIndex = 3  # Yellow
            elif 620 <= center[0] <= 720:
                colorIndex = 4  # Black
        else:
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
            elif colorIndex == 4:
                blpoints[black_index].appendleft(center)
    # Append the next deques when nothing is detected to avois messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1
        blpoints.append(deque(maxlen=512))
        black_index += 1

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints, blpoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv.line(frame, points[i][j][k - 1],
                        points[i][j][k], colors[i], 2)
                cv.line(paintWindow, points[i][j]
                        [k - 1], points[i][j][k], colors[i], 2)

    # Show all the windows
    cv.imshow("Tracking", frame)
    # cv.imshow("Paint", paintWindow)
    # cv.imshow("mask", Mask)

    # If the 'q' key is pressed then stop the application
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and all resources
cap.release()
cv.destroyAllWindows()
