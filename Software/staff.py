import cv2
import numpy as np


def detect_staff(gray):
    row_sum = np.sum(gray, 1)
    staffLines = []

    maximum = np.max(row_sum)

    # Save rows which have high no. of black pixels
    for row in range(gray.shape[0]):
        length = int(row_sum[row] * gray.shape[1] / maximum)
        if length < (gray.shape[1] * 1 / 3):
            staffLines.append(row)

    fill(gray, staffLines)
    return staffLines


def fill(gray, staff):
    staff_img = np.copy(gray) * 0
    for x in staff:
        for y in range(gray.shape[1]):
            if gray[x][y] != 255:
                if gray[x - 1][y] == 0 and gray[x + 1][y] == 0:
                    gray[x][y] = 0
                else:
                    gray[x][y] = 255
                    staff_img[x][y] = 255

    cv2.imwrite("./Processing/remove_staff.png", gray)
    cv2.imwrite("./Processing/staff.png", staff_img)
