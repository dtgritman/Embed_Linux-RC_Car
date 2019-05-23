#
import io
import time
import cv2
import picamera
import picamera.array
import numpy as np

stream = io.BytesIO()
cam = picamera.PiCamera()
cam.resolution = (320,240)
face_cascade = cv2.CascadeClassifier('faces.xml')

print(cv2.__version__)

while True:
    cam.capture(stream, format='jpeg', use_video_port=True)
    frame = np.fromstring(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)

    frame = cv2.imdecode(frame, 1)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
    frame = cv2.resize( frame,(640,480)) 
    cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        print("Exiting")
        break
