# ROSMASTER-M3PRO Course Corpus

This index links to the section README for each course chapter. Use it as the corpus map: start with setup, then move through embodied AI, robot operation, hardware, and software foundations.

## Setup

- [0. Configuration and Operation Guide](./0.Configuration%20and%20Operation%20Guide/README.md) - First-run setup for controller operation, robot login, arm calibration, Docker access, firmware parameters, FAQs, and DIY arm precautions.

## Part A - Embodied AI

- [1. AI Model Basics](./1.AI%20Model%20Basics/README.md) - Introduces large-model concepts, RAG workflows, the `multi_brains` architecture, and the core embodied-AI source code.
- [2. AI Model Development](./2.AI%20Model%20Development/README.md) - Walks through model-provider accounts, API keys, Dify, chatbot workflows, local RAG deployment, agents, wake-up responses, and module testing.
- [3. AI Model - Text Version](./3.AI%20Model%20-%20Text%20Version/README.md) - Demonstrates text-command workflows for robot actions, visual understanding, grasping, navigation, object transfer, and intent understanding.
- [4. AI Model - Voice Version](./4.AI%20Model%20-%20Voice%20Version/README.md) - Covers the same embodied-AI behaviors as the text course, but driven through voice interaction.

## Part B - Operate the Robot

- [5. Chassis Control Course](./5.Chassis%20Control%20Course/README.md) - Covers ROS 2 chassis commands, controller and keyboard teleoperation, velocity calibration, line following, and patrol behavior.
- [6. LiDAR Course](./6.Lidar%20Course/README.md) - Builds from LiDAR usage and filtering to obstacle behaviors, SLAM mapping, Navigation2, RTAB-Map, app navigation, and object transport.
- [7. Depth Camera Course](./7.Depth%20Camera%20Course/README.md) - Introduces the depth camera stack for depth visualization, measurement, volume estimation, gesture recognition, edge detection, YOLOv8, and tracking.
- [8. MediaPipe Visual Course](./8.Mediapipe%20Visual%20Course/README.md) - Covers camera-based interaction with hands, posture, face landmarks, effects, object recognition, drawing, fingertip tracking, and robotic-arm gestures.
- [9. Robotic Arm and 3D Space Gripping Course](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/README.md) - Focuses on arm and chassis coordination, AprilTag and color-block sorting, tracking, 3D grasping, gesture control, and obstacle removal.
- [10. MoveIt2 Simulation Course](./10.MoveIt2%20Simulation%20Course/README.md) - Explains MoveIt2 configuration, simulation-to-robot linkage, random motion, kinematics, Cartesian paths, planning, collision detection, and scene design.
- [11. Multi-Vehicle Course](./11.Multi-vehicle%20Course/README.md) - Covers coordinated chassis, arm, navigation, and formation workflows for multiple ROSMASTER robots.

## Part C - Hardware

- [12. Control Board Course](./12.Control%20Board%20Course/README.md) - Documents STM32 and micro-ROS development, including firmware setup, board peripherals, sensors, actuators, and ROS topic publishing/subscription.
- [13. Main Control Course](./13.Main%20Control%20Course/README.md) - Provides compute-board setup references for Jetson Nano B01, Jetson Orin Nano/NX, and Raspberry Pi 5 systems.

## Part D - Software and Foundations

- [14. Linux System Course](./14.Linux%20System%20Course/README.md) - Reference material for Linux basics, Ubuntu tools, remote access, drivers, networking, storage, services, and system backup.
- [15. ROS 2 Basic Course](./15.ROS%20Basic%20Course/README.md) - Reference material for ROS 2 Humble, workspaces, packages, nodes, topics, services, actions, interfaces, launch, rosbag, URDF, Gazebo, and TF2.
- [16. Docker Course](./16.Docker%20Course/README.md) - Covers Docker concepts, installation, image and container commands, image publishing, hardware interaction, robot containers, and Docker-based development.
- [17. Image Processing Basics Course](./17.Image%20Processing%20Basics%20Course/README.md) - Introduces OpenCV image I/O, quality, pixel operations, geometric transforms, grayscale and binary processing, edge detection, and drawing.
