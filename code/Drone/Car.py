import time 
import RPi.GPIO as GPIO

class Car:

    def __init__(self, STBY, PWMA, AIN2, AIN1, BIN1, BIN2, PWMB):
        GPIO.setmode(GPIO.BOARD)

        self.STBY = STBY
        # Drive motor
        self.speed_drive = PWMA
        self.AIN1 = AIN1
        self.AIN2 = AIN2
        # Left-Right controller
        self.LR_ON = PWMB
        self.BIN1 = BIN1
        self.BIN2 = BIN2

        GPIO.setup(PWMA, GPIO.OUT)  # Connected to PWMA 
        GPIO.setup(AIN2, GPIO.OUT)  # Connected to AIN2
        GPIO.setup(AIN1, GPIO.OUT)  # Connected to AIN1 

        GPIO.setup(STBY, GPIO.OUT)  # Connected to STBY 

        GPIO.setup(BIN1, GPIO.OUT)  # Connected to BIN1 
        GPIO.setup(BIN2, GPIO.OUT)  # Connected to BIN2 
        GPIO.setup(PWMB, GPIO.OUT)  # Connected to PWMB
    
    def changeDrive(self, direction):
        if direction == 1:
            GPIO.output(AIN1, GPIO.HIGH)
            GPIO.output(AIN2, GPIO.LOW)
        elif direction == -1:
            GPIO.output(AIN1, GPIO.LOW)
            GPIO.output(AIN2, GPIO.HIGH)
        else:
            GPIO.output(AIN1, GPIO.LOW)
            GPIO.output(AIN2, GPIO.LOW)
    
    def changeSteering(self, direction):
        if direction == 1:
            GPIO.output(BIN1, GPIO.HIGH)
            GPIO.output(BIN2, GPIO.LOW)
        elif direction == -1:
            GPIO.output(BIN1, GPIO.LOW)
            GPIO.output(BIN2, GPIO.HIGH)
        else:
            GPIO.output(BIN1, GPIO.LOW)
            GPIO.output(BIN2, GPIO.LOW)
    
    def reset(self):
        GPIO.output(self.STBY, GPIO.LOW)

        GPIO.output(self.speed_drive, GPIO.LOW)
        GPIO.output(self.AIN1, GPIO.LOW)
        GPIO.output(self.AIN2, GPIO.LOW)

        GPIO.output(self.LR_ON, GPIO.LOW)
        GPIO.output(self.BIN1, GPIO.LOW)
        GPIO.output(self.BIN2, GPIO.LOW)