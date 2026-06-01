# Gesture Grabbing and Releasing Objects

## 1. Content Description

This lesson captures color images, uses MediaPipe to recognize hand gestures, and controls the robotic arm to grasp or release objects based on the recognized gesture.

This lesson requires terminal commands. Use the terminal that matches your mainboard. Raspberry Pi 5 and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker entry steps, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin users can open a terminal directly on the robot and run the commands there.

## 2. Program Startup

Start the camera:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, open another terminal and start the gesture-based grasp/release program:

```bash
ros2 run yahboomcar_mediapipe 16_GestureGrasp
```

After the program starts, a `Yes` gesture commands the robotic arm to move to a preset position and grasp an object. An `OK` gesture commands the arm to place the object at a preset position. This example recognizes two gestures: `Yes` and `OK`.

Place your hand in the camera image and make the `Yes` gesture. The robotic arm moves forward to grasp the object.

![Picture: page 1: picture 0](_page_1_Picture_0.jpeg)

After the object is grasped, make the `OK` gesture to place it at the upper-left position.

![Picture: page 1: picture 2](_page_1_Picture_2.jpeg)

Press Ctrl+C in the terminal to exit the program.

## 3. Core Code Analysis

Program code path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/16_GestureGrasp.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/16_GestureGrasp.py
```

Import the required libraries:

```python
import math
import time
import cv2 as cv
import numpy as np
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from arm_msgs.msg import ArmJoints,ArmJoint
import cv2
from M3Pro_demo.media_library import *
import threading
```

Initialize the gesture detector, arm state, publishers, and subscriber:

```python
def __init__(self,name):
    super().__init__(name)
    self.drawing = mp.solutions.drawing_utils
    self.timer = time.time()
    self.move_state = False
    self.points = []
    self.start_count = 0
    self.no_finger_timestamp = time.time()
    self.gc_stamp = time.time()
    #Call the media_library library to create an object of the HandDetector
class
    self.hand_detector = HandDetector()
    self.pTime = 0
    # Define the state of grabbing blocks
    self.one_grabbed = 0
    self.two_grabbed = 0
    self.three_grabbed = 0
    self.four_grabbed = 0
    self.block_num = 0
    # Define the state of grabbing blocks
    self.Count_One = 0
    self.Count_Two = 0
    self.Count_Three = 0
    self.Count_Four = 0
    self.Count_Five = 0
    self.rgb_bridge = CvBridge()
    #Define the topic for controlling 6 servos and publish the detected posture
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    #Define a topic for controlling a single servo and publish data on a single
servo control topic
```

```
self.pub_SingleTargetAngle = self.create_publisher(ArmJoint, "arm_joint",
10)
    self.init_joints = [90, 164, 18, 0, 90, 30]
    self.pubSix_Arm(self.init_joints)
    #Define subscribers for the color image topic
    self.sub_rgb =
self.create_subscription(Image,"/camera/color/image_raw",self.get_RGBImageCallBa
ck,100)
```

```python
def get_RGBImageCallBack(self,msg):
    #Use CvBridge to convert color image message data into image data
    rgb_image = self.rgb_bridge.imgmsg_to_cv2(msg, "bgr8")
    #Call the findHands method of the class to detect the palm and return the
joint list
    frame, lmList,_ = self.hand_detector.findHands(rgb_image)
    #print("lmList: ",lmList)
    #Judge whether the joint list is 0, that is, whether the palm is detected
    if len(lmList) != 0:
        #Call the get_gesture method of the class, which returns the recognized
gesture based on the list of joint points
        gesture = self.hand_detector.get_gesture(lmList)
        #print("gesture = {}".format(gesture))
        #Based on the returned gesture, determine whether it is Yes or OK
        if gesture == 'Yes':
            cv.putText(frame, gesture, (250, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9,
(0, 255, 0), 1)
            self.Count_One = self.Count_One + 1
            self.Count_Two = 0
            self.Count_Three = 0
            self.Count_Four = 0
            self.Count_Five = 0
            #Count the value of self.Count_One. If it is greater than 5 and
self.move_state is False, the thread function of the robot arm gripping will be
executed.
            if self.Count_One >= 5 and self.move_state == False:
                self.move_state = True
                self.Count_One = 0
                print("start arm_ctrl_threading = {}".format(gesture))
                task = threading.Thread(target=self.arm_ctrl_threading,
name="arm_ctrl_threading", args=(gesture, ))
                task.setDaemon(True)
                task.start()
        elif gesture == 'OK':
            cv.putText(frame, gesture, (250, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9,
(0, 255, 0), 1)
            self.Count_Five = self.Count_Five + 1
            self.Count_One = 0
            self.Count_Two = 0
            self.Count_Three = 0
            self.Count_Four = 0
            if self.Count_Five >= 5 and self.move_state == False:
                self.move_state = True
                self.Count_Five = 0
```

```
print("start arm_ctrl_threading = {}".format(gesture))
                task = threading.Thread(target=self.arm_ctrl_threading,
name="arm_ctrl_threading", args=(gesture, ))
                task.setDaemon(True)
                task.start()
    key = cv2.waitKey(1)
    cv.imshow('frame', frame)
```

The `arm_ctrl_threading` thread executes the arm action associated with the recognized gesture:

```python
def arm_ctrl_threading(self, gesture):
    if gesture == 'OK':
        #The placement position can be modified according to actual needs
        move_joints = [163, 111, 0, 53, 90, 135]
        self.pubSix_Arm(move_joints)
        time.sleep(2.0)
        #Control servo No. 6 and release the gripper
        self.pubSingleArm(6,30)
        time.sleep(2.0)
        # Return to the initial posture
        move_joints = [90, 164, 18, 0, 90, 135]
        self.pubSix_Arm(move_joints)
        time.sleep(2.0)
    elif gesture == 'Yes':
        #The position of the lower claw can be modified according to actual
needs
        move_joints = [90, 15, 65, 20, 90, 30]
        # #Control servo No. 6 and release the gripper
        self.pubSingleArm(6,30)
        time.sleep(2.0)
        # Move to object position
        self.pubSix_Arm(move_joints)
        time.sleep(2.0)
        #Control servo No. 6 and clamp the claws
        self.pubSingleArm(6,135)
        time.sleep(2.0)
        move_joints = [90, 164, 18, 0, 90, 135]
        self.pubSix_Arm(move_joints)
        time.sleep(2.0)
    self.move_state = False
```
