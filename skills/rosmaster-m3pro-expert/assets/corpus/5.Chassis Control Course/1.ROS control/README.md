# ROS Control

## 1. Course Content

Learn the basics of controlling the robot with ROS 2.

This lesson shows how to use ROS 2 topic tools to control robot speed, the buzzer, the light strip, and the robotic arm. It also shows how to read low-level data, such as LiDAR, IMU, battery, and odometry data.

## 2. Preparation

### 2.1 Content Description

This lesson uses Jetson Orin NX as the example. For Raspberry Pi and Jetson Nano boards, open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For instructions, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

For Orin and NX boards, open a terminal directly on the robot and run the commands from this lesson.

### 2.2 Start the Agent

The Docker agent must be started before testing. If it is already running, you do not need to restart it.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

## 3. Startup Commands

### 3.1 Function Description

This function controls the robot speed, buzzer, light strip, and robotic arm through ROS 2 topics. It can also read low-level data such as LiDAR, IMU, battery, and odometry data.

### 3.2 Start the Agent

After booting, open a terminal and run:

```bash
sh start_agent.sh
```

If startup fails, check whether the cable connections are loose and verify that the serial device is recognized:

```bash
ls /dev/myserial
```

### 3.3 View Node Information

Use the correct terminal for your board. Jetson Nano and Raspberry Pi 5 users should enter the Docker container first. Orin board users can run the command directly in the robot terminal.

After the agent connects successfully, list the ROS 2 nodes:

```bash
ros2 node list
```

If `/YB_Node` appears, the low-level control node has started. Query information about this node:

```bash
ros2 node info /YB_Node
```

The tables below show the topics this node subscribes to and publishes.

#### Subscribed Topics

| Topic        | Message type            | Description               |
|--------------|-------------------------|---------------------------|
| `/arm6_joints` | `arm_msgs/msg/ArmJoints` | Controls six servos       |
| `/arm_joint` | `arm_msgs/msg/ArmJoint` | Controls a single servo   |
| `/beep`      | `std_msgs/msg/UInt16`   | Controls the buzzer       |
| `/cmd_vel`   | `geometry_msgs/msg/Twist` | Controls robot movement |
| `/rgb`       | `std_msgs/msg/ColorRGBA` | Controls the light strip |

#### Published Topics

| Topic           | Message type                | Description                      |
|-----------------|-----------------------------|----------------------------------|
| `/battery`      | `std_msgs/msg/Float32`      | Publishes battery voltage data   |
| `/imu/data_raw` | `sensor_msgs/msg/Imu`       | Publishes raw IMU data           |
| `/odom_raw`     | `nav_msgs/msg/Odometry`     | Publishes raw odometry data      |
| `/scan0`        | `sensor_msgs/msg/LaserScan` | Publishes left rear LiDAR data   |
| `/scan1`        | `sensor_msgs/msg/LaserScan` | Publishes right front LiDAR data |

### 3.4 Publish Control Commands

Use the following command format to publish one frame of control data:

```text
ros2 topic pub <topic_name> <message_type> <message_data> --once
```

#### 3.4.1 Control Robot Speed

For the first test, place the robot so its wheels do not touch the ground. To move forward at a linear velocity of `0.1 m/s`, run:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" --once
```

After the command runs, the robot moves forward at `0.1 m/s`.

To rotate at an angular velocity of `1.0 rad/s`, run:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.0}}" --once
```

After the command runs, the robot rotates.

To stop the robot, publish zero linear and angular velocity:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" --once
```

The `--once` flag sends only one message frame. For more `ros2 topic pub` options, see **15. ROS 2 Basics - 19. Common ROS 2 Command Tools**.

#### 3.4.2 Control the Buzzer

Turn on the buzzer:

```bash
ros2 topic pub /beep std_msgs/msg/UInt16 "data: 1" --once
```

Turn off the buzzer:

```bash
ros2 topic pub /beep std_msgs/msg/UInt16 "data: 0" --once
```

#### 3.4.3 Control the Light Strip

Set the light strip to red:

```bash
ros2 topic pub /rgb std_msgs/msg/ColorRGBA "{r: 1.0, g: 0.0, b: 0.0, a: 1.0}" --once
```

#### 3.4.4 Control Six Servos

Set all six servo angles to 90 degrees so the robotic arm moves to an upright, straight posture.

Note: Keep clear of the robotic arm to avoid being hit.

```bash
ros2 topic pub /arm6_joints arm_msgs/msg/ArmJoints {"joint1: 90, joint2: 90,
joint3: 90, joint4: 90, joint5: 90, joint6: 90, time: 1500"} --once
```

The `time` value is the servo operation time in milliseconds.

#### 3.4.5 Control a Single Servo

Set servo No. 6, the gripper, to 150 degrees:

```bash
ros2 topic pub /arm_joint arm_msgs/msg/ArmJoint "{id: 6,joint: 150,time: 2000}" --once
```

### 3.5 Subscribe to Robot Data

Use the following command format to receive sensor data published by the robot node:

```text
ros2 topic echo <topic_name>
```

#### 3.5.1 Subscribe to LiDAR Data

This product has two LiDAR sensors. The left rear LiDAR topic is `/scan0`, and the right front LiDAR topic is `/scan1`.

For example, to view right front LiDAR data, run:

```bash
ros2 topic echo /scan1
```

For more information about LiDAR data, see **6. LiDAR Course**.

#### 3.5.2 Subscribe to Battery Voltage Data

The normal battery voltage should be above `10.3V` and below `12V`. If it falls below `10.3V`, the buzzer beeps to indicate that the battery voltage is too low and the battery needs to be charged.

Query the battery voltage:

```bash
ros2 topic echo /battery
```

For example, a displayed value of `11.8V` means the current battery voltage is 11.8 volts.

#### 3.5.3 Subscribe to IMU Data

The control board has a 9-axis IMU that provides robot attitude feedback. Read raw IMU data:

```bash
ros2 topic echo /imu/data_raw
```

#### 3.5.4 Subscribe to Odometry Data

The four motors include encoders. The ROS control board reads encoder information and publishes calculated odometry data. Read raw odometry data:

```bash
ros2 topic echo /odom_raw
```

Example output begins with fields like these:

```text
header:
stamp:
sec: 1749726281
nanosec: 816000000
frame_id: odom
child_frame_id: base_footprint
pose:
pose:
pose:
position:
```
