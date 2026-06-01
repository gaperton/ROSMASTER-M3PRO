# Chassis Control Course

This section teaches the core ways to control and tune the ROSMASTER-M3PRO chassis. It covers direct ROS 2 topic control, PS2 controller teleoperation, keyboard teleoperation, angular and linear velocity calibration, autonomous line patrol, and LiDAR-aware patrol routes.

Use this section when you need to verify low-level robot motion, understand the chassis topics and sensor feedback, calibrate odometry behavior, or build confidence with manual and semi-autonomous movement before navigation and AI tasks.

## [5.1 ROS 2 Chassis Topic Control](./1.ROS%20control/README.md)

Introduces direct robot control through ROS 2 topics. The lesson shows how to start the low-level agent, inspect `/YB_Node`, publish `/cmd_vel` motion commands, control the buzzer, light strip, and robotic arm topics, and subscribe to low-level data such as LiDAR scans, battery voltage, raw IMU data, and raw odometry.

## [5.2 PS2 Gamepad Teleoperation](./2.Handle%20control/README.md)

Shows how to control the chassis and robotic arm with the wireless PS2 controller. It covers checking the controller receiver device, testing joystick and button input with `jstest`, launching the controller receiver and robot control nodes, mapping controller inputs to chassis and arm actions, and understanding how `/joy` input is converted into `/cmd_vel` and `/arm_joint` commands.

## [5.3 Keyboard Teleoperation](./3.Keyboard%20control/README.md)

Explains keyboard-based chassis control through the `yahboom_keyboard` node. It lists direction and speed-control keys, shows how keyboard input publishes `geometry_msgs/msg/Twist` messages on `/cmd_vel`, and walks through the node graph, message type, movement dictionaries, and speed dictionaries used by the teleoperation program.

## [5.4 Angular Velocity Calibration](./4.Angular%20velocity%20calibration/README.md)

Guides angular velocity calibration using the `calibrate_angular` node and `rqt_reconfigure`. The lesson explains the test angle, speed, tolerance, angular scale correction, TF-based rotation measurement between `odom` and `base_footprint`, and how to write the final `set_ros_scale_angluar` parameter to the control board through `config_robot.py`.

## [5.5 Linear Velocity Calibration](./5.Line%20velocity%20calibration/README.md)

Guides linear velocity calibration using the `calibrate_linear` node and `rqt_reconfigure`. It covers setting a measured test distance, tuning `odom_linear_scale_correction`, monitoring TF displacement, repeating the test until the actual distance matches the target, and writing the final `set_ros_scale_line` value to the chassis control board.

## [5.6 Autonomous Line Following](./6.Line%20patrol%20automatic%20driving/README.md)

Shows how to run autonomous line patrol with the depth camera and line-following node. The robot detects a ground marker line, starts following when the spacebar is pressed, pauses and sounds the buzzer when an obstacle is detected, resumes after the obstacle is removed, and stops when the line disappears; the lesson also covers recalibrating the target line color.

## [5.7 LiDAR-Aware Patrol Routes](./7.Patrol/README.md)

Explains the patrol function for predefined movement routes with LiDAR obstacle detection. It covers launching the patrol node, using `rqt_reconfigure` to select route commands such as line, circle, square, or triangle, tuning velocity and obstacle-detection parameters, looping patrol routes, and understanding how TF, fused odometry, LiDAR `/scan1`, and `/cmd_vel` are used to move and stop safely.
