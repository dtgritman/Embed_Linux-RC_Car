from imutils.video.pivideostream import PiVideoStream
import io
import time
import cv2
import picamera
import picamera.array
import numpy as np
import imutils
stream = io.BytesIO()
#cam = picamera.PiCamera()
#cam.resolution = (320,240)
#cam.framerate = 32
shirt_cascade = cv2.CascadeClassifier('body.xml')
#green = 60
#sensitivity = 15
#green_pixels = 0
print(cv2.__version__)
vs = PiVideoStream().start()
time.sleep(2.0)
while True:
    # captures frames from camera, stores them in stream
    #cam.capture(stream, format='jpeg', use_video_port=True)
    #frame = np.fromstring(stream.getvalue(), dtype=np.uint8)
    #stream.seek(0)
    frame = vs.read()
    frame = imutils.resize(frame, width=360)
    #frame = cv2.imdecode(frame, 1)
    # convert to grayscale for cascade detection
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    shirts = shirt_cascade.detectMultiScale(gray, 1.02, 5)
    #color_frame = frame
    # draws rectangle around any objects detected
    for (x,y,w,h) in shirts:
        # rectangle is half the height of body detected
        cv2.rectangle(frame,(x,y),(x+w,y+(h/2)),(255,255,0),2)
        print("Coordinates of center are x:" + str((int(x) + int(w)/2)) + " y: " + str((int(y) + int(h)/2)))
    #    color_frame = frame[y:y+h, x:x+w]
    frame = cv2.resize(frame,(640,480))
    cv2.imwrite('test.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    # loop over the boundaries
    # create NumPy arrays from the boundaries
    #lower_green = np.array([green - sensitivity, 100, 100])
    #upper_green = np.array([green + sensitivity, 255, 255])

    # find the colors within the specified boundaries and apply
    # the mask
    #mask = cv2.inRange(frame, lower_green, upper_green)
    #merged_mask = cv2.inRange(lower_green, upper_green)
    #output = cv2.bitwise_and(frame, frame, mask=mask)

    # show the images
    #cv2.imshow('images',  output)
    # frames are outputed
    cv2.imshow('Video', frame)
    #cv2.imshow('color frame', color_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        vs.stop()
        print("Exiting")
        break
