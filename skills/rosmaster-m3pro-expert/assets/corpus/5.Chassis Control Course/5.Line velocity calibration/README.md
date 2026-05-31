# Linear Velocity Calibration

## 1. Course Content

Learn how to calibrate robot linear velocity. After the program starts, click **Start** in the visual interface. The chassis moves forward and stops when the error is less than the tolerance value.

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

Run the linear velocity calibration node:

```bash
ros2 launch calibration calibrate_linear.launch.py
```

If an error appears during the first run indicating that there is no TF transform, press Ctrl+C to exit and run the program again.

Open the dynamic parameter adjuster:

```bash
ros2 run rqt_reconfigure rqt_reconfigure
```

Click the **calibrate_linear** node in the node list on the left.

![Picture: page 2: picture 4](_page_2_Picture_4.jpeg)

Note: The nodes may not appear the first time you open the tool. Click **Refresh** to display all nodes. The **calibrate_linear** node is used to calibrate linear velocity.

The rqt parameters are:

- `test_distance`: Calibration test distance. This example moves forward 1 meter.
- `speed`: Linear speed.
- `tolerance`: Allowed error tolerance.
- `odom_linear_scale_correction`: Linear velocity scale correction. If the test result is not ideal, modify this value.
- `start_test`: Test switch.
- `direction`: Can be ignored for this robot. It is used for McWheel chassis structures to calibrate left/right movement.
- `base_frame`: Base coordinate frame name.
- `odom_frame`: Odometry coordinate frame name.

### 3.2 Start Calibration

In `rqt_reconfigure`, select the `calibrate_linear` node. If it is not displayed, click **Refresh**.

Choose a known ground reference, such as a tape measure or tile. Set `test_distance` to the actual test distance. This example uses 1 meter. Click the `start_test` box to start calibration.

The robot monitors the TF transform between `base_footprint` and `odom`, calculates the theoretical distance traveled, and stops when the error is less than `tolerance`. The terminal prints `done` after the stop command is sent.

If the actual distance traveled is less than 1 meter, increase `odom_linear_scale_correction` appropriately. After modifying the value, click a blank area so the parameter is written, reset `start_test`, and then start calibration again. Record the final calibrated `odom_linear_scale_correction` value.

### 3.3 Write Calibration Parameters to the Chassis

To write parameters to the chassis, first disconnect the chassis agent. Press Ctrl+C or close the agent terminal.

Open `config_robot.py` in the robot home directory.

![Picture: page 4: picture 2](_page_4_Picture_2.jpeg)

Uncomment line 551, enter the calibrated coefficient in `robot.set_ros_scale_line(xx)`, and save the file.

Open a terminal on the robot and run:

```bash
python3 config_robot.py
```

Wait for parameter writing to finish. The terminal prints the written value, such as `ros_scale_line:0.890`, indicating that linear velocity calibration is complete.

## 4. Source Code Analysis

Source code path on Jetson Orin Nano and Jetson Orin NX:

```text
/home/jetson/M3Pro_ws/src/calibration/calibration/calibrate_linear.py
```

For Jetson Nano and Raspberry Pi, enter Docker first.

### 4.1 View the Node Relationship Graph

Open a terminal and run:

```bash
ros2 run rqt_graph rqt_graph
```

![Figure: page 5: figure 12](_page_5_Figure_12.jpeg)

In the node relationship graph:

- `imu_filter` filters raw chassis IMU data from `/imu/data_raw` and publishes filtered data to `/imu/data`.
- `/ekf_filter_node` subscribes to raw odometry `/odom_raw` and filtered IMU data `/imu/data`, performs data fusion, and publishes `/odom`.
- `calibrate_linear` monitors the TF transform from `odom` to `base_footprint` and publishes `/cmd_vel` to control chassis movement.

### 4.2 Source Code Analysis

The `get_position` method in the `CalibrateLinear` class monitors TF coordinate transforms.

```python
def get_position(self):
    try:
        now = rclpy.time.Time()
        transform = self.tf_buffer.lookup_transform(
            self.base_frame,
            self.odom_frame,
            now,
            timeout=rclpy.duration.Duration(seconds=1.0)
        )
        return transform
    except (LookupException, ConnectivityException, ExtrapolationException):
        self.get_logger().info('transform not ready')
        raise
```

The `on_timer` method, the timer callback in the `CalibrateLinear` class, calculates chassis displacement and controls chassis movement.

```python
def on_timer(self):
    move_cmd = Twist()
    self.start_test = self.get_parameter(
        'start_test'
    ).get_parameter_value().bool_value
    self.odom_linear_scale_correction = self.get_parameter(
        'odom_linear_scale_correction'
    ).get_parameter_value().double_value
    self.direction = self.get_parameter(
        'direction'
    ).get_parameter_value().bool_value
    self.test_distance = self.get_parameter(
        'test_distance'
    ).get_parameter_value().double_value
    self.tolerance = self.get_parameter(
        'tolerance'
    ).get_parameter_value().double_value
    self.speed = self.get_parameter(
        'speed'
    ).get_parameter_value().double_value

    if self.start_test:
        self.position.x = self.get_position().transform.translation.x
        self.position.y = self.get_position().transform.translation.y
        self.get_logger().info(f"self.position.x: {self.position.x}")
        self.get_logger().info(f"self.position.y: {self.position.y}")
        distance = sqrt(
            pow((self.position.x - self.x_start), 2) +
            pow((self.position.y - self.y_start), 2)
        )
        distance *= self.odom_linear_scale_correction
        self.get_logger().info(f"distance: {distance}")
        error = distance - self.test_distance
        self.get_logger().info(f"error: {error}")

        if abs(error) < self.tolerance:
            self.start_test = rclpy.parameter.Parameter(
                'start_test',
                rclpy.Parameter.Type.BOOL,
                False
            )
            all_new_parameters = [self.start_test]
            self.set_parameters(all_new_parameters)
            self.get_logger().info("done")
        else:
            if self.direction:
                print("x")
                move_cmd.linear.x = copysign(self.speed, -1 * error)
            else:
                move_cmd.linear.y = copysign(self.speed, -1 * error)
                print("y")
        self.cmd_vel.publish(move_cmd)
    else:
        self.x_start = self.get_position().transform.translation.x
        self.y_start = self.get_position().transform.translation.y
        self.get_logger().info(f"self.x_start: {self.x_start}")
        self.get_logger().info(f"self.y_start: {self.y_start}")
        self.cmd_vel.publish(Twist())
```
