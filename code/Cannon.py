from time import sleep


class TankCannon:
    def __init__(self, GPIO, angleStepperMotor, gearRatio=1):
        self.GPIO = GPIO
        self.angleStepper = angleStepperMotor
        self.gearRatio = gearRatio
    
    def changeAngle(self, degrees):
        steps = int((degrees * self.gearRatio) / (360 / self.angleStepper.steps))
        if degrees < 0:
            self.angleStepper.stepRev(self.GPIO, 0 - steps)
        else:
            self.angleStepper.stepFwd(self.GPIO, steps)

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
    
    def stepFwd(self, GPIO, steps=1):
        for i in range(steps):
            self.lastStep_seq += 1
            #restart sequence if it reaches max
            if self.lastStep_seq >= len(self.step_seq):
                self.lastStep_seq = 0
                
            #step motor forward
            GPIO.output(self.pins, self.step_seq[self.lastStep_seq])
            sleep(self.stepTime)

    def stepRev(self, GPIO, steps=1):
        for i in range(steps):
            self.lastStep_seq -= 1
            #restart sequence if it reaches 0
            if self.lastStep_seq < 0:
                self.lastStep_seq = len(self.step_seq) - 1
                
            #step motor backwards
            GPIO.output(self.pins, self.step_seq[self.lastStep_seq])
            sleep(self.stepTime)