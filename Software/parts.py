import cv2
import numpy as np


def detect_parts(img):
    detect_beam(img)
    return detect_stem(img)


def detect_stem(img):
    preprocess_img = preprocess_stem(img)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 2  # angular resolution in radians of the Hough grid
    threshold = 6  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 32  # minimum number of pixels making up a line
    max_line_gap = 6  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(preprocess_img, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    stems = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
        if abs(angle) == 90:
            cv2.line(line_image, (x1, y1), (x2, y2), 255, 1)
            stems.append([x1, y1, x2, y2])

    cv2.imwrite("./Processing/stem.png", line_image)

    return stems


def preprocess_stem(img):
    dilate = cv2.dilate(img, np.ones((7, 1), np.uint8))
    erode = cv2.erode(dilate, np.ones((1, 5), np.uint8))
    edges = cv2.Canny(erode, 250, 350, apertureSize=3)
    return cv2.dilate(edges, np.ones((5, 5), np.uint8))


def detect_beam(gray):
    preprocess_img = preprocess_beam(gray)

    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 2  # angular resolution in radians of the Hough grid
    threshold = 6  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = 30  # minimum number of pixels making up a line
    max_line_gap = 1  # maximum gap in pixels between connectable line segments
    line_image = np.copy(gray) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(preprocess_img - 255, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi
        if 0 <= abs(angle) <= 45:
            cv2.line(line_image, (x1, y1), (x2, y2), 255, 1)

    dilate = cv2.dilate(line_image, np.ones((21, 17), np.uint8))
    cv2.imwrite("./Processing/beam.png", dilate)


def preprocess_beam(img):
    erode = cv2.erode(img, np.ones((5, 3), np.uint8))
    dilate = cv2.dilate(erode, np.ones((7, 5), np.uint8))
    return cv2.erode(dilate, np.ones((7, 3), np.uint8))


def detect_clef(img):
    preprocess_img = preprocess_clef(img)

    # blob detection
    params = cv2.SimpleBlobDetector_Params()
    params.filterByColor = False
    params.minThreshold = 50
    params.minArea = 30
    params.filterByCircularity = True
    params.minCircularity = 0.7

    det = cv2.SimpleBlobDetector_create(params)

    # detect blobs
    clef_point = []
    points = det.detect(preprocess_img)
    # clef = cv2.drawKeypoints(img, points, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
    for kp in points:
        # cv2.ellipse(clef, center, (11, 7), -20, 0, 360, (0, 255, 0), -1)
        clef_point.append([int(kp.pt[0]), int(kp.pt[1])])
    # cv2.imwrite("./Processing/clef.png", clef)
    return clef_point


def preprocess_clef(img):
    blurred = cv2.medianBlur(img, 9)
    adap_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 0)
    return cv2.dilate(adap_thresh, np.ones((3, 3), np.uint8))
