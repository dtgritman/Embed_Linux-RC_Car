## This folder contains all the code related to the project

| File | Description |
|------|-------------|
| [Drone/Cannon.py](Drone/Cannon.py) | This file contains the TankCannon class and StepperMotor class which can be used to control the tanks cannon by turning it left, right, up, and down, and turning the cannon on and off. |
| [Drone/Car.py](Drone/Car.py) | This file contains the Car class which can be used to control the rc car drive and steering with speed control. |
| [web.py](web.py) | This program contains the webserver for the project which controls the tank. It uses Flask on port 8080. This also contains the detection code to run by itself. |
| [tankps4.py](tankps4.py) | This program can be used to control the tank with ps4 controller. (L2/R2 for drive, left joystick for steering, right joystick for cannon position, R1 for firing, and options to pause/resume) |
|[camera.py](camera.py)| Class for the video stream and object detection|