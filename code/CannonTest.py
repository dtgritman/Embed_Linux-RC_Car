import pigpio
from Cannon import TankCannon, StepperMotor


pinCannon = 20
pinServo = 21
AIN2 = 5
AIN1 = 6
BIN1 = 19
BIN2 = 26

#initialize pi for pigpio and check if connected
pi = pigpio.pi()
if not pi.connected:
    print("Pi not connected to pigpio.")
    exit()

cannon = TankCannon(pi, pinCannon, pinServo, StepperMotor(pi, AIN1, AIN2, BIN1, BIN2), 3)

try:
    while True:
        control = input("Enter f (laser), b (base rotation), or v (cannon angle): ")
        try:
            if control == "f":
                control = input("Set Cannon off/on (0/1): ")
                if int(control) == 1:
                    cannon.fireCannon(1)
                else:
                    cannon.fireCannon(0)
            elif control == "b":
                control = input("Set Base Rotation (in degrees): ")
                cannon.setBaseRotation(int(control))
            elif control == "v":
                control = input("Set Cannon Angle (in degrees): ")
                cannon.setCannonAngle(int(control))
        except:
            print("Hmm, seems like you don't know how to enter a number")
except KeyboardInterrupt:
    print('Done!')

finally:
    cannon.stop()
    pi.stop()
