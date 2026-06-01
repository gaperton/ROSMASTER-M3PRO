# MoveIt2 Simulation-Reality Linkage

Raspberry Pi 5 and Jetson Nano run ROS in Docker, so MoveIt2 performance is usually limited on those boards. Raspberry Pi 5 and Jetson Nano users should run these MoveIt2 examples in the virtual machine. Orin users can run the same commands directly on the robot because ROS runs directly on the Orin mainboard.

This lesson uses the virtual machine as the example environment.

## 1. Content Description

This lesson connects the simulated robotic arm in RViz to the physical robotic arm, allowing MoveIt2 motion plans to drive the real arm.

## 2. Preparation

The physical robotic arm does not provide independent obstacle avoidance. Before driving the real arm, make sure the area around the arm is clear.

### 2.1. Start the Agent

Start the agent on the robot mainboard. The agent starts the control node that controls the robot and chassis. It normally starts automatically when the robot boots. If it is not running, start it from the robot terminal:

```bash
sh start_agent.sh
```

### 2.2. Distributed Communication Between the Virtual Machine and Robot

The virtual machine and robot must be able to communicate:

- Put both devices on the same local network. The simplest method is to connect them to the same Wi-Fi network.
- Make sure both systems use the same `ROS_DOMAIN_ID`. The robot default is `30`, and the virtual machine default is also `30`. If they differ, edit `~/.bashrc` in the virtual machine, set `ROS_DOMAIN_ID` to match the robot, save the file, and run `source ~/.bashrc`.
- On the virtual machine, run `ros2 node list`. If `/YB_Node` appears, distributed ROS 2 communication is working.

## 3. Program Startup

Start MoveIt2 in the virtual machine:

```bash
ros2 launch test_moveit_config demo.launch.py
```

When the terminal displays **"You can start planning now!"**, MoveIt2 has started successfully.

![Figure: page 1: figure 4](_page_1_Figure_4.jpeg)

At this point, the simulated arm is straightened upward. After the real-machine bridge starts, the physical arm will also straighten upward. Keep the arm in an open area before running the next command. In the virtual machine terminal, start the bridge program:

```bash
ros2 run MoveIt_SimToMachine SimulationToMachine
```

After the program starts, the physical robotic arm straightens upward to match the arm in RViz.

Next, plan a motion from the current `up` pose to the preset `init` pose. In RViz, set [Planning Group] to `arm_group`, select [Start State], select [Goal State], and choose the configured `init` pose. Then click [Plan&Execute].

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

The RViz arm plans first and then slowly moves to the `init` posture. The physical robotic arm follows the same movement.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

## 4. Node Communication

Run the following command in the virtual machine to view the current node communication graph:

```bash
ros2 run rqt_graph rqt_graph
```

Select [Nodes/Topics (all)] in the upper-left corner, then click the refresh button to display the graph.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

Focus on the following part of the graph:

![Figure: page 3: figure 2](_page_3_Figure_2.jpeg)

This graph shows communication between the three main nodes.

## 5. Core Code Analysis

Program source code path in the virtual machine:

```text
/home/yahboom/moveit2_ws/src/MoveIt_SimToMachine/MoveIt_SimToMachine/SimulationToMachine.py
```

Import the required libraries:

```python
import rclpy
from rclpy.node import Node
from control_msgs.msg import JointTrajectoryControllerState
from math import pi
import numpy as np
from arm_msgs.msg import ArmJoints
```

Initialize the program and create topic subscribers and publishers:

```python
def __init__(self, name):
    super().__init__(name)
    #Create a subscriber and define the /arm_group_controller/state topic message
published by the MoveIt node
    self.sub_state
=self.create_subscription(JointTrajectoryControllerState,"/arm_group_controller/
state",self.get_ArmPosCallback,1)
    #Create a publisher to publish the control topic message of six servo angles,
and the underlying control node subscribes to the message
    self.pub_SixTargetAngle = self.create_publisher(ArmJoints, "arm6_joints",
10)
    self.joints = [90.0, 90.0, 90.0, 90.0, 90.0, 30.0]
```

The `/arm_group_controller/state` callback receives controller state messages:

```python
def get_ArmPosCallback(self,msg):
    #print("Get the position of arm : ",msg.actual.positions)
    #Get the actual joint status of the robotic arm
    arm_rad = np.array(msg.actual.positions)
    DEG2RAD = np.array([180 / pi])
    #Convert angle to radians
    arm_deg = np.dot(arm_rad.reshape(-1, 1), DEG2RAD)
    #Median value of robotic arm
    mid = np.array([90, 90, 90, 90, 90])
    #mid = np.array([0, 0, 0, 0, 0])
    #Calculate absolute joint angles
    arm_array = np.array(np.array(arm_deg) + mid)
    #Assign values to servos 1-5
    for i in range(5): self.joints[i] = arm_array[i]
    print("self.joints: ",self.joints)
    #Execute the function to publish the topic of servo angle
    self.pubSixArm(self.joints)
```

The servo-angle publishing function sends the target joint angles:

```python
def pubSixArm(self, joints, id=6, angle=180.0, runtime=2000):
    #Create topic data object
    arm_joints =ArmJoints()
    #Assign values to the data in the topic data object
    arm_joints.joint1 = int(joints[0])
    arm_joints.joint2 = int(joints[1])
    arm_joints.joint3 = int(joints[2])
    arm_joints.joint4 = int(joints[3])
    arm_joints.joint5 = int(joints[4])
    arm_joints.joint6 = int(joints[5])
    arm_joints.time = runtime self.pub_SixTargetAngle.publish(arm_joints)
    #Publish topic data
    self.pub_SixTargetAngle.publish(arm_joints)
```
