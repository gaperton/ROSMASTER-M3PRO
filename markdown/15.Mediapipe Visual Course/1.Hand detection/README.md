# Hand detection
## 1. Content Description
This course implements color image acquisition and hand joint detection using the MediaPipe

framework.


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

to start the hand detection program.


After the program is run, the following figure will be shown. The hand joint points detected will be

displayed on the right side of the image.


![](1.Hand-detection.pdf-0-2.jpeg)
## 3. Core code analysis
Program code path:


Raspberry Pi 5 and Jetson-Nano board


The program code is in the running docker. The path in docker

is `/root/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/01_HandDetec`

```
   tor.py

```

Orin Motherboard


The program code path

is `/home/jetson/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/01_Ha`

```
   ndDetector.py

```

Import the library files used,


![](1.Hand-detection.pdf-1-0.jpeg)


Initialize data and define publishers and subscribers,


![](1.Hand-detection.pdf-1-1.jpeg)


Color image callback function,


![](1.Hand-detection.pdf-2-0.jpeg)


pubHandsPoint function,


![](1.Hand-detection.pdf-2-1.jpeg)


frame_combine merge image function,


![](1.Hand-detection.pdf-2-2.jpeg)


```
  return dst

```
