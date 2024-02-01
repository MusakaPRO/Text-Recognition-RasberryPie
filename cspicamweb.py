from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import pytesseract
from flask import Flask, jsonify

app = Flask(__name__)

# This will act as a flag to communicate with the web page
start_detected = False

def detect_start():
    global start_detected
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    camera.rotation = 180
    camera.sharpness = 60
    rawCapture = PiRGBArray(camera, size=(640, 480))
    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        text = pytesseract.image_to_string(image)
        
        cv2.imshow("Frame", image)
        print(text)
        if "START" in text:
            start_detected = True
            print("START detected!")
            break  # You can remove this break if you want to keep looking for START

        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("q"):
            break

@app.route('/check')
def check():
    global start_detected
    response = jsonify({'start': start_detected})
    start_detected = False  # Reset after checking
    return response

if __name__ == '__main__':
    from threading import Thread
    Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)).start()
    detect_start()
