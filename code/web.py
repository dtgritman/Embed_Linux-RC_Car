from flask import Flask, render_template
import sqlite3 as sqlite
import json

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
