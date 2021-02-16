import face_recognition
import picamera
import numpy as np
import os
from datetime import datetime

# define the folder for stranger images
path = 'home/pi/flaskweb_nostream/static/images'

# initialize the camera 
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# Initialize some variables
face_locations = []
face_encodings = []

def capture_and_compare(known_face_encodings):
    match = True
    result = False

    while True:
        # Grab a single frame of video from the RPi camera as a numpy array
        camera.capture(output, format="rgb")

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(output)
        face_encodings = face_recognition.face_encodings(output, face_locations)

        # Loop over each face found in the frame to see if it's someone we know.
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            match = face_recognition.compare_faces([known_face_encodings], face_encoding)
            if not match : 
                result = True
                break

        if result:
            os.rename(output, path+datetime.now().strftime('%A-%y%m%d%H%M%S.jpg'))


'''
        camera.capture('/home/pi/Pictures/' + datetime.now().strftime('%A-%y%m%d%H%M%S.jpg'))

'''