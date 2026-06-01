# Configuration and Operation Guide

This section gets the ROSMASTER-M3PRO from first power-on to a usable development state. It covers controller operation, remote login, source-code access, Docker access for Raspberry Pi 5 and Jetson Nano boards, robotic-arm calibration, control-board parameter updates, and hardware precautions for safe arm use.

Use this section before the numbered courses when you need to confirm basic robot operation, connect to the robot desktop, enter the correct runtime environment, calibrate the arm, or recover common configuration details.

## [0.1 Controller Quick Start](./1.%20Quick%20start%20handle%20to%20control%20the%20car/README.md)

Explains how to use the wireless controller after plugging its receiver into the robot. It maps the joysticks, buttons, arm controls, gripper controls, lighting controls, wake button, and motion-unlock button, then shows how to stop, temporarily restart, or disable controller autostart on Raspberry Pi, Jetson Nano, and Orin mainboards.

## [0.2 Robot Login and Source Code Access](./2.%20Log%20in%20to%20the%20car%20and%20view%20the%20code/README.md)

Shows the recommended first-login workflow: connect to the robot hotspot or Ethernet, read the OLED IP address, log in through VNC or optional SSH, move the robot onto an internet-connected Wi-Fi network, and view the source code. It also documents the factory hotspot, default IP, and default login credentials for Raspberry Pi 5, Jetson Nano, Orin Nano, and Orin NX.

## [0.3 Robotic Arm Calibration](./3.%20Robotic%20Arm%20Calibration/README.md)

Covers both center-position calibration and offset calibration for the six-servo arm. The guide separates Orin Nano/NX steps from Raspberry Pi 5 and Jetson Nano steps, including when to stop the communication agent, how to release and align the servos, how to run the camera/kinematics calibration flow, and how to rebuild the `arm_kin` package after saving offset data.

## [0.4 Docker Container Access for Raspberry Pi 5 and Jetson Nano](./4.%20Enter%20the%20Docker%20%28Jetson-Nano%20and%20Raspberry%20Pi%205%20users,%20see%20here%29/README.md)

Explains why Raspberry Pi 5 and Jetson Nano users run ROS 2 Humble inside the `m3pro` Docker container. It gives the basic container commands for starting the container, entering its terminal, exiting it, and shutting it down when needed.

## [0.6 Control Board Firmware Parameter Configuration](./6.%20Modify%20the%20firmware%20parameters%20of%20the%20car%20control%20board/README.md)

Describes how to edit and write runtime parameters to the car control board after confirming the factory firmware is installed. It covers hardware connection, stopping the micro-ROS agent, editing `config_robot.py`, and configuring values such as ROS domain ID, ROS namespace, motor PID, IMU yaw PID, ROS velocity scaling, and robotic-arm center values.

## [0.7 FAQ and General Precautions](./7.%20Frequently%20Asked%20Questions%20and%20Precautions/README.md)

Reserved for frequently asked questions and general operating precautions.

## [0.8 DIY Robotic Arm Precautions](./8.Precautions%20for%20DIY%20Robotic%20Arm/README.md)

Lists gripper-servo angle recommendations by object size and explains why the correct angle matters. Use this before gripping tasks so servo No. 6 does not stall or burn out when the block size in the scene does not match the program's expected object size.
