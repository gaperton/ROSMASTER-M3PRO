# MediaPipe Gesture Recognition

## 1. Content Description

This lesson explains how to subscribe to an image topic, obtain camera images, and use MediaPipe for gesture recognition.

This lesson requires terminal commands. Use the terminal that matches your mainboard. This lesson uses Raspberry Pi 5 as the example. Raspberry Pi and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker instructions, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

### About MediaPipe

MediaPipe is a data-stream processing and machine-learning application framework developed and open-sourced by Google. It is a graph-based processing pipeline for applications that use video, audio, sensor data, and other time-series data. MediaPipe is cross-platform and can run on embedded platforms such as Raspberry Pi, mobile devices, workstations, and servers. It also supports mobile GPU acceleration. Key MediaPipe concepts include packets, streams, calculators, graphs, and subgraphs.

#### MediaPipe Hands

MediaPipe Hands is a high-fidelity hand and finger tracking solution. It uses machine learning to infer 21 hand landmarks.

After detecting the palm in the full image, the hand landmark model locates 21 3D hand joint coordinates in the detected hand region by direct coordinate prediction. The model learns a consistent hand pose representation and remains robust when hands are partially visible or occluded. The training data includes about 30,000 real-world images annotated with 21 3D coordinates, plus rendered synthetic hand models mapped to corresponding 3D coordinates.

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

After obtaining the coordinates of each joint, the program can recognize gestures through geometric calculation.

## 2. Program Startup

Start the camera:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, open another terminal and start the MediaPipe gesture recognition program:

```bash
ros2 run M3Pro_demo mediapipe_gesture
```

After startup, the program can recognize three gestures: `OK`, `Yes`, and `Thumb_down`.

![Figure: page 1: figure 8](_page_1_Figure_8.jpeg)

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

![Figure: page 2: figure 1](_page_2_Figure_1.jpeg)

## 3. Core Code Analysis

Program code path for Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/mediapipe_gesture.py
```

Program code path for Orin boards:

```text
/home/jetson/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/mediapipe_gesture.py
```

Import the required libraries:

```python
import cv2
import os
from sensor_msgs.msg import Image
import message_filters
from cv_bridge import CvBridge
import cv2 as cv
from arm_msgs.msg import ArmJoints
import time
from M3Pro_demo.media_library import *
```

```python
from rclpy.node import Node
import rclpy
from message_filters import Subscriber,
TimeSynchronizer,ApproximateTimeSynchronizer
from sensor_msgs.msg import Image
import threading
```

Initialize variables and create subscribers and publishers:

```python
def __init__(self, name):
    super().__init__(name)
    self.init_joints = [90, 150, 12, 20, 90, 0]
    self.rgb_bridge = CvBridge()
    #Create an object recognized by Medipipe
    self.hand_detector = HandDetector()
    self.pr_time = time.time()
    self.pTime = self.cTime = 0
    #Subscribe to the publisher, publish the initial position of the robotic arm,
and control the movement of the robotic arm to the posture of the recognized
gesture
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    #Create a color image topic subscriber
    self.rgb_image_sub = Subscriber(self, Image, '/camera/color/image_raw')
    #Publish initial recognition posture
    self.pubSix_Arm(self.init_joints)
    self.ts = ApproximateTimeSynchronizer([self.rgb_image_sub], 1, 0.5)
    self.ts.registerCallback(self.callback)
    time.sleep(2)
    self.start_time = 0.0
```

Color image callback function and image processing:

```python
def callback(self,color_msg):
    rgb_image = self.rgb_bridge.imgmsg_to_cv2(color_msg, "bgr8")
    self.process(rgb_image)
def process(self, frame):
     #Call the function to find the palm in the Medipipe recognition class
    frame, lmList, bbox = self.hand_detector.findHands(frame)
    #Judge the length of lmList. If it is greater than 0, it means the palm is
found.
    if len(lmList) != 0:
        # Enter the thread to process the gesture recognition function, the
parameter passed in is lmList
        gesture = threading.Thread(target=self.Gesture_Detect_threading, args=
(lmList,bbox))
        gesture.start()
        gesture.join()
        self.cTime = time.time()
        fps = 1 / (self.cTime - self.pTime)
        self.pTime = self.cTime
        text = "FPS : " + str(int(fps))
        cv.putText(frame, text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0,
255), 1)
        if cv.waitKey(1) & 0xFF == ord('q'):
            cv.destroyAllWindows()
```

```python
cv.imshow('frame', frame)
def Gesture_Detect_threading(self, lmList,bbox):
    #Call the function to get gesture in Medipipe recognition class
    gesture = self.hand_detector.get_gesture(lmList)
    print("gesture: ",gesture)
```

The MediaPipe recognition class is defined in the `media_library` library, which is located in the `M3Pro_demo` package.

Path for Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/media_library.py
```

Path for Orin boards:

```text
/home/jetson/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/media_library.py
```

This library extends the native MediaPipe library and defines multiple classes. Each class provides different functions that can be called with the required parameters. For example, the `HandDetector` class defines:

- findHands: Find hands
- fingersUp: Detect whether fingers are extended
- ThumbTOforefinger: Detect the angle between the thumb and index finger
- get_gesture: Detect gestures
