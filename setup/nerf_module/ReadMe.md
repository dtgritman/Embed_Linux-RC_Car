## Required Software Setup
Required software setup for the nerf_module:

To prevent issues with the motors used in the cannon we have used the pigpio library and daemon.
The pigpio library can be installed using the command
```
~$ sudo apt-get install pigpio python-pigpio python3-pigpio
```

This library requires the pigpio daemon to be running, this can either be started every time using
```
~$ sudo pigpiod
```
or can be set to run on startup by using the command
```
~$ sudo systemctl enable pigpiod
```

## Assembly of Cannon
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
