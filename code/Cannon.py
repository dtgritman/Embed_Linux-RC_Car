from time import sleep


class TankCannon:
    def __init__(self, GPIO, pin_Cannon, pin_RotationServo, angleStepperMotor, stepper_GearRatio=1, rotationServo_Offset=0):
        self.GPIO = GPIO
        #initialize GPIO
        GPIO.setup(pin_RotationServo, GPIO.OUT)
        GPIO.setup(pin_Cannon, GPIO.OUT)
        GPIO.output(pin_Cannon, 1)
        
        #initialize servo and variables needed
        self.rotationServo_Min = 2
        self.rotationServo_Max = 12.5
        self.rotationServo_AngleConvert = (self.rotationServo_Max - self.rotationServo_Min) / 180
        self.rotationServoMid = ((self.rotationServo_Max - self.rotationServo_Min) / 2) + self.rotationServo_Min + rotationServo_Offset
        self.rotationServo = GPIO.PWM(pin_RotationServo, 50)
        self.rotationServo.start(0)
        
        #set variables
        self.cannonPin = pin_Cannon
        self.angleStepper = angleStepperMotor
        self.stepperGearRatio = stepper_GearRatio
        
        self.curVAngle = -90
    
    def changeVAngle(self, degrees):
        #limit vertical angle
        if curVAngle + degrees > 60:
            degrees = 60 - curVAngle
            curVAngle = 60
        elif curVAngle + degrees < -60:
            degrees = -60 - curVAngle 
            curVAngle = -60
        
        steps = int((degrees * self.stepperGearRatio) / (360 / self.angleStepper.steps))
        if degrees < 0:
            self.angleStepper.stepRev(self.GPIO, 0 - steps)
        else:
            self.angleStepper.stepFwd(self.GPIO, steps)
    
    def setBaseRotation(self, degrees):
        if degrees < -45:
            degrees = -45
        elif degrees > 45:
            degrees = 45
        
        self.rotationServo.ChangeDutyCycle(self.rotationServoMid + (degrees * self.rotationServo_AngleConvert))
    
    def fireCannonToggle(self):
        self.GPIO.output(self.cannonPin, not self.GPIO.input(self.cannonPin))

class StepperMotor:
    step_seq = [
        (1,1,0,0),
        (0,1,1,0),
        (0,0,1,1),
        (1,0,0,1)
    ]
    lastStep_seq = 0
    
    def __init__(self, GPIO, pin_INA1, pin_INA2, pin_INB1, pin_INB2, motorSteps=200, motorRpm=50):
        GPIO.setup(pin_INA1, GPIO.OUT)
        GPIO.setup(pin_INA2, GPIO.OUT)
        GPIO.setup(pin_INB1, GPIO.OUT)
        GPIO.setup(pin_INB2, GPIO.OUT)
        self.steps = motorSteps
        self.rpm = motorRpm
        self.pins = (pin_INA1, pin_INB1, pin_INA2, pin_INB2)
        self.stepTime = motorSteps * motorRpm / 60000 / 100 # steps * rev/min * 60000ms / min 
    
    def stepFwd(self, GPIO, steps):
        for i in range(steps):
            self.lastStep_seq += 1
            #restart sequence if it reaches max
            if self.lastStep_seq >= len(self.step_seq):
                self.lastStep_seq = 0
                
            #step motor forward
            GPIO.output(self.pins, self.step_seq[self.lastStep_seq])
            sleep(self.stepTime)

    def stepRev(self, GPIO, steps):
        for i in range(steps):
            self.lastStep_seq -= 1
            #restart sequence if it reaches 0
            if self.lastStep_seq < 0:
                self.lastStep_seq = len(self.step_seq) - 1
                
            #step motor backwards
            GPIO.output(self.pins, self.step_seq[self.lastStep_seq])
            sleep(self.stepTime)