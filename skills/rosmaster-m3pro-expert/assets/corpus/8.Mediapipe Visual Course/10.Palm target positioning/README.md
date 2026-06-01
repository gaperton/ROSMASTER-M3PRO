# Palm Target Positioning

## 1. Content Description

This lesson captures color images, uses MediaPipe to detect a hand, and outputs the palm center coordinates. These coordinates can be used later for chassis tracking or robotic-arm target tracking.

This lesson requires terminal commands. Use the terminal that matches your mainboard. Raspberry Pi 5 and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker entry steps, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin users can open a terminal directly on the robot and run the commands there.

## 2. Program Startup

Start the camera:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, open another terminal and start the palm-positioning program:

```bash
ros2 run yahboomcar_mediapipe 12_FindHand
```

After the program starts, detected palms are outlined in green, and the palm center coordinates are printed in the terminal.

![Figure: page 0: figure 11](_page_0_Figure_11.jpeg)

## 3. Core Code Analysis

Program code path:

Raspberry Pi 5 and Jetson Nano:

```
/root/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/12_FindHand.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/yahboomcar_mediapipe/yahboomcar_mediapipe/12_FindHand.py
```

Import the required libraries:

```python
import rclpy
from rclpy.node import Node
from M3Pro_demo.media_library import *
import cv2 as cv
import numpy as np
import time
import os
import threading
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from arm_msgs.msg import ArmJoints
import cv2
```

Initialize the reusable `HandDetector`, publishers, and subscribers:

```python
def __init__(self,name, mode=False, maxHands=2, detectorCon=0.5, trackCon=0.5):
    super().__init__(name)
    #Call the media_library library to create an object of the HandDetector
class
    self.hand_detector = HandDetector()
    #create a publisher
    self.rgb_bridge = CvBridge()
    #Define the topic for controlling 6 servos and publish the detected posture
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    self.init_joints = [90, 150, 10, 20, 90, 90]
    self.pubSix_Arm(self.init_joints)
    #Define subscribers for the color image topic
    self.sub_rgb =
self.create_subscription(Image,"/camera/color/image_raw",self.get_RGBImageCallBa
ck,100)
```

Color image callback:

```python
def get_RGBImageCallBack(self,msg):
    #Use CvBridge to convert color image message data into image data
    rgb_image = self.rgb_bridge.imgmsg_to_cv2(msg, "bgr8")
    # Pass the obtained image into the process function for palm detection
    frame = self.process(rgb_image)
    key = cv2.waitKey(1)
    cv.imshow('dist', frame)
```

The `process` function detects the hand and prints the palm center:

```python
def process(self, frame):
    #Call the object method to perform palm detection and return the detected
image as well as the lmList list and bbox list
    frame, lmList, bbox = self.hand_detector.findHands(frame)
    self.hand_detector.draw = True
    #If the lmList list is not empty, it means that a palm has been detected
    if len(lmList) != 0:
        hand = self.hand_detector.fingersUp(lmList)
    #Get the xy coordinates of the palm, bbox stores the xy coordinates of the
upper left and lower right corners of the palm
    indexX = (bbox[0] + bbox[2]) / 2
    indexY = (bbox[1] + bbox[3]) / 2
    print("index X: %.1f, Y: %.1f" % (indexX, indexY))
    return frame
```

The MediaPipe recognition helper classes are defined in the `media_library.py` file in the `M3Pro_demo` package.

File path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/media_library.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/media_library.py
```

This helper library wraps native MediaPipe functionality into reusable classes. For example, the `HandDetector` class defines:

- `findHands`: Detect hands.
- `fingersUp`: Determine which fingers are extended.
- `ThumbTOforefinger`: Detect the angle between the thumb and index finger.
- `get_gesture`: Recognize gestures.
