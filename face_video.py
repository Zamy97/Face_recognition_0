import face_recognition
import os
import cv2
import pickle
import time



KNOWN_FACES_DIR = 'known_faces'
# UNKNOWN_FACES_DIR = 'unknown_faces'
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'cnn'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model

video = cv2.VideoCapture(0)

next_id = 0


# Returns (R, G, B) from name
def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

known_faces = []
known_names = []
process_this_frame = True

# We oranize known faces as subfolders of KNOWN_FACES_DIR
# Each subfolder's name becomes our label (name)
for name in os.listdir(KNOWN_FACES_DIR):

    # Next we load every file of faces of known person
    for filename in os.listdir(f'{KNOWN_FACES_DIR}/{name}'):
        encoding = pickle.load(open(f'{name}/{filename}', 'rb'))

        # Append encodings and name
        known_faces.append(encoding)
        known_names.append(int(name))

    if len(known_names) > 0:
        next_id = max(known_names) + 1
    else:
        next_id = 0

while True:
    # Grab a single frame of video
    ret, frame = video.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:

        # This time we first grab face locations - we'll need them to draw boxes
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):

            # We use compare_faces (but might use face_distance as well)
            # Returns array of True/False values in order of passed known_faces
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

            # Since order is being preserved, we check if any face was found then grab index
            # then label (name) of first matching known face withing a tolerance
            match = None
            if True in results:  # If at least one is true, get a name of first of found labels
                match = known_names[results.index(True)]
                print(f' - {match} from {results}')
            else:
                match = str(next_id)
                next_id += 1
                known_names.append(match)
                known_faces.append(face_encoding)
                os.mkdir(f'{KNOWN_FACES_DIR}/{match}')
                pickle.dump(face_encoding, open(f'{KNOWN_FACES_DIR}/{match}/{match}-{int(time.time())}.pkl', 'wb'))


    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, known_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4


        # # Each location contains positions in order: top, right, bottom, left
        # top_left = (face_location[3], face_location[0])
        # bottom_right = (face_location[1], face_location[2])

        # Get color by name using our fancy function
        color = name_to_color(match)

        # Paint frame
        # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Now we need smaller, filled grame below for a name
        # This time we use bottom in both corners - to start from bottom and move 50 pixels down
        top_left = (face_location[3], face_location[2])
        bottom_right = (face_location[1], face_location[2] + 22)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Paint frame
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
# cv2.waitKey(10000)
# cv2.destroyWindow(filename)
