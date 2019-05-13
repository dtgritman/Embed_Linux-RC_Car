from evdev import InputDevice, ecodes
from ps4controllercodes import *
from Drone.Cannon import TankCannon, StepperMotor
import time
import os

def tank(tank):
    controllerFile = "/dev/input/event2"
    
    while not os.path.exists(controllerFile):
        print("{} - Controller Not Found!".format(time.strftime("%H:%M:%S")))
        for i in range(30):
            if not os.path.exists(controllerFile):
                time.sleep(1)
        time.sleep(1)
    
    #creates object 'controller' to store the data
    controller = InputDevice(controllerFile)
    #prints out device info at start
    print(controller)
    
    #setup variables to track controller
    cannonState = False
    curR1Trig = 0
    curLJsX = 127
    curLJsY = 127
    curRJsX = 127
    curRJsY = 127
    
    # activate cannon
    cannon.activate()
    
    paused = False
    try:
        #evdev takes care of polling the controller in a loop
        for event in controller.read_loop():
            if paused:
                if event.type == ecodes.EV_KEY and event.code == BTN.option and event.value == 1:
                    paused = False
                    cannon.activate()
                continue
            
            if event.type == ecodes.EV_KEY:
                if event.code == BTN.option:
                    if event.value == 1:
                        paused = True
                        print("Input Paused!")
                        cannon.deactivate()
                        continue
                elif event.code == BTN.x:
                    if event.value == 1:
                        cannonState = not cannonState
                        tank.fireCannon(cannonState)
                
                elif event.code == TRIG.r1:
                    curR1Trig = event.value
            
            elif event.type == ecodes.EV_ABS:
                #Range is 0 to 255, Center values are about 127 (up/left: below 127, down/right: above 127)
                if event.code == JS.right_x:
                    curRJsX = event.value
                elif event.code == JS.right_y:
                    curRJsY = event.value
            
            servoPos = 0
            if curRJsX < 121:
                servoPos = (-45 / 122) * (122 - curRJsX)
            elif curRJsX > 133:
               servoPos = (45 / 122) * (curRJsX - 133)
            
            stepperPos = 0
            if curRJsY < 121:
                stepperPos = (90 / 122) * (122 - curRJsY)
            elif curRJsY > 131:
                stepperPos = (-90 / 122) * (curRJsY - 133)
            
            
            tank.setBaseRotation(int(servoPos))
            tank.setCannonAngle(int(stepperPos))
            print("CannonState: {}, ServoPos: {}, StepperPos: {}".format(cannonState, int(servoPos), int(stepperPos)))
        
    except OSError:
        print("{} - Controller Disconnected!".format(time.strftime("%H:%M:%S")))
        return True
    
    except KeyboardInterrupt:
        print("\nConnection Closed!")
        return False


#------------ MAIN ------------
pinCannon = 20
pinServo = 21
AIN2 = 5
AIN1 = 6
BIN1 = 19
BIN2 = 26

cannon = TankCannon(pinCannon, pinServo, StepperMotor(AIN1, AIN2, BIN1, BIN2), 3)
try:
    # run cannon while controller connected
    while tank(cannon):
        # if controller disconnected: stop tank
        cannon.deactivate()
        time.sleep(5)

except KeyboardInterrupt:
    print("\nConnection Closed!")

finally:
    cannon.stop()