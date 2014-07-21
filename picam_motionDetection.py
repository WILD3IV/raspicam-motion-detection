#!/usr/bin/env python

import cv2
import numpy as np
import datetime
import time
import io
import picamera

## frame_diff finds two absolute differences between image matrices;
## 3 images are used to create a moving average of frames
def frame_diff(f0, f1, f2):
    d1 = cv2.absdiff(f0,f2)
    d2 = cv2.absdiff(f1, f2)
    result = cv2.bitwise_and(d1,d2)
    
    ret, result = cv2.threshold(result, threshold, 255,cv2.THRESH_BINARY);
    return result
    
def write_video(camera):
    camera.resolution = (1280, 720)
    camera.ISO = 500
    folder = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    
    camera.start_recording('/home/pi/motion_camera/recorded_video/' + folder + '/' + timestamp + '.h264')
    camera.wait_recording(30)    
    camera.stop_recording()
    print 'recording stopped'

    camera.resolution = (320,240)
    
print 'INITIALIZING MOTION DETECTION CAMERA'

camera = picamera.PiCamera()
camera.resolution = (320,240)
camera.LED = False

stream = io.BytesIO()

threshold = 35
min_pixel_change = 1000
min_pixel_change_rec = 500
    
    
stream.seek(0)
camera.capture(stream, 'jpeg', True)
prev_frame = cv2.cvtColor((cv2.imdecode((np.fromstring(stream.getvalue(), dtype=np.uint8)), 1)), cv2.COLOR_BGR2GRAY)

stream.seek(0)
camera.capture(stream, 'jpeg', True)
current_frame = cv2.cvtColor((cv2.imdecode((np.fromstring(stream.getvalue(), dtype=np.uint8)), 1)), cv2.COLOR_BGR2GRAY)

stream.seek(0)
camera.capture(stream, 'jpeg', True)
next_frame = cv2.cvtColor((cv2.imdecode((np.fromstring(stream.getvalue(), dtype=np.uint8)), 1)), cv2.COLOR_BGR2GRAY)

print 'MOTION DETECTION ACTIVATED'

while True:
    movement = frame_diff(prev_frame, current_frame, next_frame)   
    nonZero = cv2.countNonZero(movement)
   
    
    if nonZero > min_pixel_change:
        print 'motion detected<<>>start recording'

        write_video(camera)
        
        stream.seek(0)
        camera.capture(stream, 'jpeg', True)
        current_frame = cv2.cvtColor((cv2.imdecode((np.fromstring(stream.getvalue(), dtype=np.uint8)), 1)), cv2.COLOR_BGR2GRAY)
        stream.seek(0)
        camera.capture(stream, 'jpeg', True)
        next_frame = cv2.cvtColor((cv2.imdecode((np.fromstring(stream.getvalue(), dtype=np.uint8)), 1)), cv2.COLOR_BGR2GRAY)
        
    prev_frame = current_frame
    current_frame = next_frame
    stream.seek(0)
    camera.capture(stream, 'jpeg', True)
    next_frame = cv2.cvtColor((cv2.imdecode((np.fromstring(stream.getvalue(), dtype=np.uint8)), 1)), cv2.COLOR_BGR2GRAY)
        

    key= cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break

print "Goodbye"
