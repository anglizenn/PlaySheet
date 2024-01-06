import cv2
import numpy as np


def detect_notehead(img, staff, clef):
    keypts_filled = filled_head(img)
    keypts_empty = empty_head(img)

    join = keypts_filled + keypts_empty
    join = tuple(set(join))
    # draw circle around blob
    # notes = cv2.drawKeypoints(img, join, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)

    filled = []
    empty = []

    clef.sort(key=lambda x: x[0])
    clef_x = clef[-1][0]+10

    dilated = cv2.dilate(img, np.ones((3,3), np.uint8))

    for kp in join:
        center = [int(kp.pt[0]), int(kp.pt[1])]
        if int(kp.pt[0]) > clef_x + 10:
            if check_staff(staff, center[1]):
                if dilated[int(kp.pt[1])][int(kp.pt[0])] == 0:
                    # cv2.ellipse(notes, center, (11, 7), -20, 0, 360, (0, 255, 0), -1)
                    filled.append(center)
                else:
                    # cv2.ellipse(notes, center, (11, 7), -20, 0, 360, (255, 0, 0), -1)
                    empty.append(center)

    # cv2.imwrite("./Processing/notehead.png", notes)

    return empty, filled


def preprocess_filled(img):
    edges = cv2.Canny(img, 250, 350, apertureSize=3)
    return cv2.dilate(edges, np.ones((5, 5), np.uint8))


def filled_head(img):
    preprocess_img = preprocess_filled(img)

    # blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.minThreshold = 50
    params.minArea = 30
    params.filterByCircularity = True
    params.minCircularity = 0.7

    det = cv2.SimpleBlobDetector_create(params)

    # detect blobs
    return det.detect(preprocess_img)


def preprocess_empty(img):
    blurred = cv2.medianBlur(img, 9)
    adap_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 0)
    dilated = cv2.dilate(adap_thresh, np.ones((3, 3), np.uint8))
    return cv2.erode(dilated, np.ones((3, 3), np.uint8))


def empty_head(img):
    preprocess_img = preprocess_empty(img)

    # blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = False
    params.minThreshold = 50
    params.minArea = 35
    params.filterByCircularity = True
    params.minCircularity = 0.8

    det = cv2.SimpleBlobDetector_create(params)

    # detect blobs
    return det.detect(preprocess_img)


def check_staff(staff, y):
    for line in staff:
        if line[0] <= y <= line[-1]:
            return True
    return False
