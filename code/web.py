from flask import Flask, render_template, request
import sqlite3 as sqlite
import json
from Cannon import TankCannon, StepperMotor

pinCannon = 20
pinServo = 21
AIN2 = 5
AIN1 = 6
BIN1 = 19
BIN2 = 26

cannon = TankCannon(pinCannon, pinServo, StepperMotor(AIN1, AIN2, BIN1, BIN2), 3)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detectionlogs')
def detectionLogJSON():
    try:
        # connect to DetectionLog Database
        con = sqlite.connect('log/DetectionLogDB.db')
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
    except KeyboardInterrupt:
        pass

cannon.stop()