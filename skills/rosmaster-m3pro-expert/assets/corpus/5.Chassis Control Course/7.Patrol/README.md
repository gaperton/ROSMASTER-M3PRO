# Patrol

## 1. Course Content

Learn the robot patrol function.

Set the patrol route in the dynamic parameter controller and click **Start**. The robot moves along the patrol route while LiDAR scans for obstacles within the specified angle and detection distance. If an obstacle is detected, the robot stops and the buzzer sounds. When no obstacle is detected, the robot resumes patrolling.

## 2. Preparation

### 2.1 Content Description

This lesson uses Jetson Orin NX as the example. For Raspberry Pi and Jetson Nano boards, open a terminal, enter the Docker container, and then run the commands from this lesson inside the container. For instructions, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

For Orin and NX boards, open a terminal directly on the robot and run the commands from this lesson.

### 2.2 Start the Agent

The Docker agent must be started before testing. If it is already running, you do not need to restart it.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

## 3. Run the Example

### Notice

Jetson Nano and Raspberry Pi users must enter the Docker container first.

### 3.1 Start the Program

Run the patrol node in the robot terminal:

```bash
ros2 launch patrol patrol.launch.py
```

Using the accompanying virtual machine as an example, run the parameter configuration node:

```bash
ros2 run rqt_reconfigure rqt_reconfigure
```

Click the **Patrol** node in the left options bar. If no node appears when the tool first opens, click **Refresh**.

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

The **Command** field sets the patrol route. This example uses a square patrol route. After setting the route in **Command**, click **Switch** to start patrolling. The terminal prints status information.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

If there is an obstacle on the patrol path, the robot stops and prints the **obstacle** prompt.

The rqt parameters are:

- `odom_frame`: Odometry coordinate frame name.
- `base_frame`: Base coordinate frame name.
- `circle_adjust`: Adjustment coefficient for circular patrol route size. See the code for details.
- `Switch`: Patrol switch.
- `Command`: Patrol route. Available routes include `LengthTest` for linear patrol, `Circle` for circular patrol, `Square` for square patrol, and `Triangle` for triangular patrol.
- `Set_loop`: Restart patrol. When enabled, patrol continues in a loop along the specified route.
- `ResponseDist`: Obstacle detection distance.
- `LaserAngle`: LiDAR detection angle.
- `Linear`: Linear velocity.
- `Angular`: Angular velocity.
- `Length`: Linear movement distance.
- `RotationTolerance`: Rotation error tolerance.
- `RotationScaling`: Rotation scaling factor.

## 4. Source Code Analysis

Source code path on Jetson Orin Nano and Jetson Orin NX:

```text
/home/jetson/M3Pro_ws/src/patrol/patrol/patrol.py
```

For Jetson Nano and Raspberry Pi, enter Docker first. Source code path:

```text
/root/M3Pro_ws/src/patrol/patrol/patrol.py
```

### 4.1 View the Node Relationship Graph

Open a terminal and run:

```bash
ros2 run rqt_graph rqt_graph
```

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

In the node relationship graph:

- `patrol` is the main node for the patrol function. It subscribes to the coordinate transform between odometry data `odom` and `base_footprint`, and uses `/scan1` LiDAR data to detect obstacles ahead.
- `YB_Node` publishes LiDAR data `/scan1` and raw odometry `/odom_raw`. It subscribes to `/cmd_vel` to control chassis motion through inverse kinematics.
- `ekf_filter_node` uses an extended Kalman filter to fuse raw odometry with filtered IMU data and publishes fused odometry to `/odom`.
- `imu_filter` filters raw IMU data `/imu/data_raw` and publishes filtered data to `/imu/data`.

### 4.2 Program Flowchart

The flowchart image is large. View the original image in this lesson's folder.

### 4.3 Key Program Logic

Movement status acquisition monitors the TF transforms between `odom` and `base_footprint`, then calculates the current XY coordinates and rotation angle. This is implemented by the `get_position` and `get_odom_angle` methods in the `YahboomCarPatrol` class.

```python
def get_position(self):
    try:
        now = rclpy.time.Time()
        trans = self.tf_buffer.lookup_transform(
            self.odom_frame,
            self.base_frame,
            now
        )
        return trans
    except (LookupException, ConnectivityException, ExtrapolationException):
        self.get_logger().info('transform not ready')
        raise

def get_odom_angle(self):
    try:
        now = rclpy.time.Time()
        rot = self.tf_buffer.lookup_transform(
            self.odom_frame,
            self.base_frame,
            now
        )
        cacl_rot = PyKDL.Rotation.Quaternion(
            rot.transform.rotation.x,
            rot.transform.rotation.y,
            rot.transform.rotation.z,
            rot.transform.rotation.w
        )
        angle_rot = cacl_rot.GetRPY()[2]
    except (LookupException, ConnectivityException, ExtrapolationException):
        self.get_logger().info('transform not ready')
        return
    return angle_rot
```

Movement control handles basic chassis movement. All patrol routes are combinations of linear movement and rotation. This is implemented by the `advancing` and `Spin` methods in the `YahboomCarPatrol` class.

```python
def advancing(self, target_distance):
    self.position.x = self.get_position().transform.translation.x
    self.position.y = self.get_position().transform.translation.y
    move_cmd = Twist()
    self.distance = sqrt(
        pow((self.position.x - self.x_start), 2) +
        pow((self.position.y - self.y_start), 2)
    )
    self.distance *= self.LineScaling
    self.get_logger().info(f"distance: {self.distance}")
    self.error = self.distance - target_distance
    move_cmd.linear.x = self.Linear

    if abs(self.error) < self.LineTolerance:
        self.get_logger().info("stop")
        self.distance = 0.0
        self.pub_cmdVel.publish(Twist())
        self.x_start = self.position.x
        self.y_start = self.position.y
        self.Switch = rclpy.parameter.Parameter(
            'Switch',
            rclpy.Parameter.Type.BOOL,
            False
        )
        all_new_parameters = [self.Switch]
        self.set_parameters(all_new_parameters)
        return True
    else:
        if self.Joy_active or self.front_warning > 10:
            if self.moving == True:
                self.pub_cmdVel.publish(Twist())
                self.moving = False
                self.get_logger().info("obstacles")
        else:
            self.pub_cmdVel.publish(move_cmd)
        self.moving = True
        return False
```

```python
def Spin(self, angle):
    self.target_angle = radians(angle)
    self.odom_angle = self.get_odom_angle()
    self.delta_angle = (
        self.RotationScaling *
        self.normalize_angle(self.odom_angle - self.last_angle)
    )
    self.turn_angle += self.delta_angle
    self.get_logger().info(f"turn_angle: {self.turn_angle}")
    self.error = self.target_angle - self.turn_angle
    self.get_logger().info(f"error: {self.error}")
    self.last_angle = self.odom_angle
    move_cmd = Twist()

    if abs(self.error) < self.RotationTolerance or self.Switch == False:
        self.pub_cmdVel.publish(Twist())
        self.turn_angle = 0.0
        return True

    if self.Joy_active or self.front_warning > 10:
        if self.moving == True:
            self.pub_cmdVel.publish(Twist())
            self.moving = False
            self.get_logger().info("obstacles")
    else:
        if self.Command == "Square" or self.Command == "Triangle":
            move_cmd.angular.z = copysign(self.Angular, self.error)
        elif self.Command == "Circle":
            length = self.Linear * self.circle_adjust / self.Length
            move_cmd.linear.x = self.Linear
            move_cmd.angular.z = copysign(length, self.error)
        self.pub_cmdVel.publish(move_cmd)
    self.moving = True
```
