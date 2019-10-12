# imports
from flask import Flask, render_template, request, Response
from threading import Thread
import sqlite3 as sqlite
import json
import time
import cv2
import numpy as np
import imutils
import os

# import custom car classes
from camerapi import VideoCamera
from Drone.Cannon import TankCannon, StepperMotor
from Drone.Car import Car

# tank starts actived and in manual mode
tankActive = 1
autoActive = 0
streamFrame = None
streamActive = True

# cannon gpio pins and intialization
pinCannon = 20
pinServo = 21
stepperAIN2 = 5
stepperAIN1 = 6
stepperBIN1 = 19
stepperBIN2 = 26
cannon = TankCannon(pinCannon, pinServo, StepperMotor(stepperAIN1, stepperAIN2, stepperBIN1, stepperBIN2), stepper_GearRatio=3, rotationServo_Offset=50)

# car gpio pins and intialization
carSTBY = 17
carPWMA = 3
carAIN2 = 4
carAIN1 = 18
carBIN1 = 27
carBIN2 = 23
carPWMB = 24
# car distance sensors gpio pins
distanceTrig = 22
distanceEchoL = 10
distanceEchoF = 9
distanceEchoR = 11
car = Car(carSTBY, carPWMA, carAIN2, carAIN1, carBIN1, carBIN2, carPWMB, distanceTrig, [distanceEchoL, distanceEchoF, distanceEchoR])


app = Flask(__name__)

@app.route('/')
def index():
    global tankActive, autoActive
    tankActive = 1
    autoActive = 0
    cannon.activate()
    car.activate()
    return render_template('index.html')

# get the camera feed output
def gen():
    global streamFrame, streamActive
    frame = open('static/img/loading.jpg', 'rb').read()
    while streamActive:
        if streamFrame != None:
            frame = streamFrame
        
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
    return ""

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
        car.activate()
    else:
        cannon.deactivate()
        car.deactivate()
    
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
    
    # -1 = left, 0 = off, 1 = right
    steerDir = 0
    # steering motor speed percent
    steerPerc = int(request.form['steering'])
    if steerPerc > 0:
        steerDir = 1
    elif steerPerc < 0:
        steerDir = -1
        steerPerc = -steerPerc
    
    car.setSteering(steerDir, steerPerc)
    
    # -1 = reverse, 0 = off, 1 = forward
    driveDir = 0
    # drive motor speed percent
    drivePerc = int(request.form['drive'])
    if drivePerc > 0:
        driveDir = 1
    elif drivePerc < 0:
        driveDir = -1
        drivePerc = -drivePerc
    
    car.setDrive(driveDir, drivePerc)
    
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

# the threaded function that runs the camera and the auto mode
def runAutoDetection():
    global tankActive, autoActive, streamFrame, streamActive
    tankActive = 1
    autoActive = 0
    streamActive = True
    camera = VideoCamera()
    
    # setup connection to DetectionLog Database
    con = sqlite.connect('../log/DetectionLogDB.db')
    cur = con.cursor()
    logPictureNum = 0
    
    # find current picture number to start at
    while os.path.exists('static/img/image%s.jpg' % logPictureNum):
        logPictureNum += 1
    
    prevDetectCoords = [0, 0]
    
    while streamActive:
        '''
        # Distance sensor reading causes hang up in code
        car.updateDistances()
        print(car.distances)
        '''
        
        # get the current frame and detection coords
        streamImage, detectCoords = camera.get_frame()
        ret, jpeg = cv2.imencode('.jpg', streamImage)
        streamFrame = jpeg.tobytes()
        
        # don't log or control the cannon when in manual mode
        if not tankActive or not autoActive:
            continue
        
        # check if something is detected
        if detectCoords[0] > -1:
            # check for large movements of the center of the box, to indicate unique target for logging
            if abs(detectCoords[0] - prevDetectCoords[0]) > 20 or abs(detectCoords[1] - prevDetectCoords[1]) > 20:
                cv2.imwrite('static/img/image%s.jpg' % logPictureNum, streamImage, [cv2.IMWRITE_JPEG_QUALITY, 90])
                # write timestamp, detection type, and image to SQLite db
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                detection_type = "unknown"
                image_name = ("image%s.jpg" % logPictureNum)
                cur.execute('INSERT INTO DetectionLogs(Date, Type, Image) VALUES (?,?,?);', (current_time, detection_type, image_name))
                con.commit()
                logPictureNum += 1
            
            cannon.setCannonPos(detectCoords[0], detectCoords[1], camera.resolution[0], camera.resolution[1])
            cannon.fireCannon(1)
            # store the detection coordinates for reference later
            prevDetectCoords = detectCoords
        else:
            cannon.fireCannon(0)


if __name__ == '__main__':
    t1 = Thread(target = runAutoDetection)
    t1.setDaemon(True)
    t1.start()
    app.run(host='0.0.0.0', port=8080, threaded=True)
    streamActive = False

print("Exiting...")
cannon.stop()
car.stop()
