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
            for i in range(len(sensors)):
                if sensors[i] > 0:
                    self.pi.set_mode(sensors[i], pigpio.INPUT)
        
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
            startT = 0
            for sensor in range(len(self.sensors)):
                endT = 0
                while self.pi.read(self.sensors[sensor]):
                    endT = time.time()
        
                if startT == 0 or endT == 0:
                    self.pi.write(self.sensorTrig, True)
                    time.sleep(0.00001)
                    self.pi.write(self.sensorTrig, False)
                    while not self.pi.read(self.sensors[sensor]):
                        startT = time.time()
                    while self.pi.read(self.sensors[sensor]):
                        endT = time.time()
                # convert sound travel time to distance 
                self.distances[sensor] = (endT - startT) * 17150
    
    # shut everything off and disconnect from pi
    def stop(self):
        self.deactivate()
        self.pi.stop()
