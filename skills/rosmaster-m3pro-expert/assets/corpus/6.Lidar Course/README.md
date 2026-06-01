# LiDAR Course

This section covers the ROSMASTER-M3PRO LiDAR stack, from raw scan topics to SLAM, Navigation2, app-based mapping, and object transport workflows. It starts with the dual-LiDAR hardware and scan fusion, then builds through obstacle avoidance, tracking, guard behavior, map creation, localization, navigation, and integrated transport tasks.

Use this section when you need to understand the robot's 2D LiDAR data path, create maps, tune navigation workflows, compare mapping backends, or run LiDAR-assisted tasks that combine navigation with camera recognition and robotic-arm handling.

## [6.1 LiDAR Introduction and Usage](./1.Lidar%20introduction%20and%20use/README.md)

Introduces the T-mini Plus 360-degree 2D LiDAR used on the robot, including its ToF ranging principle, scan frequency, ranging range, angular resolution, and eye-safe design. The lesson also shows how the low-level control node publishes `/scan0` and `/scan1`, how to inspect LaserScan fields, and how to visualize a LiDAR scan in RViz.

## [6.2 Dual LiDAR Fusion and Filtering](./2.Dual%20Lidar%20fusion/README.md)

Explains why the robot's front and rear LiDAR scans are merged into one scan before SLAM and navigation. It covers `ira_laser_tools` scan merging, the `/scan_multi` fused output, laser filtering to remove robot-body points, the filtered `/scan` topic, and RViz or `rqt_graph` checks for the scan-fusion pipeline.

## [6.3 LiDAR Obstacle Avoidance](./3.Lidar%20obstacle%20avoidance/README.md)

Shows how to run the LiDAR obstacle-avoidance example after starting the LiDAR driver, fusion, and filtering launch file. The program reads `/scan`, checks front-left, front, and front-right sectors, and publishes `/cmd_vel` commands so the robot moves forward when clear and steers away from detected obstacles.

## [6.4 LiDAR Tracking](./4.Lidar%20tracking/README.md)

Demonstrates nearest-object tracking with LiDAR. The program searches the fused scan for the closest object in front of the robot, then uses PID control to keep the object centered and maintain a target distance while publishing chassis velocity commands.

## [6.5 LiDAR Guard](./5.Lidar%20guard/README.md)

Runs the LiDAR guard behavior, where the robot rotates to keep the nearest front object centered and sounds the onboard buzzer when the object is closer than the alarm threshold. The lesson covers the scan processing, angular PID control, `/cmd_vel` output, and `/beep` alarm topic.

## [6.6 Gmapping-SLAM Mapping](./6.Gmapping-SLAM%20mapping/README.md)

Guides map creation with the gmapping SLAM algorithm. It explains gmapping's RBPF particle-filter approach, starts the mapping and RViz display nodes, uses keyboard or gamepad control to drive the robot slowly through the environment, and saves the resulting PGM and YAML map files for later navigation.

## [6.7 Cartographer-SLAM Mapping](./7.Cartographer-SLAM%20mapping/README.md)

Shows how to build maps with Google Cartographer. The lesson covers Cartographer's scan processing, submaps, loop closure, and graph optimization, then walks through starting low-level sensors, running Cartographer mapping, viewing the map in RViz, saving standard map files, and saving PBStream maps for relocalization.

## [6.8 slam_toolbox Mapping](./8.slam_toolbox%20mapping/README.md)

Explains slam_toolbox-based 2D SLAM mapping with LiDAR and IMU data. It covers scan matching, graph optimization, map creation in RViz, slow manual driving with keyboard or gamepad control, saving the PGM/YAML map output, and inspecting the node graph and TF tree.

## [6.9 Navigation2 Single-Point Navigation and Obstacle Avoidance](./9.Navigation2%20single-point%20navigation%20avoid/README.md)

Introduces Navigation2 on a saved map for single-goal navigation. The lesson starts the base bringup and Nav2 stack, loads RViz, sets the robot's initial pose with 2D Pose Estimate, sends a target with 2D Goal Pose, observes path planning and obstacle avoidance, and explains core Nav2 concepts such as AMCL, planners, controllers, costmaps, behavior trees, and recovery behavior.

## [6.10 Navigation2 Multi-Point Navigation and Obstacle Avoidance](./10.Navigation2%20multi-point%20navigation%20avoid/README.md)

Builds on single-point Nav2 by using waypoint mode for multi-point navigation. It covers setting the initial pose, enabling Waypoint/Nav Through Pose Mode, marking multiple target poses in RViz, starting waypoint following, and understanding how waypoint data is published and executed through the FollowWaypoints action server.

## [6.11 Rapid Relocalization and Navigation](./11.Repositioning%20navigation/README.md)

Explains rapid relocalization by replacing Navigation2's default AMCL localization with Cartographer localization while keeping the rest of the Nav2 stack. The lesson requires a saved PBStream map, starts Cartographer localization and Navigation2, shows automatic pose estimation in RViz, and reviews the launch-file changes that disable AMCL.

## [6.12 RTAB-Map Mapping](./12.RTAB-Map%20mapping/README.md)

Shows how to combine the chassis, LiDAR, and depth camera to build a map with RTAB-Map. It introduces appearance-based loop closure, visual feature processing, graph optimization, and memory management, then walks through distributed ROS 2 setup, camera and LiDAR bringup, RTAB-Map launch parameters, keyboard driving, and saving the `rtabmap.db` database.

## [6.13 RTAB-Map Navigation](./13.RTAB-Map%20navigation/README.md)

Uses a saved RTAB-Map database for navigation with RTAB-Map localization and Navigation2 planning. The lesson covers copying the database, starting chassis, LiDAR, and camera bringup, moving the arm to a navigation pose, launching RTAB-Map in localization-only mode, starting Nav2, and sending navigation goals in RViz.

## [6.14 App Mapping and Navigation](./14.APP%20mapping%20navigation/README.md)

Explains how to use the ROS Robot mobile app for mapping and navigation. It covers app installation, same-LAN requirements, starting app-based Gmapping, Cartographer, or slam_toolbox mapping, connecting to the robot video and map interface, saving maps from the phone, starting app-based Navigation2, setting the initial pose, and sending navigation goals from the app.

## [6.15 AprilTag Object Transport](./15.Machine%20code%20handling/README.md)

Combines Navigation2, AprilTag recognition, and 3D robotic-arm gripping to pick up and transport tagged blocks. The workflow starts camera and arm solving, chassis and LiDAR bringup, gripping, AprilTag recognition, Navigation2, RViz, rotation detection, and navigation status detection, then uses keyboard modes and Nav2 goals to search, grasp, transport, and release the tagged object.

## [6.16 Colored Block Transport](./16.Color%20block%20transport/README.md)

Combines Navigation2, color recognition, and 3D robotic-arm gripping for colored block pickup and placement. It covers launching the camera, arm solver, chassis bringup, gripping, color recognition, RViz, and Navigation2, selecting or calibrating target colors, gripping a block, navigating to a target point, placing the block, and returning to the starting position for another cycle.
