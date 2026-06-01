# Robotic Arm and 3D Space Gripping Course

This section covers robotic-arm kinematics, camera-guided object localization, depth-assisted grasping, AprilTag-based sorting, color-block sorting, KCF tracking, gesture-triggered sorting, and line patrol with obstacle removal. The lessons combine the arm solver, chassis motion, camera/depth topics, and gripper control so the robot can identify targets, adjust its position, grasp objects, and place them at predefined locations.

Use this section when you need to understand how visual targets, depth measurements, chassis alignment, and robotic-arm actions are coordinated for 3D grasping tasks.

## [9.1 Robotic Arm Solution](./1.Robotic%20arm%20solution/README.md)

Introduces forward and inverse kinematics for the robotic arm. The lesson shows how to start the kinematics service, inspect its ROS 2 interface, call the forward-kinematics and inverse-kinematics services, and compare the calculated end-effector pose with the URDF visualization.

## [9.2 Robotic Arm + Chassis Linkage Control](./2.Robotic%20arm%20chassis%20linkage%20control/README.md)

Demonstrates coordinated motion between the chassis and robotic arm. The robot drives forward or backward while the arm moves in the opposite direction, using kinematics services and separate control threads to keep the motion synchronized.

## [9.3 AprilTag ID Sorting](./3.Machine%20code%20ID%20sorting/README.md)

Uses AprilTag IDs on machine-code blocks to select the placement target. The program detects tags from camera and depth data, aligns the robot to the required grasping distance, lowers the gripper, and places each block according to its ID.

## [9.4 AprilTag Height-Anomaly Sorting](./4.Sorting%20height%20abnormality%20machine%20code/README.md)

Detects AprilTag blocks, estimates their height, and removes blocks higher than 4 cm. The lesson explains how the robot identifies height anomalies, adjusts distance when needed, grasps the target block, and places it at the configured location.

## [9.5 Tracking and Gripping AprilTag Blocks](./5.Tracking%20and%20gripping%20machine%20code/README.md)

Tracks a handheld AprilTag block and keeps it centered in the camera image. When tracking stops, the robot checks the distance to the target, moves the chassis if necessary, then grasps and places the block.

## [9.6 Color Block Sorting](./6.Color%20block%20color%20sorting/README.md)

Sorts color blocks by keyboard-selected color. The lesson covers color selection, HSV calibration, binary mask display, distance checks, and gripper control for placing the selected block at the target position.

## [9.7 Color Block Height-Anomaly Sorting](./7.Sorting%20height%20abnormality%20color%20block/README.md)

Extends color-block sorting by selecting blocks of a target color whose height exceeds 4 cm. The program combines color recognition, depth-based height filtering, chassis alignment, and robotic-arm placement.

## [9.8 Tracking and Gripping Color Blocks](./8.Tracking%20and%20gripping%20color%20block/README.md)

Tracks a selected color block as it moves through the camera image. The robot follows the block with the arm, checks whether the target is within the required distance, moves forward if needed, and then grasps and places the block.

## [9.9 Wood Block Shape Sorting](./9.Wood%20block%20shape%20sorting/README.md)

Sorts wooden blocks by target shape. The user enters `Rectangle`, `Square`, or `Cylinder`, and the program identifies matching blocks, aligns the robot to the grasping range, and places the selected shape at the configured location.

## [9.10 KCF Tracking and Gripping](./10.KCF%20tracking%20and%20gripping%20objects/README.md)

Uses a KCF tracker to follow a user-selected object. The lesson explains object selection with the mouse, depth-based distance measurement, tracker reset/stop topics, chassis adjustment, and final grasping control.

## [9.11 MediaPipe Gesture ID Sorting (AprilTag)](./11.Medipipe%20gesture%20ID%20sorting%20machine%20code/README.md)

Maps MediaPipe finger-count gestures to AprilTag IDs. After recognizing a gesture from 1 to 4, the robot searches for the matching tag, adjusts to the correct grasping distance, and places the selected block.

## [9.12 MediaPipe Gesture Height Sorting (AprilTag)](./12.Mediapipe%20gesture%20height%20sorting%20machine%20code/README.md)

Uses MediaPipe gestures to choose a height threshold for AprilTag block sorting. The robot recognizes a finger-count gesture, searches for a block above the derived height threshold, and sorts it if found.

## [9.13 Desktop Tracking and Gripping (AprilTag)](./13.Desktop%20tracking%20and%20gripping%20machine%20code/README.md)

Tracks an AprilTag block moving on the desktop with coordinated chassis and arm motion. The user can switch between tracking mode and grasping mode to either follow the block or pick it up and place it.

## [9.14 3D Tracking (AprilTag)](./14.3D%20tracking%20machine%20code/README.md)

Tracks AprilTag movement in 3D space. The program estimates target movement in left-right, up-down, and forward-backward directions and moves the robotic arm to follow the block.

## [9.15 Line Patrol and Obstacle Removal](./15.Line%20patrol%20and%20obstacle%20removal/README.md)

Combines line following, LiDAR obstacle detection, AprilTag recognition, and robotic-arm removal. The robot follows a colored line, stops for obstacles, removes detected machine-code blocks from the path, and then resumes patrol.
