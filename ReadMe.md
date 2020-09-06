# Humans vs Zombies

### Team
 * **Miguel**: Building a vehicle to hold the project components.
 * **Dustin**: Building a nerf cannon that will angle up/down and rotate side to side. 
 * **Faizan**: Creating the object detection mechanism to target objects.

### Goal
 We plan to create a vehicle which shoots nerf projectiles for the campus-wide game called ‘Humans vs. Zombie’. Our tank has two hardware modules, the tanks enclosure and the nerf cannon used to fire the nerf pelts. We hope to add object recognition to our project to make it autonomous We will not only be using the Pi’s onboard GPIO pins but use a server to stream any video information onto a web-server. The Pi will also log anyone it deems to be threatening for correction or algorithm calibration.

# Tutorial 
Each part has its respective tutorial due to the modulization of the project. Please follow each markdown file closely and 

## Pi Setup

You can find a full tutorial in the [`setup/`](/setup/rasp_pi.md) folder

## Part 1 (Car Setup)

#### Modifications

1. Removing the top of the car 
2. Removing the cars microprocessor
3. Resoldering the on/off switch 

![](/img/rc_car_org_board.jpg)

![](/img/rc_car_battery_switch.jpg)

#### Wiring 


    STBY = GPIO #17     = Stand By

    Drive motor:
    PWMA = GPIO #3      = Speed
    AIN2 = GPIO #4
    AIN1 = GPIO #18

    Left-Right controller:
    BIN1 = GPIO #27
    BIN2 = GPIO #23    
    PWMB = GPIO #24    = Speed



## Part 2 (Nerf Module Setup)

Though this part can be completed without setting up the car we highly recommend finishing the car set-up for any changes you may need to make.

### Assembly of Cannon
#### Parts Needed
- Stepper Motor (NEMA 17)
- Standard 180 degree Servo Motor
- 1x Bearing (for the top stand center) with an inner diamter of 12mm, an outer diameter of 37mm, and a width of 12mm.
- 2x Bearings (for arm mounts) with an inner diameter of 7mm, outer diameter of 19mm, and a width of 6mm.
- 4x Transfer Ball bearings (for the legs of the top) with a bearing surface that has a diameter of 15mm and a mounting cylinder with a diameter of 25mm which has a flared top.

#### Stand Assembly
1. Sand the bearing mounting hole at the top of the arm until you can press in the bearing using a tool like a c-clamp (the bearing should not be able to be inserted by hand).
2. Once the bearing is mounted, insert the ArmAxle in to the bearing (some sanding may be required), this should be very difficult to insert and can be tapped in very lightly with a hammer.
3. With the ArmAxle mounted, you can place the ArmGear on the side with the stepper motor mount. This gear should be relatively difficult to push on the axle.
4. Place the stepper motor on the mount and screw it down but leave enough slack to slide the motor up and down.
5. Put the StepperGear on the motor and place it so the gears are in contact (leave a very small amount of space so the gears don't bind).
6. Push the LaserBracket on to the Axle (should be relatively snug).
7. Finally with the laser pointer mounted on the LaserRail, slide the rail in to the bracket (again this should be relatively snug).

#### Base Assembly
1. The base has raised wall which will be used to mount the ssd and raspberry pi, to do so we used velcro on the inner wall and ssd to mount it and on the outer wall we used neoprene closed cell foam to help hold the raspberry pi (and prevent damage to the pins) with rubber bands wrapped around.
2. With the bearing track sanded down, place the BaseGear on the center rod (should fit snuggly).

#### Top Assembly
1. First, press in the center bearing.
2. Attach the ServoGear to servo, we used hot glue on a servo horn (if using this method make sure its centered).
3. Mount the servo to the top using the ServoMounts (slowly screw the screws in, taking breaks frequently so you don't break screw).
4. Place the Transfer Ball Bearings in to the tops four arms (should fit snuggly).
5. Mount the stand(s) to the top using the ArmBrackets and ArmMounts (carefully screw in to the mounting holes).
6. Finally place the top on the base and press the top down so the base rod snuggly fits in the bearing and then place a screw through the TopBearingWasher and screw in to the rod to prevent the top from lifting off the base.


## Part 3 (Object Detection)

Our project uses OpenCV and python3 to detect human faces. We are using precompiled libraries. 
[Object Detection](/setup/object_detection.md)

## Part 4 (Putting it all together)

You can find our master init file in the [code/](https://github.com/MiguelAPerez/Humans-vs-Zombies/tree/master/code) folder. To run the RC Car run the `web.py` file using python3 

```bash
 $ python3 web.py
```


#### Citation 
 Cascade Used: [Opencv git repo](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalcatface.xml)
