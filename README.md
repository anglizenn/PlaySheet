# PlaySheet
A mobile application created on Android Studio which accepts a music sheet, scans it and plays the tune of the music sheet through the use of Optical Music Recognition (OMR). Demo: https://youtube.com/shorts/HeN24CEaPgA?feature=share

## Software
The processing and conversion of the music sheet to a tune is performed through a Python software connected to the mobile application through a server. The conversion can be broken down into 9 steps:
### 1. Staff Line Detection & Removal
The staff lines were detected through the use of a histogram to find the highest intensity of black pixels. To remove the staff lines, the pixels above and below the staff line pixels were checked to see if they were also part of a musical notation to prevent fragmentation of the musical notation.
   
### 2. Cropping
Each page of the music sheet was cropped vertically and horizontally to improve the runtime of the software. The horizontal cropping was done based on the first and last column in the image which contain a black pixel. The vertical cropping was done based on the staff lines at three ledger lines above and below the highest and lowest staff line on the page. This was done by calculating the average spacing between staff lines and adding/subtracting it to the relevant staff line row index.
   
### 3. Clef Detection & Identification
Blob detection was performed on the pre-processed left part of the page to idenitfy if the clef was a treble/base clef. 
   
### 4. Notehead Detection & Identification
Pre-processing was performed on the image and blob detection was used to identify the noteheads and if the notehead was filled or unfilled.
   
### 5. Stem Detection
Hough transform was applied to the pre-processed image to find lines with an angle of 90/180 degrees.
  
### 6. Beam Detection
The same was done for beam detection except the lines with an angle of 0/360 degrees were identified.
   
### 7. Musical Note Identification
Based on the information obtained in earlier stages, the musical note could be identified based on its individual characteristics. For example, crotchets would be filled noteheads with a stem attached to it but without a beam. Once the musical notes have been identified, the duration of each note can be obtained.
   
### 8. Pitch Identification
The pitch was identified through the position of the centre of the notehead to see which staff line/space it intersects with.
   
### 9. Encoding to MIDI
The information is then fed to a Python library "MIDIUtil" to obtain a MIDI file which will be sent back to the mobile application.

## Mobile Application
The mobile application was developed on Android Studio. The user can select a music sheet from their device and send it to the Python software where the music sheet is read and converted to a MIDI file. The MIDI file is sent back to the mobile application from the Python software and the user can listen to the tune.
