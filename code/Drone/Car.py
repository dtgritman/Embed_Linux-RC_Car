import time
import pigpio

class Car:
    def __init__(self, STBY, PWMA, AIN2, AIN1, BIN1, BIN2, PWMB, sensorTrig=0, sensors=[]):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Pi not connected to pigpio.")
            return
        
        # GPIO Drive Pin locations
        self.STBY = STBY
        # drive motor
        self.drivePWM = PWMA
        self.driveIN1 = AIN1
        self.driveIN2 = AIN2
        # steering motor
        self.steerPWM = PWMB
        self.steerIN1 = BIN1
        self.steerIN2 = BIN2
        
        # initialize GPIO
        self.pi.set_mode(STBY, pigpio.OUTPUT)
        self.pi.set_mode(PWMA, pigpio.OUTPUT)
        self.pi.set_mode(AIN1, pigpio.OUTPUT)
        self.pi.set_mode(AIN2, pigpio.OUTPUT)
        self.pi.set_mode(PWMB, pigpio.OUTPUT)
        self.pi.set_mode(BIN1, pigpio.OUTPUT)
        self.pi.set_mode(BIN2, pigpio.OUTPUT)
        
        self.pi.set_PWM_frequency(PWMA, 50)
        self.pi.set_PWM_frequency(PWMB, 50)
        
        
        # Sensor GPIO Pin locations
        self.sensorTrig = sensorTrig
        self.sensors = sensors
        self.distances = []
        for i in range(len(sensors)):
            self.distances.append(0)
        
        # initialize sensor GPIO
        if sensorTrig > 0:
            self.pi.set_mode(sensorTrig, pigpio.OUTPUT)
            for sensor in range(len(sensors)):
                if sensors[sensor] > 0:
                    self.pi.set_mode(sensors[sensor], pigpio.INPUT)
        
        # activate car
        self.activate()
    
    # activate motors
    def activate(self): 
        self.deactivate()
        self.pi.write(self.STBY, 1)
    
    # shut off motors
    def deactivate(self):
        self.pi.write(self.STBY, 0)
        # shut off drive motor
        self.pi.write(self.driveIN1, 0)
        self.pi.write(self.driveIN2, 0)
        self.pi.set_PWM_dutycycle(self.drivePWM, 0)
        # shut off steering motor
        self.pi.write(self.steerIN1, 0)
        self.pi.write(self.steerIN2, 0)
        self.pi.set_PWM_dutycycle(self.steerPWM, 0)
        if self.sensorTrig > 0:
            # make sure sensors aren't triggered
            self.pi.write(self.sensorTrig, False)
    
    # set drive motor
    def setDrive(self, direction, dutycycle=100):
        dc = int((255.0 / 100.0) * dutycycle)
        if direction == 1:
            self.pi.write(self.driveIN1, 1)
            self.pi.write(self.driveIN2, 0)
            self.pi.set_PWM_dutycycle(self.drivePWM, dc)
        elif direction == -1:
            self.pi.write(self.driveIN1, 0)
            self.pi.write(self.driveIN2, 1)
            self.pi.set_PWM_dutycycle(self.drivePWM, dc)
        else:
            self.pi.write(self.driveIN1, 0)
            self.pi.write(self.driveIN2, 0)
            self.pi.set_PWM_dutycycle(self.drivePWM, 0)
    
    # set steering motor
    def setSteering(self, direction, dutycycle=100):
        dc = int((255.0 / 100.0) * dutycycle)
        if direction == 1:
            self.pi.write(self.steerIN1, 0)
            self.pi.write(self.steerIN2, 1)
            self.pi.set_PWM_dutycycle(self.steerPWM, dc)
        elif direction == -1:
            self.pi.write(self.steerIN1, 1)
            self.pi.write(self.steerIN2, 0)
            self.pi.set_PWM_dutycycle(self.steerPWM, dc)
        else:
            self.pi.write(self.steerIN1, 0)
            self.pi.write(self.steerIN2, 0)
            self.pi.set_PWM_dutycycle(self.steerPWM, 0)
    
    # update sensors distance
    def updateDistances(self):
        if self.sensorTrig > 0:
            for sensor in range(len(self.sensors)):
                while self.pi.read(self.sensors[sensor]):
                    continue
                # trigger the sensors so they start reading
                self.pi.write(self.sensorTrig, True)
                time.sleep(0.000001)
                self.pi.write(self.sensorTrig, False)
                # wait until the sensor starts reading, if it takes longer than .001 seconds then something went wrong
                startT = time.time()
                while not self.pi.read(self.sensors[sensor]) and time.time() - startT < .001:
                    continue
                startT = time.time()
                # wait for the sensor to become inactive which gives us the ending time
                while self.pi.read(self.sensors[sensor]):
                    continue
                endT = time.time()
                # convert the sensor readings to distance in centimeters
                self.distances[sensor] = round((endT - startT) * 17150, 2)
            
            '''
            # trial to read multiple sensors at once but was having issues
            # definitely can be optimized better and needs code hang detection
            startT = {}
            endT = {}
            self.pi.write(self.sensorTrig, True)
            time.sleep(0.0000001)
            self.pi.write(self.sensorTrig, False)
            sensorCount = len(self.sensors)
            while len(endT) < sensorCount:
                for sensor in range(sensorCount):
                    if sensor not in startT.keys():
                        if self.pi.read(self.sensors[sensor]):
                            startT[sensor] = time.time()
                    elif not sensor in endT.keys():
                        if not self.pi.read(self.sensors[sensor]):
                            endT[sensor] = time.time()
            for sensor in range(len(self.sensors)):
                self.distances[sensor] = round((endT[sensor] - startT[sensor]) * 17150, 2)
            '''
    
    # shut everything off and disconnect from pi
    def stop(self):
        self.deactivate()
        self.pi.stop()
