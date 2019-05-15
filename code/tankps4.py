from evdev import InputDevice, ecodes
from ps4controllercodes import *
from Drone.Cannon import TankCannon, StepperMotor
from Drone.Car import Car
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
    curL2Trig = 0
    curR2Trig = 0
    curLJs = { "x": 127, "y": 127 }
    curRJs = { "x": 127, "y": 127 }
    
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
                    car.activate()
                continue
            
            if event.type == ecodes.EV_KEY:
                if event.code == BTN.option:
                    if event.value == 1:
                        paused = True
                        print("Input Paused!")
                        cannon.deactivate()
                        car.deactivate()
                        continue
                elif event.code == TRIG.r1:
                    if event.value == 1:
                        cannonState = not cannonState
                        tank.fireCannon(cannonState)
            
            elif event.type == ecodes.EV_ABS:
                #Range is 0 to 255
                if event.code == TRIG.hold_l2:
                    curL2Trig = event.value
                elif event.code == TRIG.hold_r2:
                    curR2Trig = event.value
                
                #Range is 0 to 255, Center values are about 127 (up/left: below 127, down/right: above 127)
                elif event.code == JS.left_x:
                    curLJs["x"] = event.value
                elif event.code == JS.left_y:
                    curLJs["y"] = event.value
                #Range is 0 to 255, Center values are about 127 (up/left: below 127, down/right: above 127)
                elif event.code == JS.right_x:
                    curRJs["x"] = event.value
                elif event.code == JS.right_y:
                    curRJs["y"] = event.value
            
            steerDir = 0
            steerPerc = 0
            if curLJs.get("x") < 121:
                steerDir = -1
                steerPerc = ((122 - curLJs.get("x")) / 122) * 100
            elif curLJs.get("x") > 133:
                steerDir = 1
                steerPerc = ((curLJs.get("x") - 133) / 122) * 100
            
            driveDir = 0
            drivePerc = 0
            if curR2Trig - curL2Trig > 0:
                driveDir = 1
                drivePerc = ((curR2Trig - curL2Trig) / 255) * 100
            elif curL2Trig - curR2Trig > 0:
                driveDir = -1
                drivePerc = ((curL2Trig - curR2Trig) / 255) * 100
            
            basePos = 0
            if curRJs.get("x") < 121:
                basePos = (-45 / 122) * (122 - curRJs.get("x"))
            elif curRJs.get("x") > 133:
               basePos = (45 / 122) * (curRJs.get("x") - 133)
            
            stepperPos = 0
            if curRJs.get("y") < 121:
                stepperPos = (90 / 122) * (122 - curRJs.get("y"))
            elif curRJs.get("y") > 133:
                stepperPos = (-90 / 122) * (curRJs.get("y") - 133)
            
            car.setSteering(steerDir, int(steerPerc))
            car.setDrive(driveDir, int(drivePerc))
            tank.setBaseRotation(int(basePos))
            tank.setCannonAngle(int(stepperPos))
            print("Cannon: {}, Base: {}, Stepper: {}, Drive: {}|{}%, Steer: {}|{}%".format(cannonState, int(basePos), int(stepperPos), driveDir, int(drivePerc), steerDir, int(steerPerc)))
        
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

carSTBY = 27
carPWMA = 4
carAIN2 = 17
carAIN1 = 18
carBIN1 = 22
carBIN2 = 23
carPWMB = 24
car = Car(carSTBY, carPWMA, carAIN2, carAIN1, carBIN1, carBIN2, carPWMB)
try:
    # run cannon while controller connected
    while tank(cannon):
        # if controller disconnected: stop tank
        cannon.deactivate()
        car.deactivate()
        time.sleep(5)

except KeyboardInterrupt:
    print("\nConnection Closed!")

finally:
    cannon.stop()
