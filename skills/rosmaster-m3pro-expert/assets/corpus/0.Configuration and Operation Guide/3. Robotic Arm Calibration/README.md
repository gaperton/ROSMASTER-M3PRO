# Robotic Arm Calibration

Mechanical calibration has two steps: center-position calibration and offset calibration.

## 1. Jetson Orin Nano/NX Version

Skip this section if you are using the Raspberry Pi 5 or Jetson Nano version.

### 1.1 Calibrate the Center Position

If you are using the Yahboom factory image, the communication agent starts automatically at boot.

Run the following command to move the robotic arm to an upright position, which makes calibration easier:

```bash
ros2 topic pub /arm6_joints arm_msgs/msg/ArmJoints {"joint1: 90, joint2: 90,
joint3: 90, joint4: 90, joint5: 90, joint6: 180, time: 1500"} --once
```

In the terminal running the agent, press Ctrl+C to stop the agent. Then run the following command to release the servos:

```bash
python3 ~/calibrate_arm.py
```

After the program starts, it should print the lower-level control board version, such as `V1.X`. If the version is not printed, run the program again, or confirm that the agent has released the communication serial port.

After the servos are released, you can move all six servos by hand. Check which servo is not aligned, then adjust the arm until it forms a straight line and the gripper is fully closed, forming the L-shaped pose shown below.

![Picture: page 1: picture 0](_page_1_Picture_0.jpeg)

In the terminal running `calibrate_arm.py`, enter `y` and press Enter to confirm that centering is complete. The program prints the state values for all six servos. Calibration succeeds only when each servo reports `state = 1`.

Run the following command to restart the communication agent:

```bash
sh start_agent.sh
```

### 1.2 Calibrate the Offset

Open a terminal on the Orin board and run the commands in this section. The screenshots use a Raspberry Pi 5 board as an example, but the procedure is the same.

Start the camera and robotic-arm kinematics solver:

```bash
ros2 launch M3Pro_demo camera_arm_kin.launch.py
```

Open a second terminal and start the offset calibration program:

```bash
ros2 run M3Pro_demo arm_offset
```

After the program starts, the robotic arm moves to the calibration pose and a camera window appears. Place the 4 x 4 x 4 cm wooden block, the largest block provided, inside the blue box in the marker-detection window, as shown below.

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

Press the space bar to complete offset calibration. The calibrated offset data is saved to `yahboomcar_ws/src/arm_kin/param/offset_value.yaml`.

Rebuild the `arm_kin` package so the updated calibration file takes effect:

```bash
cd ~/yahboomcar_ws
colcon build --packages-select arm_kin
```

## 2. Jetson Nano and Raspberry Pi 5 Version

Skip this section if you are using an Orin mainboard.

Raspberry Pi 5 and Jetson Nano users must perform these steps inside the Docker container. Open a terminal on the host system, enter the Docker container, then run the commands shown in this section. For details, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

### 2.1 Calibrate the Center Position

If you are using the Yahboom factory image, the communication agent starts automatically at boot.

Inside Docker, run the following command to move the robotic arm to an upright position, which makes calibration easier:

```bash
ros2 topic pub /arm6_joints arm_msgs/msg/ArmJoints {"joint1: 90, joint2: 90,
joint3: 90, joint4: 90, joint5: 90, joint6: 180, time: 1500"} --once
```

Press Ctrl+C to stop the agent, then run the following command inside Docker to release the servos:

```bash
python3 calibrate.py
```

After the program starts, it should print the lower-level control board version, such as `V1.X`. If the version is not printed, run the program again.

After the servos are released, you can move all six servos by hand. Check which servo is not aligned, then adjust the arm until it forms a straight line and the gripper is fully closed, as shown below.

![Picture: page 5: picture 0](_page_5_Picture_0.jpeg)

In the terminal running `calibrate.py`, enter `y` and press Enter to confirm that centering is complete. The program prints the state values for all six servos. Calibration succeeds only when each servo reports `state = 1`.

On the host system, run the following command to restart the communication agent:

```bash
sh start_agent.sh
```

### 2.2 Calibrate the Offset

Open a Docker terminal and start the camera and robotic-arm kinematics solver:

```bash
ros2 launch M3Pro_demo camera_arm_kin.launch.py
```

Open a second terminal and start the offset calibration program:

```bash
ros2 run M3Pro_demo arm_offset
```

After the program starts, the robotic arm moves to the calibration pose and a camera window appears. Place the 4 x 4 x 4 cm wooden block, the largest block provided, inside the blue box in the marker-detection window, as shown below.

![Picture: page 7: picture 0](_page_7_Picture_0.jpeg)

Press the space bar to complete offset calibration. The calibrated offset data is saved to `yahboomcar_ws/src/arm_kin/param/offset_value.yaml`.

Rebuild the `arm_kin` package so the updated calibration file takes effect:

```bash
cd ~/yahboomcar_ws
colcon build --packages-select arm_kin
```
