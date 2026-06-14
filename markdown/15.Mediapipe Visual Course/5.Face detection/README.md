# Face detection
## 1. Content Description
This course implements color image acquisition and face detection using the MediaPipe

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

in the terminal to start the face detection program.


After the program is run, as shown in the figure below, the detected face will be framed and the

detection score will be displayed. The higher the score, the more accurate the face recognition is.


![](5.Face-detection.pdf-1-0.jpeg)
## 3. Core code analysis
Program code path:


Raspberry Pi 5 and Jetson-Nano board


The program code is in the running docker. The path in docker is

/root/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/07_FaceDetectio

n.py

Orin Motherboard


The program code path is

/home/jetson/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/07_Face

Detection.py


Import the library files used,


![](5.Face-detection.pdf-1-1.jpeg)


Initialize data and define publishers and subscribers,

```
 def __init__(self, name):

```

![](5.Face-detection.pdf-2-0.jpeg)


Color image callback function,


![](5.Face-detection.pdf-2-1.jpeg)


findFaces function,


![](5.Face-detection.pdf-2-2.jpeg)


```
    return frame, bboxs

```

fancyDraw function draws the bounding box according to the value of the detection result bbox


![](5.Face-detection.pdf-3-0.jpeg)
