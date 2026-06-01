# Fingertip Gesture Control of Robotic Arm

## 1. Content Description

This lesson captures color images, detects fingertips with MediaPipe, records a fingertip trajectory, recognizes the drawn shape, and then controls the robotic arm according to that shape.

This lesson requires terminal commands. Use the terminal that matches your mainboard. Raspberry Pi 5 and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker entry steps, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin users can open a terminal directly on the robot and run the commands there.

## 2. Program Startup

Start the camera:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, open another terminal and start the fingertip-trajectory arm-control program:

```bash
ros2 run yahboomcar_mediapipe 14_FingerAction
```

After the program starts, hold an open palm toward the camera, similar to the number `5`. The program draws landmarks for the whole hand. Adjust your hand so it stays near the upper middle of the image.

![Picture: page 1: picture 0](_page_1_Picture_0.jpeg)

To start drawing, keep only the index finger extended, similar to the number `1`.

![Picture: page 1: picture 2](_page_1_Picture_2.jpeg)

While holding the `1` gesture, move your finger. A red line appears on the screen and follows the index fingertip.

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

After drawing the shape, open all fingers again to make the `5` gesture. The program generates the trajectory image and recognizes the drawn shape.

![Picture: page 2: picture 2](_page_2_Picture_2.jpeg)

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

Note: Draw closed shapes. If the trajectory is not closed, parts of the recognized shape may be missing.

There are currently four trajectory shapes that can be recognized: triangle, rectangle, circle, and five-pointed star.

When the camera recognizes a supported trajectory shape, the robotic arm performs the corresponding action.

## 3. Core Code Analysis

Program code path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/14_FingerAction.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/14_FingerAction.py
```

Import the required libraries:

```python
import math
import time
import cv2 as cv
import numpy as np
import mediapipe as mp
import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from arm_msgs.msg import ArmJoints,ArmJoint
import cv2
import gc
import threading
import enum
```

Initialize the trajectory-recognition state, arm publishers, and image subscriber:

```python
def __init__(self,name):
    super().__init__(name)
    self.drawing = mp.solutions.drawing_utils
    self.timer = time.time()
    self.move_state = False
    self.state = State.NULL
    self.points = []
    self.start_count = 0
    self.no_finger_timestamp = time.time()
    self.gc_stamp = time.time()
    self.hand_detector = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_tracking_confidence=0.05,
        min_detection_confidence=0.6
    )
    self.rgb_bridge = CvBridge()
    #Define the topic for controlling 6 servos and publish the detected posture
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    #Define a topic for controlling a single servo and publish data on a single
servo control topic
    self.pub_SingleTargetAngle = self.create_publisher(ArmJoint, "arm_joint",
10)
    self.init_joints = [90, 164, 18, 0, 90, 30]
    self.pubSix_Arm(self.init_joints)
    #Define subscribers for the color image topic
    self.sub_rgb =
self.create_subscription(Image,"/camera/color/image_raw",self.get_RGBImageCallBa
ck,100)
```

The color image callback follows the trajectory-recognition flow from the previous lesson, then starts an additional thread to control the robotic arm:

```
if not self.move_state:
   self.move_state = True
   # Pass in a parameter graph_name, which is the name of the trajectory
   task = threading.Thread(target=self.arm_move_action, name="arm_move_action",
args= (graph_name, ))
   task.setDaemon(True)
   task.start()
```

The `arm_move_action` thread selects the corresponding arm action from the recognized trajectory name:

```python
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

For example, `self.arm_move_square()` runs the square action:

```python
def arm_move_square(self):
    move_joints = [90, 0, 180, 20, 90, 30]
    #Publish a topic message to control 6 servos and change the posture of the
robotic arm
    self.pubSix_Arm(move_joints)
    time.sleep(1.4)
    for i in range(3):
        #Control servo No. 4 to -15 degrees
        self.pubSingleArm(4,-15)
        time.sleep(0.4)
        #Control servo No. 4 to turn to 20 degrees
        self.pubSingleArm(4,20)
        time.sleep(0.4)
```
