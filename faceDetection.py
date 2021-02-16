import face_recognition
import cv2
import numpy as np
import os
from datetime import datetime

def faceCheck():
    # PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
    # OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
    # specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir('static/known_img'):
        # use face_recognition.face_encodings(img) to get the encodings of known people
        image = face_recognition.load_image_file('/home/pi/flaskweb_nostream/static/known_img/' + filename)
        known_face_encodings = face_recognition.face_encodings(image)
        known_face_names = os.path.splitext(filename)[0]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    count = 0
    destpath = '/home/pi/flaskweb_nostream/static/unknown/'

    while True:
        print('*\n*\n*\nProgram start')
        name = ''
        Unknown_face_encodings = []
        Unknown_face_names = []

        print('\tEncoding stranger faces that has been captured in: ' + destpath)
        for filename in os.listdir(destpath):
            # use face_recognition.face_encodings(img) to get the encodings of known people
            print('\tGet file:' + filename)
            image = face_recognition.load_image_file(destpath + filename)
            Unknown_face_encodings = face_recognition.face_encodings(image)
            Unknown_face_names = os.path.splitext(filename)[0]
        
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            print('\tStart analyzing the frame')
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                print('\tFace detecteded')
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                #check if this unknown face has captured before 
                unknown_match = face_recognition.compare_faces(Unknown_face_encodings, face_encoding)
                
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

                face_names.append(name)
                
                # save the frame if the person is unknown
                if True in unknown_match:
                    print('\tThis stranger has already captured!')

                # datetime object containing current date and time
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H/%M/%S")
                
                if not any(unknown_match) and name == 'Unknown':
                    if not cv2.imwrite(destpath + "Unknown%d.jpg" % count, frame):
                        raise Exception("Could not write image")
                    print("\tUnknown%d.jpg successfully saved on %s!!!" % (count, dt_string))
                    count = count + 1
                            

        process_this_frame = not process_this_frame


    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()