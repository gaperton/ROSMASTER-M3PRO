# Fingertip gesture control robotic arm
## 1. Content Description
This function captures color images and uses the MediaPipe framework to detect fingertips.

Gestures are used to start and stop recording the fingertip's trajectory within the image. After

recording is complete, a fingertip trajectory map is generated and the trajectory is recognized.

Finally, the robot arm is controlled based on the trajectory.


This section requires entering commands in the terminal. The terminal you open depends on

your motherboard type. This lesson uses the Raspberry Pi 5 as an example. For Raspberry Pi and

Jetson-Nano boards, you need to open a terminal on the host computer and enter the command

to enter the Docker container. Once inside the Docker container, enter the commands mentioned

in this section in the terminal. For instructions on entering the Docker container from the host

computer, refer to this product tutorial **[Configuration and Operation Guide]--[Enter the**

**Docker (Jetson Nano and Raspberry Pi 5 users, see here)]** .


Simply open the terminal on the Orin motherboard and enter the commands mentioned in this

section.

## 2. Program startup
First, in the terminal, enter the following command to start the camera,


After successfully starting the camera, open another terminal and enter the following command

in the terminal to start the program for controlling the robotic arm with fingertip trajectory

gestures:


After the program is run, as shown in the figure below, place your palm flat on the camera screen,

open your fingers, and face the camera with your palm, similar to the number 5 gesture. The

image will draw the joints on the entire palm. Adjust the position of your palm and try to keep it in

the upper middle part of the screen.


![](12.Fingertip-gesture-control-robotic-arm.pdf-1-0.jpeg)

At this time, the index finger remains unchanged and the other fingers are retracted, similar to

the gesture of the number 1.


While holding gesture 1, move the position of your finger and a red line will appear on the screen,

drawing the path of your index finger.


![](12.Fingertip-gesture-control-robotic-arm.pdf-1-1.jpeg)
![](12.Fingertip-gesture-control-robotic-arm.pdf-2-0.jpeg)

After the graphic is drawn, open all your fingers and make a gesture similar to the number 5, and

the drawn graphic will be generated below.


![](12.Fingertip-gesture-control-robotic-arm.pdf-2-1.jpeg)
![](12.Fingertip-gesture-control-robotic-arm.pdf-3-0.jpeg)

Note: The drawn graphics need to be closed, otherwise some content may be missing.


There are currently four trajectory shapes that can be recognized: triangle, rectangle, circle, and

five-pointed star.


When the camera recognizes different trajectory shapes, it will control the robotic arm to perform

corresponding actions.

## 3. Core code analysis
Program code path:


Raspberry Pi 5 and Jetson-Nano board

The program code is in the running docker. The path in docker

is `/root/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/14_FingerAct`

```
   ion.py

```

Orin Motherboard

The program code path

is `/home/jetson/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/14_Fi`

```
   ngerAction.py

```

Import the library files used,


![](12.Fingertip-gesture-control-robotic-arm.pdf-3-1.jpeg)


Initialize data and define publishers and subscribers,


![](12.Fingertip-gesture-control-robotic-arm.pdf-4-0.jpeg)


The color image callback function can refer to the content of the previous section. Here, there is

an additional thread to control the robotic arm.


![](12.Fingertip-gesture-control-robotic-arm.pdf-4-1.jpeg)


The arm_move_action thread executes the function and executes the corresponding function

according to the passed name.

```
 def arm_move_action(self, name):

    time.sleep(1)

    print("-----------------")

    if name == 'Triangle':

      self.arm_move_triangle()

    elif name == 'Square':

      self.arm_move_square()

    elif name == 'Circle':

      self.arm_move_circle()

    elif name == 'Star':

      self.arm_move_star()

    self.pubSix_Arm(self.init_joints)

```

```
      time.sleep(1.5)

    self.move_state = False

```

Take self.arm_move_square() as an example,


![](12.Fingertip-gesture-control-robotic-arm.pdf-5-0.jpeg)
