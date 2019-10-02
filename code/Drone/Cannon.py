from time import sleep
import pigpio

class TankCannon:
    def __init__(self, pin_Cannon, pin_RotationServo, angleStepperMotor, stepper_GearRatio=1, cannonRelay_active="HIGH", rotationServo_Offset=0):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Pi not connected to pigpio.")
            return
        
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
        self.rotationServoAngleConversion = (self.rotationServoMax - self.rotationServoMin) / 180.0
        
        # set stepper min and max
        self.angleStepperMin = -90.0
        self.angleStepperMax = 90.0
        self.angleStepperConversion = 360.0 / (angleStepperMotor.steps * stepper_GearRatio)
        
        # set variables
        self.angleStepper = angleStepperMotor
        self.stepperGearRatio = stepper_GearRatio
        if cannonRelay_active.upper() == 'HIGH':
            self.cannonStates = [1, 0]
        else:
            self.cannonStates = [0, 1]
        
        
        self.curVAngle = -90.0 # cannon starts off facing down
        self.active = 0
        self.activate()
        
    # initialize cannon and motors
    def activate(self):
        self.active = 1
        # make sure cannon is inactive at start
        self.fireCannon(0)
        # set servo to middle
        self.setBaseRotation(0)
        # initialize stepper motor angle
        self.setCannonAngle(0)
    
    # turn the cannon and motors off
    def deactivate(self):
        # center the servo motor
        self.pi.set_servo_pulsewidth(self.rotationServoPin, self.rotationServoMid)
        # set cannon angle to resting postion and deactivate stepper motor
        self.setCannonAngle(-90.0)
        self.angleStepper.deactivate()
        # shut off cannon
        self.fireCannon(0)
        # shut off servo motor
        self.pi.set_servo_pulsewidth(self.rotationServoPin, 0)
        self.active = 0
    
    # set cannon position based on x,y coordinates
    def setCannonPos(self, x, y, width=320, height=240, fovX=54.0, fovY=41.0):
        midX = width / 2
        if x < midX:
            xDegrees = -(midX - x) * (fovX / width)
        else:
            xDegrees = (x - midX) * (fovX / width)
        self.setBaseRotation(xDegrees)
        
        midY = height / 2
        if y < midY:
            yDegrees = (midY - y) * (fovY / height)
        else:
            yDegrees = -(y - midY) * (fovY / height)
        self.setCannonAngle(yDegrees)
    
    # set the vertical angle of the cannon
    def setCannonAngle(self, degrees):
        if not self.active:
            return
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
    
    # set the rotation of the base
    def setBaseRotation(self, degrees):
        if not self.active:
            return
        if degrees < -45:
            degrees = -45
        elif degrees > 45:
            degrees = 45
        
        self.pi.set_servo_pulsewidth(self.rotationServoPin, self.rotationServoMid + (degrees * self.rotationServoAngleConversion))
    
    # set the cannon state (0: off, 1: on)
    def fireCannon(self, state):
        if not self.active:
            return
        self.pi.write(self.cannonPin, self.cannonStates[state])
    
    # deactivate the cannon and stop the connection to the pigpio
    def stop(self):
        self.deactivate()
        self.pi.stop()

class StepperMotor:
    step_seq = [
        (1,1,0,0),
        (0,1,1,0),
        (0,0,1,1),
        (1,0,0,1)
    ]
    
    def __init__(self, pin_INA1, pin_INA2, pin_INB1, pin_INB2, motorSteps=200, motorRpm=130):
        self.pi = pigpio.pi()
        if not self.pi.connected:
            print("Pi not connected to pigpio.")
            return
        
        # initialize GPIO
        self.pi.set_mode(pin_INA1, pigpio.OUTPUT)
        self.pi.set_mode(pin_INA2, pigpio.OUTPUT)
        self.pi.set_mode(pin_INB1, pigpio.OUTPUT)
        self.pi.set_mode(pin_INB2, pigpio.OUTPUT)
        
        self.steps = motorSteps
        self.rpm = motorRpm
        self.pins = (pin_INA1, pin_INB1, pin_INA2, pin_INB2)
        self.stepTime = 60.0 / (motorRpm * motorSteps)
        
        self.lastStep_seq = 4
    
    # deactivate the stepper motor
    def deactivate(self):
        # set all pins to off
        for pin in range(4):
            self.pi.write(self.pins[pin], 0)
    
    # move the stepper motor CW a number of steps
    def stepFwd(self, steps):
        for i in range(steps):
            self.lastStep_seq += 1
            # restart sequence if it reaches max
            if self.lastStep_seq >= len(self.step_seq):
                self.lastStep_seq = 0
                
            # step motor forward
            for pin in range(4):
                self.pi.write(self.pins[pin], self.step_seq[self.lastStep_seq][pin])
            sleep(self.stepTime)
    
    # move the stepper motor CCW a number of steps
    def stepRev(self, steps):
        for i in range(steps):
            self.lastStep_seq -= 1
            # restart sequence if it reaches 0
            if self.lastStep_seq < 0:
                self.lastStep_seq = len(self.step_seq) - 1
                
            # step motor backwards
            for pin in range(4):
                self.pi.write(self.pins[pin], self.step_seq[self.lastStep_seq][pin])
            sleep(self.stepTime)
    
    # deactive the stepper motor and stop the pigpio connection
    def stop(self):
        self.deactivate()
        self.pi.stop()
