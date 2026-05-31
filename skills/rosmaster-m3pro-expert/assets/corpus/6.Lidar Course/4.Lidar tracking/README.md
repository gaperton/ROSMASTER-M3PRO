# LiDAR tracking

## 1. Content Description

This section explains the LiDAR tracking example. The program searches the fused scan for the nearest object in front of the robot, then uses PID control to keep the chassis aligned with the object and maintain a target distance.

This section requires terminal commands. The terminal you use depends on the mainboard type. This section uses the Raspberry Pi 5 as an example. For Raspberry Pi and Jetson Nano mainboards, open a terminal and enter the Docker container. After entering the Docker container, run the commands from this section there. For instructions on entering a Docker container, refer to the product tutorial **[Robot Configuration and Operation Guide] - [Entering the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

On an Orin mainboard, open a terminal directly and run the commands from this section.

## 2. Program Startup

First, start the LiDAR driver, fusion, and filtering launch file:

```bash
ros2 launch yahboom_M3Pro_laser laser_driver.launch.py
```

Optionally, refer to [5. Chassis Control] - [2. Gamepad Control] to start gamepad control. Press R2 on the gamepad to pause or resume LiDAR tracking. The program can still run if gamepad control is not started. Run the following command to start LiDAR tracking:

```bash
ros2 run yahboom_M3Pro_laser laser_Tracker
```

After the program starts, place an object in the LiDAR detection range and move it slowly. The robot follows the nearest detected object, keeping roughly 0.55 m of distance while turning to keep the object in front of the chassis.

## 3. Core Code Analysis

Program code path:

Raspberry Pi and Jetson Nano boards

The program code is in the running Docker. The path in Docker is /root/yahboomcar_ws/src/yahboom_M3Pro_laser/yahboom_M3Pro_laser/laser_Tracker.py

Orin mainboard

The program code path is /home/jetson/yahboomcar_ws/src/yahboom_M3Pro_laser/yahboom_M3Pro_laser/laser_Tracker.py

Import the required libraries:

```python
#ros lib
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
#commom lib
import math
import numpy as np
import time
from time import sleep
#Import chassis PID control related libraries
from yahboom_M3Pro_laser.common import *
import os
```

The program initializes publishers and subscribers:

```python
def __init__(self,name):
    super().__init__(name)
    #create a sub
    #Create a subscriber to subscribe to the fused radar topic message
    self.sub_laser =
self.create_subscription(LaserScan,"/scan",self.registerScan,1)
    #Create a subscriber to subscribe to the handle remote control topic message
    self.sub_JoyState = self.create_subscription(Bool,'/JoyState',
self.JoyStateCallback,1)
    #create a pub
    #Create a publisher to publish speed topic message
    self.pub_vel = self.create_publisher(Twist,'/cmd_vel',1)
    #declareparam
    self.declare_parameter("linear",0.5)
    self.linear =
self.get_parameter('linear').get_parameter_value().double_value
    self.declare_parameter("angular",1.0)
    self.angular =
self.get_parameter('angular').get_parameter_value().double_value
    # Radar detection angle
    self.declare_parameter("LaserAngle",45.0)
    self.LaserAngle =
self.get_parameter('LaserAngle').get_parameter_value().double_value
    #The detection distance of the obstacle. If it is less than this value, it
means there is an obstacle.
    self.declare_parameter("ResponseDist",0.55)
    self.ResponseDist =
self.get_parameter('ResponseDist').get_parameter_value().double_value
    #Handle control flag, the value is True means the handle controls the car,
you need to press the R2 key on the handle to take handle control or enable
handle control
```

```
self.Joy_active = False
#Create a linear speed PID control object
self.lin_pid = SinglePID(1.0, 0.0, 1.0)
#Create angular velocity PID control object
self.ang_pid = SinglePID(2.0, 0.0, 2.0)
```

The registerScan callback finds the nearest valid scan point and computes the tracking command:

```python
def registerScan(self, scan_data):
    if not isinstance(scan_data, LaserScan): return
    ranges = np.array(scan_data.ranges)
    minDistList = []
    minDistIDList = []
    for i in range(len(ranges)):
        #Convert the radians in the radar topic data into degrees
        angle = (scan_data.angle_min + scan_data.angle_increment * i) * RAD2DEG
        #If the current angle is within the detection range and the distance
corresponding to the angle is not equal to 0
        if abs(angle) < self.LaserAngle and ranges[i] !=0.0 :
            #Add the distance of this angle to the minimum distance list
            minDistList.append(ranges[i])
            #Add the angle to the minimum ID list
            minDistIDList.append(angle)
    #If the length of the minimum distance list is not 0, it means that the
nearest distance object has been detected
    if len(minDistList) != 0:
        # Find the minimum value in the distance list
        minDist = min(minDistList)
        #Find the smallest angle based on the shortest distance
        minDistID = minDistIDList[minDistList.index(minDist)]
    else:
        #self.pub_vel.publish(Twist())
        print("-----------------------")
        return
    #If self.Joy_active is True, publish the parking speed and exit this callback
function
    if self.Joy_active :
        self.pub_vel.publish(Twist())
        return
    velocity = Twist()
    print("minDist: ",minDist)
    print("minDistID: ",minDistID)
    #If the minimum distance is less than 0.1 meters from the set value, update
the current minimum distance to the set distance value
    if abs(minDist - self.ResponseDist) < 0.1: minDist = self.ResponseDist
    #Calculate linear velocity
    velocity.linear.x = -self.lin_pid.pid_compute(self.ResponseDist, minDist)
    #Calculate angular velocity
    ang_pid_compute = self.ang_pid.pid_compute(abs(minDistID) / 72, 0)
    #If the minimum angle is greater than 0, it means it is on the left side of
the car, so the car turns right
    if 0< minDistID :
        velocity.angular.z = ang_pid_compute
   #If the minimum angle is less than 0, it means it is on the right side of the
car, so the car turns left
    elif minDistID <0:
        velocity.angular.z = -ang_pid_compute
```

```
if abs(ang_pid_compute) < 0.5: velocity.angular.z = 0.0
velocity.angular.z = velocity.angular.z *0.6
print("angular.z: ",velocity.angular.z)
#Release speed control topic
self.pub_vel.publish(velocity)
```
