import face_recognition
import cv2
import numpy as np
from gtts import gTTS
from notifier import SendText
import os
import time

# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

aktar_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Aktar_Zaman_1.jpg")
aktar_image_encoding = face_recognition.face_encodings(aktar_image)[0]

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Barak_Obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
ashraf_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Ashraf_Zaman.jpg")
ashraf_face_encoding = face_recognition.face_encodings(ashraf_image)[0]

fariha_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Fariha_Choudhury.jpg")
fariha_image_encoding = face_recognition.face_encodings(fariha_image)[0]

aminul_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Aminul_Islam.jpg")
aminul_image_encoding = face_recognition.face_encodings(aminul_image)[0]

bushra_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Amina_Bushra.jpg")
bushra_image_encoding = face_recognition.face_encodings(bushra_image)[0]


hamza_image = face_recognition.load_image_file("/Users/zamy/Desktop/Python_Projects/facial_recognition/Known_Images/Hamza_Ahmed.jpg")
hamza_image_encoding = face_recognition.face_encodings(hamza_image)[0]
# Load a third sample picture and learn how to recognize it.
# rahima_image = face_recognition.load_image_file("Rahima_Mahmood.jpg")
# rahima_face_encoding = face_recognition.face_encodings(rahima_image)[0]


# Create arrays of known face encodings and their names
known_face_encodings = [
    aktar_image_encoding,
    obama_face_encoding,
    ashraf_face_encoding,
    fariha_image_encoding,
    aminul_image_encoding,
    bushra_image_encoding,
    hamza_image_encoding
    # rahima_face_encoding,
]
known_face_names = [
    "Aakhtarr zaman",
     "Barak Obama",
    "Ashraf Zaman",
    "Fariha Choudhury",
    "Aminul Islam",
    "Drama Queen",
    "Hamza Ahmed"
    # "Rahima Mahmood"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
# Language in which you want to convert the language to
language = 'en'
# the number you want to send the text to
send_to = "+15106605453"
# the number you want to send the text from
sent_from = "+15104399655"

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
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                # send_text_class_object = SendText(send_to, sent_from, "There's " + str(name) + " at your door")
                # send_text_class_object._send()
                # time.sleep(300)
                if str(name) == "Aakhtarr zaman":
                    bengali_gretting = "কিতা খবর" + str(name) + "বালা আছ নি"
                    gretting_gTTS = gTTS(text=bengali_gretting, lang='bn', slow=False)
                    gretting_gTTS.save("Bengali_Grettings.mp3")
                    os.system("mpg321 Bengali_Grettings.mp3")
                else:
                    gretting = "What's up" + str(name) + "How are you doing today?"
                    gretting_gTTS = gTTS(text=gretting, lang=language, slow=False)
                    gretting_gTTS.save("Grettings.mp3")
                    os.system("mpg321 Grettings.mp3")

            face_names.append(name)

            # if len(known_names) > 0:
            #     next_id = max(known_names) + 1
            # else:
            #     next_id = 0

    process_this_frame = not process_this_frame


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
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
