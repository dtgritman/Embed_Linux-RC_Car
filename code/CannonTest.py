import RPi.GPIO as GPIO
from Cannon import TankCannon, StepperMotor


pinCannon = 21
AIN2 = 5
AIN1 = 6
BIN1 = 19
BIN2 = 26

GPIO.setmode(GPIO.BCM)
cannon = TankCannon(GPIO, pinCannon, StepperMotor(GPIO, AIN1, AIN2, BIN1, BIN2), 3)

curAngle = 0
try:
    while True:
        control = input("Enter Change Angle (in degrees): ")
        if control == "f":
            cannon.fireCannonToggle()
        else:
            try:
                angle = int(control)
                if curAngle + angle >= 0 and curAngle + angle <= 180:
                    curAngle = curAngle + angle
                    cannon.changeAngle(angle)
                else:
                    print("Angle out of range.")
            except:
                print("Input must be an inter or f.")
except KeyboardInterrupt:
    cannon.changeAngle(0 - curAngle)
    print('Done!')

finally:
    GPIO.cleanup()
