# imports
from flask import Flask, render_template, request
import sqlite3 as sqlite
import json
from Drone.Cannon import TankCannon, StepperMotor

from imutils.video.pivideostream import PiVideoStream
import io
import time
import cv2
import picamera
import picamera.array
import numpy as np
import imutils

pinCannon = 20
pinServo = 21
stepperAIN2 = 5
stepperAIN1 = 6
stepperBIN1 = 19
stepperBIN2 = 26

cannon = TankCannon(pinCannon, pinServo, StepperMotor(stepperAIN1, stepperAIN2, stepperBIN1, stepperBIN2), 3)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
    tankActive = int(request.form['tankActive'])
    if tankActive:
        cannon.activate()
    else:
        cannon.deactivate()
    
    return ""

@app.route('/carcontrol', methods=['POST'])
def carControl():
    steering = int(request.form['steering'])
    # -1 = left, 0 = off, 1 = right
    # TODO: Setup car steering
    drive = int(request.form['drive'])
    # -1 = reverse, 0 = off, 1 = forward
    # TODO: Setup car drive
    return ""

@app.route('/cannoncontrol', methods=['POST'])
def cannonControl():
    canState = int(request.form['cannonState'])
    cannon.fireCannon(canState)
    baseAngle = int(request.form['cannonBaseAngle'])
    cannon.setBaseRotation(baseAngle)
    canAngle = int(request.form['cannonAngle'])
    cannon.setCannonAngle(canAngle)
    return ""

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
        shirt_cascade = cv2.CascadeClassifier('body.xml')
        print(cv2.__version__)
        vs = PiVideoStream().start()
        time.sleep(2.0)
        while True:
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
                setCannonPos(center_x, center_y)
            # resize frame to 480p
            frame = cv2.resize(frame,(640,480))
            # write frames individually to test.jpeg
            cv2.imwrite('test.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    except KeyboardInterrupt:
        vs.stop()
        pass

cannon.stop()