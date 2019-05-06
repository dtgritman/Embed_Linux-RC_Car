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
        control = input("Enter Change Angle (in degrees): ")
        if control == "f":
            cannon.fireCannonToggle()
        elif control == "b":
            control = input("Set Base Rotation (in degrees): ")
            control = float(control)
            cannon.setBaseRotation(control)
        else:
            try:
                angle = int(control)
                if curAngle + angle >= 0 and curAngle + angle <= 180:
                    curAngle = curAngle + angle
                    cannon.changeVAngle(angle)
                else:
                    print("Angle out of range.")
            except:
                print("Input must be an inter or f.")
except KeyboardInterrupt:
    cannon.changeVAngle(0 - curAngle)
    print('Done!')

finally:
    GPIO.cleanup()
