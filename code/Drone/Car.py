import pigpio

class Car:
    def __init__(self, STBY, PWMA, AIN2, AIN1, BIN1, BIN2, PWMB):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Pi not connected to pigpio.")
            return
        
        # GPIO Pin locations
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
        
        # setup car
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
    
    # shut everything off and disconnect from pi
    def stop(self):
        self.deactivate()
        self.pi.stop()