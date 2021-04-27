# Importing Libraries

import matplotlib.pylab as plt
import cv2
import numpy as np


# function to mask

def region_of_interest(img, vertices):
    """Plots region of intrest

    Args:
        img (image): the target image to be masked
        vertices (array): the vertices to exclude during masking
    """

    mask = np.zeros_like(img)

    #channel_count = img.shape[2]
    # Use "(255,)*channel_count" insted of "(255)" if masking is applied to three channel image
    # Also Comment out the above line

    match_mask_color = 255
    cv2.fillPoly(mask, vertices, match_mask_color)          # filling the mask

    # returning masked img with region of intrest
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def drow_the_lines(img, lines):
    """Drawing lines on input image

    Args:
        img (image): The input image
        lines (vectors): Obtained from HOUGH TRANSFORM

    Returns:
        image: the image with lines marked
    """

    img = np.copy(img)  # making the copy of image
    # creating the image of same size as input image

    blank_image = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)

    for line in lines:          # looping through all the line vector obtained by HoughLine()
        for x1, y1, x2, y2 in line:
            cv2.line(blank_image, (x1, y1), (x2, y2),
                     (0, 255, 0), thickness=10)

    # Superimposing the blank image on original image
    img = cv2.addWeighted(img, 0.8, blank_image, 1, 0.0)
    return img

# Used for static image
# image = cv2.imread('Screenshot (19).png')
# Converting to RGB format
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def process(image):
    """Input image is marked with lines

    Args:
        image (image): The input image to be detected

    Returns:
        image: the output marked image
    """

    # print(image.shape)
    # Height and width may
    # differ based on size of input frame,here(1920,1080)
    height = image.shape[0]
    width = image.shape[1]
    # Definning the vertices for region of intrest based on initial frame plotted on screen
    # Change the vertices value when the frame of offset or the required region is different from the
    # used input.
    region_of_interest_vertices = [
        (0, height),
        (width/2, height/2),
        (width, height)
    ]
    # converting to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # Using Canny to detect edge
    canny_image = cv2.Canny(gray_image, 100, 200)
    cropped_image = region_of_interest(canny_image,
                                       np.array([region_of_interest_vertices], np.int32),)     # Applying masking function
    # plt.imshow(maskimage)
    # Drawing the lane line using Hough Transformation
    lines = cv2.HoughLinesP(cropped_image,
                            rho=2,
                            theta=np.pi/180,
                            threshold=50,
                            lines=np.array([]),
                            minLineLength=40,
                            maxLineGap=100)
    image_with_lines = drow_the_lines(image, lines)
    return image_with_lines


cap = cv2.VideoCapture('video (1).mp4')


result = cv2.VideoWriter('output.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, (960, 540))


while (cap.isOpened()):
    ret, frame = cap.read()
    scale_percent = 50  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)
    print(dim)

    # resized frame
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_CUBIC)

    frame = process(frame)
    result.write(frame)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
