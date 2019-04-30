# created by Joshua Simons
import io
import time
import cv2
import picamera
import picamera.array
import numpy as np
# green range from RGB (124,252,0) to (85,107,47)
stream = io.BytesIO()
cam = picamera.PiCamera()
cam.resolution = (480,360)
face_cascade = cv2.CascadeClassifier('body.xml')
boundaries = [([47,107,85], [0,252,124])]
print(cv2.__version__)

while True:
    cam.capture(stream, format='jpeg', use_video_port=True)
    frame = np.fromstring(stream.getvalue(), dtype=np.uint8)
    stream.seek(0)

    frame = cv2.imdecode(frame, 1)

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.01, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
    frame = cv2.resize( frame,(480,360)) 
    # loop over the boundaries
    for (lower, upper) in boundaries:
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(frame, lower, upper)
        output = cv2.bitwise_and(frame, frame, mask = mask)

        # show the images
        cv2.imshow("images", np.hstack([frame, output]))
        #cv2.imshow('Video', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        print("Exiting")
        break
