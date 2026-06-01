# Tracking and Gripping AprilTag Blocks

## 1. Content Description

This lesson captures camera images and recognizes a handheld AprilTag machine-code block. As the block moves, the robotic arm follows it and keeps the tag center near the center of the image. When tracking stops, the program calculates the distance between the tag and `base_link`. If the distance is greater than 24 cm, the chassis moves forward until the target is within range. Once the target is close enough, the arm grasps the machine-code block and places it at the configured position.

This lesson requires terminal commands. Use the terminal that matches your mainboard. Raspberry Pi 5 and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker entry steps, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin users can open a terminal directly on the robot and run the commands there.

Wooden blocks used in this lesson: **40x40x40mm machine-code blocks**.

## 2. Program Startup

Start the robotic-arm solver and camera driver:

```bash
ros2 launch M3Pro_demo camera_arm_kin.launch.py
```

Open another terminal and start the robotic-arm grasping program:

```bash
ros2 run M3Pro_demo grasp
```

After it starts, the display appears as shown below.

Open a third terminal and start the AprilTag tracking and grasping program:

```bash
ros2 run M3Pro_demo apriltag_follow_2D
```

After the program starts, hold the included 4 cm machine-code block in the camera view. It appears as shown below.

![Picture: page 1: picture 3](_page_1_Picture_3.jpeg)

Slowly move the machine-code block. The robotic arm tracks it and keeps the tag center in the middle of the image. When tracking stops, the program checks whether the distance between `base_link` and the tag is less than 24 cm. If it is, the buzzer sounds and the arm grasps the block, places it at the configured position, and returns to the initial pose. If the distance is greater than 24 cm, the chassis moves forward until the target is within range, then the arm grasps, places, and returns.

## 3. Core Code Analysis

Program code path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/apriltag_follow_2D.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/apriltag_follow_2D.py
```

Import the required libraries:

```python
import cv2
import os
import numpy as np
from sensor_msgs.msg import Image
#Import the function of drawing machine code information
from M3Pro_demo.vutils import draw_tags
#Import the library for detecting machine code
from dt_apriltags import Detector
from cv_bridge import CvBridge
import cv2 as cv
from M3Pro_demo.Robot_Move import *
from arm_interface.srv import ArmKinemarics
from arm_interface.msg import AprilTagInfo,CurJoints
from arm_msgs.msg import ArmJoints
from std_msgs.msg import Bool,Int16,UInt16
import time
import transforms3d.euler as t3d_euler
import math
from rclpy.node import Node
import rclpy
from message_filters import Subscriber,
TimeSynchronizer,ApproximateTimeSynchronizer
from geometry_msgs.msg import Twist
import threading
#Import the library for servo PID adjustment
from M3Pro_demo.PID import *
from M3Pro_demo.compute_joint5 import *
```

Import the robotic-arm offset parameter file to compensate for servo virtual-position deviation:

```
offset_file = "/root/yahboomcar_ws/src/arm_kin/param/offset_value.yaml"
with open(offset_file, 'r') as file:
    offset_config = yaml.safe_load(file)
```

Initialize the node and create the publishers and subscribers:

```python
def __init__(self, name):
    super().__init__(name)
    self.init_joints = [90, 150, 12, 20, 90, 0]
    self.rgb_bridge = CvBridge()
    self.depth_bridge = CvBridge()
    self.cur_distance = 0.0
    self.grasp_Dist = 240
    # Initialize chassis PID adjustment parameters
    self.linearx_PID = (0.5, 0.0, 0.2)
    self.camera_info_K = [477.57421875, 0.0, 319.3820495605469, 0.0,
477.55718994140625, 238.64108276367188, 0.0, 0.0, 1.0]
    self.EndToCamMat = np.array([[ 0 ,0 ,1 ,-1.00e-01],
                                 [-1 ,0 ,0 ,0],
                                 [0 ,-1 ,0 ,4.82000000e-02],
                                 [ 0.00000000e+00 , 0.00000000e+00 ,
0.00000000e+00 , 1.00000000e+00]])
    self.CurEndPos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self.x_offset = offset_config.get('x_offset')
    self.y_offset = offset_config.get('y_offset')
```

```
self.z_offset = offset_config.get('z_offset')
    self.at_detector = Detector(searchpath=['apriltags'],
                                families='tag36h11',
                                nthreads=8,
                                quad_decimate=2.0,
                                quad_sigma=0.0,
                                refine_edges=1,
                                decode_sharpening=0.25,
                                debug=0)
    self.rgb_image_sub = Subscriber(self, Image, '/camera/color/image_raw')
    self.sub_grasp_status =
self.create_subscription(Bool,"grasp_done",self.get_graspStatusCallBack,100)
    self.depth_image_sub = Subscriber(self, Image, '/camera/depth/image_raw')
    self.CmdVel_pub = self.create_publisher(Twist,"cmd_vel",1)
    self.pos_info_pub = self.create_publisher(AprilTagInfo,"PosInfo",1)
    self.pub_SixTargetAngle = self.create_publisher(ArmJoints, "arm6_joints",
10)
    self.TargetJoint5_pub = self.create_publisher(Int16, "set_joint5", 10)
    self.pub_beep = self.create_publisher(UInt16, "beep", 10)
    self.pub_cur_joints = self.create_publisher(CurJoints,"Curjoints",1)
    self.client = self.create_client(ArmKinemarics, 'get_kinemarics')
    self.pubSixArm(self.init_joints)
    self.cur_joints = self.init_joints
    self.get_current_end_pos()
    self.ts = ApproximateTimeSynchronizer([self.rgb_image_sub,
self.depth_image_sub], 1, 0.5)
    self.ts.registerCallback(self.callback)
    #Define the flag to start the clamping program. When the value is True, the
machine code location information is calculated and the machine code location
information topic is published.
    self.start_grasp = False
    #Define the flag for adjusting the distance. When the value is True, the
chassis moves to adjust the distance.
    self.adjust_dist = False
    #The initial value of the robot arm tracking x direction (left and right)
    self.target_servox=90
    #The initial value of the robot arm tracking the y direction (left and
right)
    self.target_servoy=180
    # Initialize the robot arm PID adjustment parameters in the x direction
    self.xservo_pid = PositionalPID(0.25, 0.1, 0.05)
    # Initialize the robot arm PID adjustment parameters in the y direction
    self.yservo_pid = PositionalPID(0.25, 0.1, 0.05)
    #Define whether the y value threshold is exceeded. When the value is True, it
means that the y value threshold is exceeded.
    self.y_out_range = False
    #Define whether the x-value threshold is exceeded. When the value is True, it
means that the y-value threshold is exceeded.
    self.x_out_range = False
    self.a = 0
    self.b = 0
    #Define the flag for publishing machine code information. When the value is
True, it means publishing, and when it is False, it means not publishing
    self.pubPos_flag = False
    #Define the flag bit for the robot to track the machine code. When the value
is True, the robot will track the machine code.
    self.XY_Track_flag = True
```

```
self.joint5 = Int16()
    #Define the end flag of the tracking and clamping program. When the value is
True, it means that the next tracking and clamping can be performed.
    self.Done_flag = True
    # Chassis PID initialization program
    self.PID_init()
```

The image-topic callback processes camera frames:

```python
def callback(self,color_frame,depth_frame):
    #Get color image topic data and use CvBridge to convert message data into
image data
    rgb_image = self.rgb_bridge.imgmsg_to_cv2(color_frame,'rgb8')
    result_image = np.copy(rgb_image)
    #Get the deep image topic data and use CvBridge to convert the message data
into image data
    depth_image = self.depth_bridge.imgmsg_to_cv2(depth_frame, encoding[1])
    frame = cv2.resize(depth_image, (640, 480))
    depth_image_info = frame.astype(np.float32)
    #Call the machine code detection program, pass in the color image for
detection, and return a tags list containing information about all the detected
machine codes
    tags = self.at_detector.detect(cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY),
False, None, 0.025)
    #Sort the test results according to the machine code id
    tags = sorted(tags, key=lambda tag: tag.tag_id)
    #Draw the center and corner points of the machine code on the color image
    draw_tags(result_image, tags, corners_color=(0, 0, 255), center_color=(0,
255, 0))
    #Start the thread and execute the function to display the image
    show_frame = threading.Thread(target=self.img_out, args=(result_image,))
    show_frame.start()
    show_frame.join()
    #If the length of the test result is not 0, it means that the machine code
has been detected
    if len(tags) > 0 :
        #print("tag: ",tags)
        #Get the center point coordinates and corner point coordinates of the
machine code
        center_x, center_y = tags[0].center
        corners = tags[0].corners
        #print("corners: ",corners)
        #Calculate the depth information of the center point
        cur_depth = depth_image_info[int(center_y),int(center_x)]
        #Calculate the pose of the machine code in the world coordinate system
        get_dist = self.compute_heigh(center_x,center_y,cur_depth/1000.0)
        #Calculate the distance between the center of the machine code and the
base coordinate base_link
        self.cur_distance = math.sqrt(get_dist[1] ** 2 + get_dist[0]** 2)*1000
        #If the difference between the center coordinates of the machine code
and the center point (320,240) in the image is greater than 10 pixels and the
robot tracking machine code flag is True, then execute the XY_Track function
        if (abs(center_x-320) >10 or abs(center_y-240)>10) and
self.XY_Track_flag==True:
            self.XY_track(center_x,center_y)
            print("Tracking")
            print("-------------------------------------")
```

```
#If the difference between the center coordinates of the machine code
and the center point (320,240) in the figure is less than 10 pixels and the
tracking and gripping program end flag is ended, then change the
self.XY_Track_flag flag to False, indicating that the robot arm tracking is
complete.
        if abs(center_x-320) <10 and abs(center_y-240)<10 and
self.Done_flag==True:
            self.adjust_dist = True
            #self.pubCurrentJoints()
            self.XY_Track_flag = False
            print("self.cur_distance: ",self.cur_distance)
            print("Adjust it.")
            print("-------------------------------------")
        #If the chassis adjustment flag is True, it means that the chassis can
be moved to adjust the distance
        if self.adjust_dist== True:
            #If the current distance is greater than 24 cm, then execute the
move_dist function to control the movement of the chassis
            if self.cur_distance>240:
                dist_adjust = self.cur_distance
                self.move_dist(dist_adjust)
            #If the current distance is less than 24 cm, it means it is within
the gripping range. Control the chassis to adjust the distance, change the value
of self.adjust_dist to False and the value of self.start_grasp to True,
indicating that you can start calculating the position information of the machine
code and publish the position information topic of the machine code
            else:
                self.adjust_dist = False
                self.start_grasp = True
                #self.pubVel(0,0,0)
        if self.start_grasp == True:
            #Get the center point coordinates of the current machine code and
calculate the depth information of the center point coordinates
            c_x, c_y = tags[0].center
            depth_dist = depth_image_info[int(c_y),int(c_x)]/1000
            #If the depth value is not 0, it means it is valid, then the
location message topic of the machine code is assigned and published.
            if depth_dist!=0:
                print("depth_dist: ",depth_dist)
                tag = AprilTagInfo()
                tag.id = tags[0].tag_id
                cur_x, cur_y = tags[0].center
                tag.x = cur_x
                tag.y = cur_y
                tag.z = depth_image_info[int(tag.y),int(tag.x)]/1000
                #Publish the topic of the current posture of the robotic arm
                self.pubCurrentJoints()
                self.Done_flag = False
                self.start_grasp = False
                #Execute the Beep_Loop function to let the buzzer publish the
topic
                self.Beep_Loop()
                self.pubVel(0,0,0)
                #Get the corner coordinates to calculate the rotation angle of
the machine code at this time
                vx = int(tags[0].corners[0][0]) - int(tags[0].corners[1][0])
                vy = int(tags[0].corners[0][1]) - int(tags[0].corners[1][1])
```

```
target_joint5 = compute_joint5(vx,vy)
            print("target_joint5: ",target_joint5)
            self.joint5.data = int(target_joint5)
            #Publish a topic message about controlling Servo No. 5
            self.TargetJoint5_pub.publish(self.joint5)
            #Publish the machine code location topic message
            self.pos_info_pub.publish(tag)
            print("Publish tag info.")
        else:
            print("Invalid distance.")
else:
    self.pubVel(0,0,0)
```
