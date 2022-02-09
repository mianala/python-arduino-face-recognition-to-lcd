import face_recognition
import sys
import cv2
import numpy as np
from serial import Serial
import time

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# initializing arduino port
display = Serial('/dev/tty.usbmodem141201')  # open serial port

# Load a sample picture and learn how to recognize it.
# mianala_image = face_recognition.load_image_file("mianala.jpg")

mianala_image = face_recognition.load_image_file(
    "images/train/Mianala/1.jpg")
eric_image = face_recognition.load_image_file("images/train/Eric/1.jpg")
tojo_image = face_recognition.load_image_file("images/train/Tojo/1.jpg")
fitahiana_image = face_recognition.load_image_file(
    "images/train/Fitahiana/1.jpg")
soa_image = face_recognition.load_image_file("images/train/Soa/1.jpg")
finaritra_image = face_recognition.load_image_file(
    "images/train/Finaritra/1.jpg")

mianala_face_encoding = face_recognition.face_encodings(mianala_image)[0]
eric_face_encoding = face_recognition.face_encodings(eric_image)[0]
tojo_face_encoding = face_recognition.face_encodings(tojo_image)[0]
fitahiana_face_encoding = face_recognition.face_encodings(fitahiana_image)[0]
soa_face_encoding = face_recognition.face_encodings(soa_image)[0]

# Load a second sample picture and learn how to recognize it.
# finaritra_image = face_recognition.load_image_file("finaritra.jpg")
finaritra_face_encoding = face_recognition.face_encodings(finaritra_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    mianala_face_encoding,
    finaritra_face_encoding,
    eric_face_encoding,
    tojo_face_encoding,
    fitahiana_face_encoding,
    soa_face_encoding,
]
known_face_names = [
    "Loharano",
    "Finaritra",
    "Eric",
    "Tojo",
    "Fitahiana",
    "Soa",
]

faces = []

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(
                known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    if(faces != face_names):
        faces = face_names
        print(face_names)
        if len(faces) == 0:
            display.write(b"Tsy hitako")
        else:
            display.write(bytes(faces[0], encoding="utf-8"))

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
