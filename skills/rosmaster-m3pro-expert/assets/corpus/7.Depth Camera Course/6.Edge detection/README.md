# Depth-Based Edge Detection

## 1. Content Description

This lesson explains how to use depth imaging for edge detection. Combined with chassis control, the robot can stop at an edge to reduce the risk of falling. The same idea can be extended to depth-based obstacle avoidance.

This lesson requires terminal commands. Use the terminal that matches your mainboard. This lesson uses Raspberry Pi 5 as the example. Raspberry Pi and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker instructions, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

## 2. Program Startup

Start the camera:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, open another terminal and start the edge detection program:

```bash
ros2 run yahboom_M3Pro_DepthCam edge_detection
```

![Figure: page 0: figure 8](_page_0_Figure_8.jpeg)

After startup, the program prints and displays that the current state is stopped. Press the spacebar to change the state. If the robot does not detect an edge after the spacebar is pressed, it moves forward and prints `Moving...`. If it detects an edge, it stops and prints `Stop!!!`.

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

## 3. Core Code Analysis

Program code path for Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/yahboom_M3Pro_DepthCam/yahboom_M3Pro_DepthCam/Edge_ Detection.py
```

Program code path for Orin boards:

```text
/home/jetson/yahboomcar_ws/yahboom_M3Pro_DepthCam/yahboom_M3Pro_DepthCam/Ed ge_Detection.py
```

Import the required libraries:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from arm_msgs.msg import ArmJoints
from cv_bridge import CvBridge
import cv2
import numpy as np
import threading
```

Depth image decoding formats:

```python
encoding = ['16UC1', '32FC1']
```

Initialize variables and define publishers and subscribers:

```python
def __init__(self, name):
    super().__init__(name)
    #Define the posture of the robotic arm to identify the edge downwards
    self.init_joints = [90, 120, 0, 0, 90, 90]
    self.pub_vel = self.create_publisher(Twist,'/cmd_vel',1)
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    self.sub_depth =
self.create_subscription(Image,"/camera/depth/image_raw",self.get_DepthImageCall
Back,100)
    self.pubSix_Arm(self.init_joints)
    #The car's forward speed
    self.lin_x = 0.1
    self.depth_bridge = CvBridge()
    #Parking/Moving signs
    self.move_flag = False
```

The depth image topic callback calculates depth information at the center point:

```python
def get_DepthImageCallBack(self,msg):
    depth_image = self.depth_bridge.imgmsg_to_cv2(msg, encoding[1])
    #Call the thread to pass in the acquired depth image and calculate the depth
information
    compute_ = threading.Thread(target=self.compute_dist, args=(depth_image,))
    compute_.start()
    compute_.join()
    key = cv2.waitKey(10)
    if key == 32:
        self.move_flag = True
    cv2.imshow("frame", depth_image)
def compute_dist(self,result_frame):
    frame = cv2.resize(result_frame, (640, 480))
    depth_image_info = frame.astype(np.float32)
    #Judge whether the current state is moving. If so, judge the distance to the
center point. If not, call the function, issue a parking instruction, and print
the information.
    if self.move_flag == True:
```

```python
#Judge whether the depth information of the center point, that is, the
point x=320, y=240, is greater than 0.5m. If so, call the function to issue a
stop command. If not, call the function to issue a forward command.
        if depth_image_info[240, 320]/1000>0.5:
            self.pubVel(0,0,0)
            self.move_flag = False
            print("Stop!!!")
        else:
            self.pubVel(self.lin_x,0,0)
            print("Moving....")
    else:
        self.pubVel(0,0,0)
        print("Stop status now!Press the SPACEBAR to change the state.")
```

Publish the velocity command:

```python
def pubVel(self,vx,vy,vz):
    vel = Twist()
    vel.linear.x = float(vx)
    vel.linear.y = float(vy)
    vel.angular.z = float(vz)
    self.pub_vel.publish(vel)
```

The three inputs are x-axis speed, y-axis speed, and angular velocity. After assigning these values, the program calls `self.pub_vel.publish(vel)` to publish the velocity topic.
