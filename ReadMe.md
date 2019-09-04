# Humans vs Zombies

### Team
 * **Miguel**: Building a vehicle to hold the project components.
 * **Dustin**: Building a nerf cannon that will angle up/down and rotate side to side. 
 * **Faizan**: Creating the object detection mechanism to target objects.

### Goal
 We plan to create a vehicle which shoots nerf projectiles for the campus-wide game called ‘Humans vs. Zombie’. Our tank has two hardware modules, the tanks enclosure and the nerf cannon used to fire the nerf pelts. We hope to add object recognition to our project to make it autonomous We will not only be using the Pi’s onboard GPIO pins but use a server to stream any video information onto a web-server. The Pi will also log anyone it deems to be threatening for correction or algorithm calibration.

## Tutorial 
Each part has its respective tutorial due to the modulization of the project. Please follow each markdown file closely and 

### Part 1 (Car Setup)

All images will be in the `img/` folder, please use them as references.
[Car ReadMe Setup](https://github.com/MiguelAPerez/Humans-vs-Zombies/blob/master/setup/rc_car/)

### Part 2 (Nerf Module Setup)

Though this part can be completed without setting up the car we highly recommend finishing the car set-up for any changes you may need to make.
[Nerf Cannon](https://github.com/MiguelAPerez/Humans-vs-Zombies/tree/master/setup/nerf_module)

### Part 3 (Object Detection)

Our project uses OpenCV and python3 to detect human faces. We are using precompiled libraries. 
[Object Detection](https://github.com/MiguelAPerez/Humans-vs-Zombies/tree/master/setup/object_detection)

### Part 4 (Putting it all together)

You can find our master init file in the [code/](https://github.com/MiguelAPerez/Humans-vs-Zombies/tree/master/code) folder. To run the RC Car run the `web.py` file using python3 

```bash
 $ python3 web.py
```


#### Citation 
 Cascade Used: [Opencv git repo](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalcatface.xml)
