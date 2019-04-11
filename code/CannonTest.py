import RPi.GPIO as GPIO
from Cannon import TankCannon, StepperMotor


AIN2 = 5
AIN1 = 6
BIN1 = 19
BIN2 = 26

GPIO.setmode(GPIO.BCM)
cannon = TankCannon(GPIO, StepperMotor(GPIO, AIN1, AIN2, BIN1, BIN2), 3)

try:
    while True:
        control = input("Enter Change Angle (in degrees): ")
        cannon.changeAngle(int(control))

except KeyboardInterrupt:
    print('Done!')

finally:
    GPIO.cleanup()
