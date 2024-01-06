import cv2


def identify(empty, filled, stems, clef):
    empty_result, filled_result, beam_result, remove = identify_note(empty, filled, stems, clef)
    semibreve_result = []
    if empty_result:
        semibreve_result = detect_semibreve(empty_result, empty, remove)
    return empty_result, filled_result, beam_result, semibreve_result


def detect_semibreve(empty_result, empty, remove):
    possible_empty = [x for x in empty if x not in empty_result and x not in remove]
    return possible_empty


def identify_note(empty, filled, stems, clef):
    beam = cv2.imread("./Processing/beam.png", cv2.IMREAD_GRAYSCALE)
    empty_result = []
    filled_result = []
    beam_result = []
    final = []
    remove_list = []
    for x in empty + filled:
        if x not in final:
            final.append(x)
    final.sort(key=lambda x: x[0])

    clef.sort(key=lambda x: x[0])
    clef_x = clef[-1][0]

    for stem in stems:
        x1, y1 = [stem[0], stem[1]], [stem[2], stem[3]]

        if stem[0] > clef_x + 10 or stem[2] > clef_x + 10:

            for i in final:
                if check_stem(i, x1, y1):
                    if i in filled:
                        if check_beam(x1, y1, beam) and beam[i[1]][i[0]] != 255:
                            beam_result.append(i)
                        else:
                            filled_result.append(i)
                    else:
                        if check_beam(x1, y1, beam):
                            remove_list.append(i)
                        else:
                            empty_result.append(i)
                    break

    return empty_result, filled_result, beam_result, remove_list


def check_stem(center, x1, y1):
    size = 12
    topleft, topright = [center[0] - size, center[1] - size], [center[0] + size, center[1] - size]
    botleft, botright = [center[0] - size, center[1] + size], [center[0] + size, center[1] + size]

    if doIntersect(x1, y1, topleft, topright) \
            or doIntersect(x1, y1, topleft, botleft) \
            or doIntersect(x1, y1, topright, botright) \
            or doIntersect(x1, y1, botleft, botright):
        return True
    else:
        return False


def check_beam(p1, p2, beam):
    if p1[1] >= p2[1]:
        y1 = p1[1]
        y2 = p2[1]
    else:
        y2 = p1[1]
        y1 = p2[1]
    for y in range(y2, y1 + 1):
        if beam[y][p1[0]] == 255:
            return True
    return False


def orientation(p, q, r):
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0


def doIntersect(x1, y1, x2, y2):
    o1 = orientation(x1, y1, x2)
    o2 = orientation(x1, y1, y2)
    o3 = orientation(x2, y2, x1)
    o4 = orientation(x2, y2, y1)

    if ((o1 != o2) and (o3 != o4)):
        return True
    else:
        return False
