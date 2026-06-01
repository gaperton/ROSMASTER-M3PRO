# MediaPipe Gesture ID Sorting (AprilTag)

## 1. Content Description

This lesson captures camera images, recognizes MediaPipe finger-count gestures from 1 to 4, and uses the recognized gesture as the target AprilTag ID. After a gesture is recognized, the robotic arm moves to the sorting posture and searches the desktop for the matching machine-code block. If the matching block is found, the arm lowers the gripper and places the block at the configured location. If no matching block is found, the arm shakes its head and returns to the gesture-recognition posture.

This lesson requires terminal commands. Use the terminal that matches your mainboard. Raspberry Pi 5 and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker entry steps, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin users can open a terminal directly on the robot and run the commands there.

## 2. Program Startup

Start the robotic-arm solver and camera driver:

```bash
ros2 launch M3Pro_demo camera_arm_kin.launch.py
```

Open another terminal and start the robotic-arm grasping program:

```bash
ros2 run M3Pro_demo grasp_desktop
```

After it starts, the display appears as shown below.

Open a third terminal and start the MediaPipe gesture ID sorting program:

```bash
ros2 run M3Pro_demo apriltagID_gesture
```

After this command starts, the second terminal should receive one frame of current-angle topic information and calculate the current arm pose, as shown below.

If the current-angle information is not received and the current pose is not calculated, coordinate conversion will produce an inaccurate grasping pose. Press Ctrl+C to stop the MediaPipe gesture ID sorting program, then restart it until the grasping program receives the current-angle information and calculates the current end position.

Open a fourth terminal and start the MediaPipe gesture recognition program:

```bash
ros2 run M3Pro_demo mediapipe_detect
```

After startup, the robotic arm moves to the recognition posture and begins recognizing gestures from 1 to 4. Gesture 1 means one extended finger, gesture 2 means two extended fingers, gesture 3 means three extended fingers, and gesture 4 means four extended fingers. Hold the gesture until the buzzer sounds, which indicates recognition is complete. The arm then moves to the sorting posture. The example below uses gesture 2.

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

After entering the sorting posture, the program begins recognizing machine-code blocks on the desktop, as shown below.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

After waiting 8 seconds, if machine-code block No. 2 is found, the program checks whether the distance between block No. 2 and `base_link` is within `[210, 220]`. If it is, the lower gripper grasps block No. 2, places it at the configured position, and the arm returns to the sorting posture. If the block is outside `[210, 220]`, the chassis adjusts the distance until the block is within range, then the gripper grasps and places it.

If machine-code block No. 2 is not found, or no machine-code block is detected, the robot buzzer sounds, the robotic arm shakes its head, and the arm returns to the gesture-recognition posture.

## 3. Core Code Analysis

### 3.1. mediapipe_detect.py

Program code path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/mediapipe_detect.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/mediapipe_detect.py
```

Import the required libraries:

```python
import cv2
import os
import numpy as npX5Plus
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 as cv
from arm_msgs.msg import ArmJoints
from std_msgs.msg import Bool,Int16,UInt16
from geometry_msgs.msg import Twist
import time
from M3Pro_demo.media_library import *
from rclpy.node import Node
import rclpy
from message_filters import Subscriber,
TimeSynchronizer,ApproximateTimeSynchronizer
import threading
```

Initialize the node and create the publishers and subscribers:

```python
def __init__(self, name):
    super().__init__(name)
    #Robotic arm gesture recognition
    self.init_joints = [90, 150, 12, 20, 90, 0]
    self.rgb_bridge = CvBridge()
    self.depth_bridge = CvBridge()
    #Create a gesture recognition object
    self.hand_detector = HandDetector()
     #Define the flag for publishing gestures. When the value is True, it means
that the topic of gesture recognition results can be published.
    self.pub_gesture = True
    #Record the number of times the gesture recognition has the same result. If
the number reaches 30, the gesture recognition is completed.
```

```
self.cnt = 0
    #Record the last gesture recognition result
    self.last_sum = 0
    self.pTime = self.cTime = 0
    #Create a topic for publishers to publish gesture recognition results
    self.pub_GesturetId = self.create_publisher(Int16,"GesturetId",1)
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    self.rgb_image_sub = Subscriber(self, Image, '/camera/color/image_raw')
    #Create a subscriber to subscribe to the reset gesture recognition result
topic
    self.sub_reset_gesture =
self.create_subscription(Bool,"reset_gesture",self.get_resetCallBack,100)
    self.pub_beep = self.create_publisher(UInt16, "beep", 10)
    #Control the robot arm to move to the recognized gesture posture
    self.pubSix_Arm(self.init_joints)
    self.ts = ApproximateTimeSynchronizer([self.rgb_image_sub], 1, 0.5)
    self.ts.registerCallback(self.callback)
    time.sleep(2)
```

The image-topic callback processes camera frames:

```python
def callback(self,color_msg):
    #Get color image topic data and use CvBridge to convert message data into
image data
    rgb_image = self.rgb_bridge.imgmsg_to_cv2(color_msg, "bgr8")
    #Pass the obtained image data into self.process for gesture recognition
    self.process(rgb_image)
```

The `process` function handles image processing:

```python
def process(self, frame):
    #Call the findHands function to detect the palm. The function will return the
lmList list, which stores the detection results.
    frame, lmList, bbox = self.hand_detector.findHands(frame)
    #If the detection list is not empty, it means that a palm is detected, and
self.pub_gesture is True, which means that the gesture topic can be published
    if len(lmList) != 0 and self.pub_gesture == True:
        #Start the thread and execute the gesture recognition program
        gesture = threading.Thread(target=self.Gesture_Detect_threading, args=
(lmList,bbox))
        gesture.start()
        gesture.join()
    self.cTime = time.time()
    fps = 1 / (self.cTime - self.pTime)
    self.pTime = self.cTime
    text = "FPS : " + str(int(fps))
    cv.putText(frame, text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255),
1)
    #self.media_ros.pub_imgMsg(frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
    cv.imshow('frame', frame)
```

The `Gesture_Detect_threading` function performs gesture detection:

```python
def Gesture_Detect_threading(self, lmList,bbox):
```

```
#Call fingersUp function to return the number of fingers extended
    fingers = self.hand_detector.fingersUp(lmList)
    print("sum of fingers: ",sum(fingers))
    print(self.pub_gesture)
    #If the number of fingers stretched is the same as last time, then start
counting
    if sum(fingers) == self.last_sum:
        print("---------------------------")
        self.cnt = self.cnt + 1
        print("cnt: ",self.cnt)
        #The cumulative count reaches 30, indicating that the gesture
recognition results of 30 times are the same. The gesture recognition program
ends, the buzzer sounds once, and the gesture recognition result topic is
published.
        if self.cnt==30 and self.pub_gesture == True:
            self.Beep_Loop()
            print("sum of fingers: ",self.last_sum)
            self.pub_gesture = False
            sum_gesture = Int16()
            sum_gesture.data = self.last_sum
            self.pub_GesturetId.publish(sum_gesture)
    else:
        self.cnt = 0
    #Change the gesture result of the last recognition to the current number of
fingers stretched
    self.last_sum = sum(fingers)
```

### 3.2. apriltagID_gesture.py

Program code path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/apriltagID_gesture.py
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/M3Pro_demo/M3Pro_demo/apriltagID_gesture.py
```

Import the required libraries:

```python
import cv2
import os
import numpy as np
import message_filters
from M3Pro_demo.vutils import draw_tags
from dt_apriltags import Detector
from cv_bridge import CvBridge
import cv2 as cv
from arm_interface.srv import ArmKinemarics
from arm_interface.msg import AprilTagInfo,CurJoints
from arm_msgs.msg import ArmJoints
from arm_msgs.msg import ArmJoint
from M3Pro_demo.Robot_Move import *
from M3Pro_demo.compute_joint5 import *
from std_msgs.msg import Float32,Bool,UInt16,Int16
```

```python
import time
import yaml
import math
from rclpy.node import Node
import rclpy
from message_filters import Subscriber,
TimeSynchronizer,ApproximateTimeSynchronizer
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
import transforms3d as tfs
import tf_transformations as tf
```

Initialize the node and create the publishers and subscribers:

```python
def __init__(self, name):
    super().__init__(name).
    #Robot arm sorting posture
    self.init_joints = [90, 120, 0, 0, 90, 90]
    self.identify_joints = [90, 150, 12, 20, 90, 0]
    #Define the array to store the end posture of the robotic arm
    self.CurEndPos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self.rgb_bridge = CvBridge()
    self.depth_bridge = CvBridge()
    self.pubPos_flag = False
    self.at_detector = Detector(searchpath=['apriltags'],
                                families='tag36h11',
                                nthreads=8,
                                quad_decimate=2.0,
                                quad_sigma=0.0,
                                refine_edges=1,
                                decode_sharpening=0.25,
                                debug=0)
    self.Center_x_list = []
    self.Center_y_list = []
    self.pos_info_pub = self.create_publisher(AprilTagInfo,"PosInfo",1)
    self.CmdVel_pub = self.create_publisher(Twist,"cmd_vel",1)
    self.sub_grasp_status =
self.create_subscription(Bool,"grasp_done",self.get_graspStatusCallBack,100)
    self.pub_cur_joints = self.create_publisher(CurJoints,"Curjoints",1)
    #Define the publisher of the reset gesture result topic
    self.pub_reset_gesture = self.create_publisher(Bool,"reset_gesture",1)
    self.TargetAngle_pub = self.create_publisher(ArmJoints, "arm6_joints", 10)
    self.pub_SingleTargetAngle = self.create_publisher(ArmJoint, "arm_joint",
10)
    self.rgb_image_sub = Subscriber(self, Image, '/camera/color/image_raw')
    self.depth_image_sub = Subscriber(self, Image, '/camera/depth/image_raw')
    self.client = self.create_client(ArmKinemarics, 'get_kinemarics')
    self.TargetJoint5_pub = self.create_publisher(Int16, "set_joint5", 10)
    self.get_current_end_pos()
    self.pubCurrentJoints()
    #Define the subscriber who subscribes to the gesture recognition result
topic
    self.sub_GesturetId =
self.create_subscription(Int16,"GesturetId",self.get_GesturetIdCallBack,1)
    self.ts = ApproximateTimeSynchronizer([self.rgb_image_sub,
self.depth_image_sub], 1, 0.5)
    #Define the publisher to publish the buzzer control topic
```

```
self.pub_beep = self.create_publisher(UInt16, "beep", 10)
    self.ts.registerCallback(self.callback)
    self.camera_info_K = [477.57421875, 0.0, 319.3820495605469, 0.0,
477.55718994140625, 238.64108276367188, 0.0, 0.0, 1.0]
    self.EndToCamMat = np.array([[ 0 ,0 ,1 ,-1.00e-01],
                                 [-1 ,0 ,0 ,0],
                                 [0 ,-1 ,0 ,4.82000000e-02],
                                 [ 0.00000000e+00 , 0.00000000e+00 ,
0.00000000e+00 , 1.00000000e+00]])
    time.sleep(2)
    self.TargetID = 0
    self.detect_flag = False
    self.x_offset = offset_config.get('x_offset')
    self.y_offset = offset_config.get('y_offset')
    self.z_offset = offset_config.get('z_offset')
    self.adjust_dist = True
    self.linearx_PID = (0.5, 0.0, 0.2)
    self.linearx_pid = simplePID(self.linearx_PID[0] / 1000.0,
self.linearx_PID[1] / 1000.0, self.linearx_PID[2] / 1000.0)
    self.joint5 = Int16()
    self.count = False
    self.start_time = 0.0
    self.index = None
```

The image-topic callback processes camera frames:

```python
def callback(self,color_msg,depth_msg):
    rgb_image = self.rgb_bridge.imgmsg_to_cv2(color_msg, "rgb8")
    depth_image = self.depth_bridge.imgmsg_to_cv2(depth_msg, "32FC1")
    depth_to_color_image = cv.applyColorMap(cv.convertScaleAbs(depth_image,
alpha=1.0), cv.COLORMAP_JET)
    frame = cv.resize(depth_image, (640, 480))
    depth_image_info = frame.astype(np.float32)
    tags = self.at_detector.detect(cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY),
False, None, 0.025)
    self.Center_x_list = list(range(len(tags)))
    self.Center_y_list = list(range(len(tags)))
    draw_tags(rgb_image, tags, corners_color=(0, 0, 255), center_color=(0, 255,
0))
    key = cv2.waitKey(10)
    if key == 32:
        self.pubPos_flag = True
    if self.count==True:
        if (time.time() - self.start_time)>8:
            self.pubPos_flag = True
            self.count = False
    if len(tags) > 0 :
        for i in range(len(tags)):
            center_x, center_y = tags[i].center
            self.Center_x_list[i] = center_x
            self.Center_y_list[i] = center_y
            cur_id = tags[i].tag_id
            cx = center_x
            cy = center_y
            cz = depth_image_info[int(cy),int(cx)]/1000
            print("cx: ",cx)
            print("cy: ",cy)
```

```
print("cz: ",cz)
            pose = self.compute_heigh(cx,cy,cz)
            dist_detect = math.sqrt(pose[1] ** 2 + pose[0]** 2)
            dist_detect = dist_detect*1000
            dist = 'dist: ' + str(dist_detect) + 'mm'
            cv.putText(rgb_image, dist, (int(cx)+5, int(cy)+15),
cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            #If the current ID is the target ID, it means the target machine
code has been found
            if cur_id == self.TargetID and self.pubPos_flag==True:
                print("Found the target.")
                #Change the value of self.detect_flag to indicate that the target
ID machine code has been found
                self.detect_flag = True
                #Store the array index of tags of the target ID machine code
                self.index = i
            print("self.index: ",self.index)
            #If the target ID machine code is found and chassis adjustment is
enabled, and the distance between the machine code block and the car base_link is
outside the range [210, 220]
            if abs(dist_detect - 215.0)>5 and self.adjust_dist==True and
self.detect_flag == True and self.index!=None:
                print("Adjusting")
                #Call move_dist to control the chassis movement and adjust the
distance
                self.move_dist(dist_detect)
             #If the target ID machine code is found and the distance between
the machine code block and the car base_link is within the range of [210, 220]
            elif abs(dist_detect - 215.0)<5 and self.detect_flag == True and
self.index!=None:
                self.pubVel(0,0,0)
                self.adjust_dist = False
                tag = AprilTagInfo()
                tag.id = tags[self.index].tag_id
                #Find the target machine code through the array subscript and
extract the center coordinates xy
                tag.x = float(self.Center_x_list[self.index])
                tag.y = float(self.Center_y_list[self.index])
                tag.z = depth_image_info[int(tag.y),int(tag.x)]/1000
                vx = int(tags[self.index].corners[0][0]) -
int(tags[self.index].corners[1][0])
                vy = int(tags[self.index].corners[0][1]) -
int(tags[self.index].corners[1][1])
                target_joint5 = compute_joint5(vx,vy)
                print("target_joint5: ",target_joint5)
                self.joint5.data = int(target_joint5)
                if tag.z!=0 and self.pubPos_flag == True :
                    #Publish machine code location topic message
                    self.pos_info_pub.publish(tag)
                    self.TargetJoint5_pub.publish(self.joint5)
                    self.pubPos_flag = False
                    self.index = None
                else:
                    print("Invalid distance.")
        #If the machine code location topic is enabled but the target ID machine
code is not found, the buzzer sounds once and the reset gesture topic is
published
```

```
if self.detect_flag == False and self.TargetID!=0 and
self.pubPos_flag==True:
            self.pubPos_flag = False
            self.Beep_Loop()
            self.shake()
            print("Did not find the target.")
            self.TargetID = 0
            reset = Bool()
            reset.data = True
            self.pub_reset_gesture.publish(reset)
    #If the machine code location topic is enabled but no machine code is found,
the buzzer sounds and the reset gesture topic is published
    elif self.pubPos_flag==True and len(tags)==0:
        self.pubVel(0,0,0)
        self.Beep_Loop()
        self.shake()
        reset = Bool()
        reset.data = True
        self.pub_reset_gesture.publish(reset)
        self.pubPos_flag = False
        print("Did not find any target.")
    rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow("result_image", rgb_image)
    cv2.imshow("depth_image", depth_to_color_image)
    key = cv2.waitKey(1)
```
