from imutils.video.pivideostream import PiVideoStream
import io
import time
import cv2
import picamera
import picamera.array
import numpy as np
import imutils
# green range from RGB (124,252,0) to (85,107,47)
stream = io.BytesIO()
cam = picamera.PiCamera()
cam.resolution = (320,240)
face_cascade = cv2.CascadeClassifier('body.xml')
green = 60
sensitivity = 15
green_frames = 0
print(cv2.__version__)
vs = PiVideoStream().start()
while True:
    #cam.capture(stream, format='jpeg', use_video_port=True)
    #frame = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #stream.seek(0)
    frame = vs.read()
    frame = cv2.imdecode(frame, 1)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    faces = face_cascade.detectMultiScale(gray, 1.02, 5)
    color_frame = frame
    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)
        color_frame = frame[y:y+h, x:x+w]
    for (x,y) in color_frame:
        if np.any(color_frame[x,y] != 0):
            green_frames = green_frames + 1
    frame = cv2.resize(frame,(640,480))
    # loop over the boundaries
    # create NumPy arrays from the boundaries
    lower_green = np.array([green - sensitivity, 100, 100])
    upper_green = np.array([green + sensitivity, 255, 255])

    # find the colors within the specified boundaries and apply
    # the mask
    mask = cv2.inRange(frame, lower_green, upper_green)
    #merged_mask = cv2.inRange(lower_green, upper_green)
    output = cv2.bitwise_and(frame, frame, mask=mask)

    # show the images
    cv2.imshow('images',  output)
    cv2.imshow('Video', frame)
    cv2.imshow('color frame', color_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        print("Exiting")
        break
