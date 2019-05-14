# imports
from flask import Flask, render_template, request, Response
import sqlite3 as sqlite
import json
from Drone.Cannon import TankCannon, StepperMotor
from Drone.Car import Car
from threading import Thread
from imutils.video.pivideostream import PiVideoStream
import io
import time
import cv2
import picamera
import picamera.array
import numpy as np
import imutils
import os

autoActive = 0
tankActive = 1

pinCannon = 20
pinServo = 21
stepperAIN2 = 5
stepperAIN1 = 6
stepperBIN1 = 19
stepperBIN2 = 26
cannon = TankCannon(pinCannon, pinServo, StepperMotor(stepperAIN1, stepperAIN2, stepperBIN1, stepperBIN2), 3)

carAIN2 = 4
carAIN1 = 17
carPWMA = 18
carBIN1 = 27
carBIN2 = 22
carPWMB = 23
carSTBY = 24
car = Car(carSTBY, carPWMA, carAIN2, carAIN1, carBIN1, carBIN2, carPWMB)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# make the camera feed stuff I hope
def gen():
    global frame
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
@app.route('/videofeed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/detectionlogs')
def detectionLogJSON():
    try:
        # connect to DetectionLog Database
        con = sqlite.connect('../log/DetectionLogDB.db')
        cur = con.cursor()
        
        # store all the rows in the DetectionLog table in an array
        detectionLogArray = []
        for row in cur.execute("SELECT * FROM DetectionLogs ORDER BY Datetime(Date) DESC LIMIT 20;"):
            detectionLogArray.insert(0, { "Date": row[0], "Type": row[1], "Image": row[2] })
        
        # output array as JSON for the client to use
        return json.dumps(detectionLogArray)

    except sqlite.Error as e:
        print("Error %s:" % e.args[0])
        return

@app.route('/tankactive', methods=['POST'])
def tankActive():
    global tankActive
    tankActive = int(request.form['tankActive'])
    if tankActive:
        cannon.activate()
    else:
        cannon.deactivate()
        car.reset()
    
    return ""

@app.route('/autoactive', methods=['POST'])
def autoActive():
    global autoActive
    autoActive = int(request.form['autoActive'])
    
    return ""

@app.route('/carcontrol', methods=['POST'])
def carControl():
    global tankActive, autoActive
    if not tankActive:
        return ""
    steering = int(request.form['steering'])
    # -1 = left, 0 = off, 1 = right
    car.changeSteering(steering)
    drive = int(request.form['drive'])
    # -1 = reverse, 0 = off, 1 = forward
    car.changeDrive(drive)
    return ""

@app.route('/cannoncontrol', methods=['POST'])
def cannonControl():
    global tankActive, autoActive
    if not tankActive or autoActive:
        return ""
    canState = int(request.form['cannonState'])
    cannon.fireCannon(canState)
    baseAngle = int(request.form['cannonBaseAngle'])
    cannon.setBaseRotation(baseAngle)
    canAngle = int(request.form['cannonAngle'])
    cannon.setCannonAngle(canAngle)
    return ""

def runAutoDetection():
    global tankActive, autoActive, frame
    autoActive = 0
    
    shirt_cascade = cv2.CascadeClassifier('body.xml')
    print(cv2.__version__)
    vs = PiVideoStream().start()
    time.sleep(2.0)
    # connect to DetectionLog Database
    con = sqlite.connect('../log/DetectionLogDB.db')
    cur = con.cursor()
    pic_number = 0
    center_prevX = 0
    center_prevY = 0
    while True:
        if not tankActive or not autoActive:
            continue
        # captures frames individually from camera
        frame = vs.read()
        frame = imutils.resize(frame, width=240)
        # convert to grayscale for cascade detection
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        shirts = shirt_cascade.detectMultiScale(gray, 1.02, 5)
        # draws rectangle around any objects detected
        for (x,y,w,h) in shirts:
            # rectangle is half the height of body detected
            cv2.rectangle(frame,(x,y),(x+w,y+(h/2)),(255,255,0),2)
            center_x = int(x) + (int(w)/2)
            center_y = int(y) + (int(h)/2)
            #print("Coordinates of center are x:" + str((int(x) + int(w)/2)) + " y: " + str((int(y) + int(h)/2)))
            # check for large movements of the box to indicate unique target? idk? maybe? hopefully?
            if (center_x - center_prevX) > 20 or (center_prevX - center_x) > 20 \
                or (center_y - center_prevY) > 20 or (center_prevY - center_y) > 20:
                # checks if filename exists already, if not then writes file appending number that does not exist yet
                while os.path.exists('static/img/image%s.jpeg' % pic_number):
                    cv2.imwrite('static/img/image%s.jpeg' % pic_number, frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    # write timestamp, detection type, and image to SQLite db
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S") 
                    detection_type = "unknown"
                    image_name = ("image%s.jpeg" % pic_number)
                    cur.execute('INSERT INTO DetectionLogs(Date, Type, Image) VALUES(?,?,?);', (current_time, detection_type, image_name))
                    con.commit()
                    pic_number += 1
            cannon.setCannonPos(center_x, center_y)
            cannon.fireCannon(1)
        # resize frame to 480p
        frame = cv2.resize(frame,(640,480))
        # write frames individually to stream.jpeg (definitely can be done better but can't do tests right now)
        #cv2.imwrite('static/stream.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
        # maybe making frame a global will do the trick and we can remove this? just maybe

if __name__ == '__main__':
    try:
        t1 = Thread(target = runAutoDetection)
        t1.setDaemon(True)
        t1.start()
        app.run(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        t1.stop()
        vs.stop()
        pass

cannon.stop()