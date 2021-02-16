# run 
# 'pip install apache'
# 'pip install flask'
# 'pip install flask_uploads'
# before you launch the website

from flask import Flask, render_template, url_for, request, Response
from flask_uploads import UploadSet, configure_uploads, IMAGES
from camera_pi import Camera
from faceDetection import faceCheck
import sys
sys.path.insert(0, '/home/pi/dlib/build/face_recognition') 
import os
import threading

os.system('python faceDetection.py')
app = Flask(__name__)

# template for info displaying on packge page
packages = [
    {
        'package_id': '123456789',
        'item_name': 'Gold standard 100% Whey protein powder',
        'date_delivered': 'June 2nd, 2021'
    },
    {
        'package_id': '456789101',
        'item_name': 'Nissin Cup Ramen Noodle Soup',
        'date_delivered': 'June 2nd, 2021'
    }
]

# homepage, display project bio
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='home')

# package page, display package status
@app.route("/package")
def package():
    return render_template('package.html', title='package', packages=packages)

# frontdoor page, display frontdoor status
@app.route("/frontdoor")
def frontdoor():
    images = os.listdir(os.path.join(app.static_folder, "images"))
    return render_template('frontdoor.html', title='frontdoor',images = images)

# upload page, allow user to upload face images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/known_img'
configure_uploads(app, photos)

# check if the upload file is allow file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload(self):
    result = ''
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']
        if allowed_file(file.filename):
            filename = photos.save(request.files['photo'])
            result = filename
    return render_template('upload.html', result=result)

'''
# video streaming page, display what's outside of the frontdoor
@app.route('/videostreaming')
def videostreaming():
    """Video streaming home page."""
    return render_template('videostreaming.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
'''

if __name__ == '__main__':
    t = threading.Thread(target=faceCheck, args = ())
    t.daemon = True
    t.start()

    app.run(debug=True)
    