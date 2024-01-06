import cv2
from midiutil.MidiFile import MIDIFile
import numpy as np

filename = "./Result/output.mid"


def compile_notes(notes, staff, clef):
    pitch = []
    notes.sort(key=lambda x: x[0])
    for line in staff:
        sublist = []
        x_list = []
        difference = []
        for note in notes:
            if min(line) <= note[1] <= max(line):
                if x_list:
                    difference = [abs(x - note[0]) for x in x_list]
                if any(x <= 15 for x in difference):
                    if sublist[-1][1] == 4:
                        sublist.pop()
                        x_list.pop()
                        sublist.append((note[1], note[2]))
                        x_list.append(note[0])
                else:
                    sublist.append((note[1], note[2]))
                    x_list.append(note[0])
        pitch_sublist = []
        staff_part = np.array(line)
        for note in sublist:
            difference_array = np.absolute(staff_part - note[0])
            pitch_sublist.append((difference_array.argmin(), note[1]))
        pitch.append(pitch_sublist)

    return pitch, detect_clef(clef, staff)


def compile_notes_test(notes, staff, clef, img, filename):
    pitch = []
    notes.sort(key=lambda x: x[0])
    for line in staff:
        sublist = []
        x_list = []
        difference = []
        for note in notes:
            if line[0] <= note[1] <= line[-1]:
                if x_list:
                    difference = [abs(x - note[0]) for x in x_list]
                if any(x <= 15 for x in difference):
                    if sublist[-1][1] == 4:
                        sublist.pop()
                        x_list.pop()
                        sublist.append([note[1], note[2]])
                        x_list.append(note[0])
                else:
                    sublist.append([note[1], note[2]])
                    x_list.append(note[0])
        colour(x_list, sublist, img, filename)

        pitch_sublist=[]
        staff_part=np.array(line)
        for note in sublist:
            difference_array = np.absolute(staff_part - note[0])
            pitch_sublist.append((difference_array.argmin(), note[1]))
        pitch.append(pitch_sublist)

    return pitch, detect_clef(clef, staff)


def colour(list1, list2, img, filename):
    notes = [[a] + b for a, b in zip(list1, list2)]
    for note in notes:
        center = (note[0], note[1])
        if note[2] == 1:
            cv2.ellipse(img, center, (11, 7), -20, 0, 360, (0, 255, 0), -1)
        elif note[2] == 2:
            cv2.ellipse(img, center, (11, 7), -20, 0, 360, (255, 0, 0), -1)
        elif note[2] == 4:
            cv2.ellipse(img, center, (12, 7), 0, 0, 360, (0, 0, 255), -1)
        elif note[2] == 1 / 2:
            cv2.ellipse(img, center, (11, 7), -20, 0, 360, (0, 255, 255), -1)
    cv2.imwrite(filename, img)


def detect_clef(clef, staff):
    point = []
    for sublist in staff:
        for i in clef:
            if sublist[7] <= i[1] <= sublist[15]:
                point.append(2)
                break
            elif sublist[15] <= i[1] <= sublist[-1]:
                point.append(1)
                break
    return point


def create_midi(notes, clef):
    mf = MIDIFile(1)  # only 1 track
    time = 0
    duration = 0
    mf.addTrackName(0, time, "Sample Track")
    mf.addTempo(0, time, 60)

    for x in range(len(clef)):
        if clef[x] == 1:
            chord = [89, 88, 86, 84, 83, 81, 79, 77, 76, 74, 72, 71, 69, 67, 65, 64, 62, 60, 59, 57, 55, 53, 52]
        else:
            chord = [69, 67, 65, 64, 62, 60, 59, 57, 55, 53, 52, 50, 48, 47, 45, 43, 41, 40, 38, 36, 35, 33, 31]
        for note in notes[x]:
            pitch = chord[note[0]]
            time += duration
            duration = note[1]
            mf.addNote(0, 0, pitch, time, duration, 100)

    # write it to disk
    with open(filename, 'wb') as outf:
        mf.writeFile(outf)
