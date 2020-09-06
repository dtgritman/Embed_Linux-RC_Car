import time
from Drone.Car import Car

# car gpio pins and intialization
carSTBY = 17
carPWMA = 3
carAIN2 = 4
carAIN1 = 18
carBIN1 = 27
carBIN2 = 23
carPWMB = 24
# car distance sensors gpio pins
distanceTrig = 22
distanceEchoL = 9
distanceEchoF = 11
distanceEchoR = 10
car = Car(carSTBY, carPWMA, carAIN2, carAIN1, carBIN1, carBIN2, carPWMB, distanceTrig, [distanceEchoL, distanceEchoF, distanceEchoR])

try:
    sideObstacle = 10
    
    driving = True
    while driving:
        carDrive = 0
        carSteering = 0
        car.updateDistances()
        # no obstacle in front of car
        if car.distances[1] > 100:
            if car.distances[0] < sideObstacle:
                # turn the car towards the right
                carSteering = 1
                setDrive = 1
            elif car.distances[2] < sideObstacle:
                # turn the car towards the left
                carSteering = -1
                setDrive = 1
        # approaching an obstacle
        elif car.distances[1] > 30:
            # obstacles are closer on the right
            if car.distances[0] > car.distances[2] and car.distances[1] > sideObstacle:
                setSteering = -1
                setDrive = 1
            # obstacles are closer on the left
            elif car.distances[2] > sideObstacle:
                setSteering = 1
                setDrive = 1
            # can't reliably turn
            else:
                setSteering = 0
                setDrive = -1
        else:
            driving = False
        car.setSteering(carSteering, 80)
        car.setDrive(carDrive)

except KeyboardInterrupt:
    pass

car.stop()