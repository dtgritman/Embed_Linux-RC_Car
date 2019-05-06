import RPi.GPIO as GPIO
from Cannon import TankCannon, StepperMotor


pinCannon = 20
pinServo = 21
AIN2 = 5
AIN1 = 6
BIN1 = 19
BIN2 = 26

GPIO.setmode(GPIO.BCM)
cannon = TankCannon(GPIO, pinCannon, pinServo, StepperMotor(GPIO, AIN1, AIN2, BIN1, BIN2), 3)

curAngle = 0
try:
    while True:
        control = input("Enter f (laser toggle), b (base rotation), or v (vertical angle): ")
        try:
            if control == "f":
                cannon.fireCannonToggle()
            elif control == "b":
                control = input("Set Base Rotation (in degrees): ")
                control = float(control)
                cannon.setBaseRotation(control)
            else:
                cannon.setVAngle(int(control))
        except:
            print("Hmm, seems like you don't know how to enter a number")
except KeyboardInterrupt:
    cannon.setVAngle(-90)
    print('Done!')

finally:
    GPIO.cleanup()
