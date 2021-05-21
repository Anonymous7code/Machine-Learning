import cv2 as cv
import pytesseract as pt
from PIL import ImageGrab
from win32api import GetSystemMetrics
import numpy as np
import googletrans

pt.pytesseract.tesseract_cmd = 'G:\\SOFTS\\Teseract-ocr\\tesseract.exe'
screenH = 1080
screenW = 1920
# img = cv.imread('hey.jpg')
# img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
trans = googletrans.Translator()


def detecting_char(img):
    # detecting characters
    hImg, wImg, _ = img.shape
    boxes = pt.image_to_boxes(img)

    for b in boxes.splitlines():
        b = b.split(' ')
        # print(b)
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv.rectangle(img, (x, hImg - y), (w, hImg-h), (0, 255, 0), 2)
        cv.putText(img, b[0], (x, hImg-y+25),
                   cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


def detecting_words(img):
    # detecting characters
    hImg, wImg, _ = img.shape
    boxes = pt.image_to_data(img)
    # print(boxes)
    for x, b in enumerate(boxes.splitlines()):
        if x != 0:
            b = b.split()
            # print(b)
            if len(b) == 12:
                x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
                cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), -1)
                print(b[11])
                # translated = trans.translate(str(b[11]), dest='hi')

                
                cv.putText(img, b[11], (x, y-25),
                           cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


# cap = cv.VideoCapture(0)

while True:
    img = ImageGrab.grab(bbox=(0, 0, screenW, screenH))
    imgToArray = np.array(img)
    img = cv.cvtColor(imgToArray, cv.COLOR_BGR2RGB)

    # ret, frame = cap.read()
    detecting_words(img)

    cv.imshow('screen', img)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

# cap.release()
cv.DestroyAllWindows()
