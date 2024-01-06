import cv2

import crop
import encode
import note
import notehead
import parts
import staff
import time
from pdf2image import convert_from_path


def main(img_colour):

    # read file
    img = cv2.cvtColor(img_colour, cv2.COLOR_BGR2GRAY)

    # Detect and remove staff line
    staff_line = staff.detect_staff(img)

    # Crop image
    staff_part, top, bottom, left, right = crop.crop(staff_line)

    # Read image with staff line removed
    removedstaff_img = cv2.imread("./Processing/remove_staff.png", cv2.IMREAD_GRAYSCALE)
    removedstaff_crop = removedstaff_img[top:bottom, left:right]

    # Detect note head
    clef = parts.detect_clef(removedstaff_img[top:bottom, left:left + 60])
    empty, filled = notehead.detect_notehead(removedstaff_crop, staff_part, clef)

    # Detect and remove stem and beam
    stems = parts.detect_parts(removedstaff_crop)

    # Identify notes
    empty_result, filled_result, beam_result, semibreve_result = note.identify(empty, filled, stems, clef)

    crotchet = []
    minim = []
    quaver = []
    semibreve = []

    # Draw the notes

    for l in beam_result:
        quaver.append((l[0], l[1], 0.5))
    for i in empty_result:
        minim.append((i[0], i[1], 2))
    for j in filled_result:
        crotchet.append((j[0], j[1], 1))
    for k in semibreve_result:
        semibreve.append((k[0], k[1], 4))

    join = list(set(crotchet + minim + quaver + semibreve))

    # Get the pitch of each note
    return encode.compile_notes(join, staff_part, clef)


# Main run function
def run(filename):
    notes_list = []
    clef_list = []

    start_time = time.time()
    fname = './Processing/page.png'

    # Convert pdf to image
    pages = convert_from_path(filename, 150,
                              poppler_path=r"C:\Program Files (x86)\Poppler\poppler-23.01.0\Library\bin")

    # Loop over pages
    for page in pages:
        page.save(fname, "PNG")
        img_colour = cv2.imread(fname)
        # Add notes from the page to the list
        notes, clef = main(img_colour)
        notes_list.extend(notes)
        clef_list.extend(clef)

    # Create midi file
    encode.create_midi(notes_list, clef_list)
    print(time.time() - start_time)
