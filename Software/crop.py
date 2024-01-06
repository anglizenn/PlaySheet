import cv2


def crop(staff_line):
    left, right = crop_horizontal(staff_line)
    staff, top, bottom = crop_vertical(staff_line)
    return staff, top, bottom, left, right


def crop_horizontal(staff):
    minimum = []
    maximum = []
    img = cv2.imread("./Processing/staff.png", cv2.COLOR_BGR2GRAY)
    for i in staff:
        for y in range(img.shape[1]):
            if img[i][y] != 0:
                minimum.append(y)
                break
        for z in range(img.shape[1] - 1, -1, -1):
            if img[i][z] != 0:
                maximum.append(z)
                break

    return min(minimum), max(maximum) + 1


def crop_vertical(rows):
    staff_lines = [rows[0]]
    for x in range(0, len(rows) - 1):
        if rows[x + 1] - rows[x] != 1:
            staff_lines.append(rows[x + 1])

    staff = [staff_lines[x:x + 5] for x in range(0, len(staff_lines), 5)]

    difference = []
    for x in staff:
        difference.append([j - i for i, j in zip(x[:-1], x[1:])])

    flatten = [y for x in difference for y in x]
    average = round(sum(flatten) / len(flatten))

    for line in staff:
        for x in range(1, 4):
            line.insert(0, line[0] - average)
            line.append(line[-1] + average)
        for x in range(len(line)):
            line.append(int(line[x] - average / 2))
        line.sort()
        line.append(int(line[-1] + average / 2))

    top = staff[0][0] - 20
    bottom = staff[-1][-1] + 20

    staff = [[value - top for value in sublist] for sublist in staff]

    return staff, top, bottom
