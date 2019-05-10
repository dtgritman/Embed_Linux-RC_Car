from time import sleep
import pigpio

class TankCannon:
    def __init__(self, pi, pin_Cannon, pin_RotationServo, angleStepperMotor, stepper_GearRatio=1, cannonRelay_active="HIGH", rotationServo_Offset=0):
        self.pi = pi
        
        # GPIO pin locations
        self.cannonPin = pin_Cannon
        self.rotationServoPin = pin_RotationServo
        
        # initialize GPIO
        self.pi.set_mode(pin_Cannon, pigpio.OUTPUT)
        self.pi.set_mode(pin_RotationServo, pigpio.OUTPUT)
        self.pi.set_PWM_frequency(pin_RotationServo, 300)
        
        # set servo values
        self.rotationServoMin = 1000
        self.rotationServoMax = 2000
        self.rotationServoMid = ((self.rotationServoMax - self.rotationServoMin) / 2) + self.rotationServoMin + rotationServo_Offset
        self.rotationServoAngleConversion = (self.rotationServoMax - self.rotationServoMin) / 180
        
        # set stepper min and max
        self.angleStepperMin = -90
        self.angleStepperMax = 90
        self.angleStepperConversion = 360 / (angleStepperMotor.steps * stepper_GearRatio)
        
        # set variables
        self.angleStepper = angleStepperMotor
        self.stepperGearRatio = stepper_GearRatio
        if cannonRelay_active.upper() == 'HIGH':
            self.cannonStates = [1, 0]
        else:
            self.cannonStates = [0, 1]
        
        # make sure cannon is inactive at start
        self.fireCannon(0)
        # initialize stepper motor angle
        self.curVAngle = -90
        self.setCannonAngle(0)
    
    def setCannonAngle(self, degrees):
        # limit vertical angle
        if  degrees > self.angleStepperMax:
            degrees = self.angleStepperMax
        elif degrees < self.angleStepperMin:
            degrees = self.angleStepperMin
        
        changeDegrees = degrees - self.curVAngle
        
        steps = int(changeDegrees / self.angleStepperConversion)
        self.curVAngle = round(self.curVAngle + steps * self.angleStepperConversion, 2)
        
        if changeDegrees < 0:
            self.angleStepper.stepRev(0 - steps)
        else:
            self.angleStepper.stepFwd(steps)
    
    def setBaseRotation(self, degrees):
        if degrees < -45:
            degrees = -45
        elif degrees > 45:
            degrees = 45
        
        self.pi.set_servo_pulsewidth(self.rotationServoPin, self.rotationServoMid + (degrees * self.rotationServoAngleConversion))
    
    def fireCannon(self, state):
        self.pi.write(self.cannonPin, self.cannonStates[state])
    
    def stop(self):
        self.setCannonAngle(-90) # set cannon angle to resting postion
        self.fireCannon(0) # shut off cannon
        self.pi.set_servo_pulsewidth(self.rotationServoPin, 0) # shut off servo motor
        self.angleStepper.stop() # shut off stepper motor

class StepperMotor:
    step_seq = [
        (1,1,0,0),
        (0,1,1,0),
        (0,0,1,1),
        (1,0,0,1)
    ]
    lastStep_seq = 0
    
    def __init__(self, pi, pin_INA1, pin_INA2, pin_INB1, pin_INB2, motorSteps=200, motorRpm=50):
        self.pi = pi
        
        # initialize GPIO
        self.pi.set_mode(pin_INA1, pigpio.OUTPUT)
        self.pi.set_mode(pin_INA2, pigpio.OUTPUT)
        self.pi.set_mode(pin_INB1, pigpio.OUTPUT)
        self.pi.set_mode(pin_INB2, pigpio.OUTPUT)
        
        self.steps = motorSteps
        self.rpm = motorRpm
        self.pins = (pin_INA1, pin_INB1, pin_INA2, pin_INB2)
        self.stepTime = motorSteps * motorRpm / 60000 / 100 # steps * rev/min * 60000ms / min 
    
    def stepFwd(self, steps):
        for i in range(steps):
            self.lastStep_seq += 1
            # restart sequence if it reaches max
            if self.lastStep_seq >= len(self.step_seq):
                self.lastStep_seq = 0
                
            # step motor forward
            #self.pi.write(self.pins, self.step_seq[self.lastStep_seq])
            for pin in range(4):
                self.pi.write(self.pins[pin], self.step_seq[self.lastStep_seq][pin])
            sleep(self.stepTime)

    def stepRev(self, steps):
        for i in range(steps):
            self.lastStep_seq -= 1
            # restart sequence if it reaches 0
            if self.lastStep_seq < 0:
                self.lastStep_seq = len(self.step_seq) - 1
                
            # step motor backwards
            #self.pi.write(self.pins, self.step_seq[self.lastStep_seq])
            for pin in range(4):
                self.pi.write(self.pins[pin], self.step_seq[self.lastStep_seq][pin])
            sleep(self.stepTime)
    
    def stop(self):
        # set all pins to off
        for pin in range(4):
            self.pi.write(self.pins[pin], 0)