import cv2
import numpy as np
from numpy.core.numerictypes import find_common_type

# Colors
MIDNIGHT_BLUE = (70, 47, 6)
TOMATO = (54, 65, 210)


def stack_images(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(
                        imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(
                        imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(
                    imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(
                    imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def rescale_frame(frame, scale=0.5):
    # Live video, static video/img
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_CUBIC)


def translate(src, x, y):
    # Translate (Shift image along x and y axis)
    translation_matrix = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (src.shape[1], src.shape[0])
    return cv2.warpAffine(src, translation_matrix, dimensions)


def rotate(src, angle, pivot=None, scale=1.0):
    # Rotate around a specific point as pivot.
    (height, width) = src.shape[:2]
    if not pivot:
        pivot = (width//2, height//2)
    rotation_matrix = cv2.getRotationMatrix2D(pivot, angle, scale)
    dimensions = (width, height)
    return cv2.warpAffine(src, rotation_matrix, dimensions)


def clean_slate(dimensions, color=(0, 0, 0)):
    slate = np.zeros(shape=dimensions, dtype='uint8')
    slate[:] = color
    return slate


def canvas_mono(dimensions):
    return np.zeros(shape=dimensions, dtype='uint8')


def rect_center(src, color=(0, 0, 0), thickness=2):
    origin = (src.shape[1]//4, src.shape[0]//4)
    bottom_right_corner = (src.shape[1]*3//4, src.shape[0]*3//4)
    return cv2.rectangle(src.copy(), origin, bottom_right_corner, color, thickness=thickness)


def label(src, text="", center=False):
    (height, width) = src.shape[:2]
    if not center:
        label_rect_origin = (0, int(7.2*height/8))
        label_rect_corner = (width//4, height)
        label_rect_w, label_rect_h = label_rect_corner[0] - \
            label_rect_origin[0], label_rect_corner[1]-label_rect_origin[1]

        font_scale = (label_rect_w * label_rect_h)*40/(height*width)
        TEXT_WINDOW = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_DUPLEX, font_scale, 2)

        label_rect_corner = (TEXT_WINDOW[0][0]+label_rect_w//10, height)
        label_rect_origin = (
            0, height-(TEXT_WINDOW[0][1]+height//100+label_rect_h//3))
        canvas = src.copy()

        # Image Margin
        canvas = cv2.rectangle(
            canvas, (0, 0), (width, height), TOMATO, height//50)
        # Highlighter
        canvas = cv2.rectangle(canvas, label_rect_origin,
                               label_rect_corner, TOMATO, -1)
        # Label-Text
        canvas = cv2.putText(canvas, text, (0+label_rect_w//20, height-label_rect_h//4),
                             cv2.FONT_HERSHEY_DUPLEX, font_scale, MIDNIGHT_BLUE, 2)
        return canvas

    else:
        TEXT_WINDOW = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_TRIPLEX, 1, 2)
        text_base_height, text_base_width = TEXT_WINDOW[0][::-1]

        font_scale = (width-width//10)/text_base_width
        margin = int((width-text_base_width*font_scale)/2)

        label_rect_origin = (
            margin, (height+text_base_height)//2)  # Bottom Left
        label_rect_corner = (width, (height-text_base_height)//2)  # Top Right

        label_rect_w, label_rect_h = label_rect_corner[0] - \
            label_rect_origin[0], label_rect_corner[1]-label_rect_origin[1]

        canvas = src.copy()

        cv2.putText(canvas, text, label_rect_origin, cv2.FONT_HERSHEY_TRIPLEX,
                    font_scale, (255, 255, 255), 20), text_base_height*font_scale

        return canvas
