# Courses

A complete table of contents for the ROSMASTER-M3PRO course corpus. **Part A** leads with what the robot actually does — driving, navigating, grasping, perceiving, and the embodied-AI brain that ties it together — roughly in the order you'd learn to use the kit. **Part B** is the platform and systems material (OS, ROS 2, Docker, compute boards, control-board firmware, OpenCV basics) you consult as reference when you want to go deeper.

**Part A — Operate the Robot**

- [A1. Setup & First Run](#a1-setup--first-run)
- [A2. Mobility & Navigation](#a2-mobility--navigation)
- [A3. Manipulation — Robotic Arm](#a3-manipulation--robotic-arm)
- [A4. Perception & Vision](#a4-perception--vision)
- [A5. Embodied AI](#a5-embodied-ai)

**Part B — Platform & Foundations** *(reference)*

- [B1. Operating System, ROS 2 & Docker](#b1-operating-system-ros-2--docker)
- [B2. Compute Boards (Main Control)](#b2-compute-boards-main-control)
- [B3. Control-Board Firmware (STM32 / micro-ROS)](#b3-control-board-firmware-stm32--micro-ros)
- [B4. Image-Processing Basics (OpenCV)](#b4-image-processing-basics-opencv)

---

# Part A — Operate the Robot

## A1. Setup & First Run

### 0. Configuration and Operation Guide

- [0.1 Controller Quick Start](./0.Configuration%20and%20Operation%20Guide/1.%20Quick%20start%20handle%20to%20control%20the%20car/README.md)
- [0.2 Robot Login and Source Code Access](./0.Configuration%20and%20Operation%20Guide/2.%20Log%20in%20to%20the%20car%20and%20view%20the%20code/README.md)
- [0.3 Robotic Arm Calibration](./0.Configuration%20and%20Operation%20Guide/3.%20Robotic%20Arm%20Calibration/README.md)
- [0.4 Docker Container Access for Raspberry Pi 5 and Jetson Nano](./0.Configuration%20and%20Operation%20Guide/4.%20Enter%20the%20Docker%20%28Jetson-Nano%20and%20Raspberry%20Pi%205%20users,%20see%20here%29/README.md)
- [0.6 Control Board Firmware Parameter Configuration](./0.Configuration%20and%20Operation%20Guide/6.%20Modify%20the%20firmware%20parameters%20of%20the%20car%20control%20board/README.md)
- [0.7 FAQ and General Precautions](./0.Configuration%20and%20Operation%20Guide/7.%20Frequently%20Asked%20Questions%20and%20Precautions/README.md)
- [0.8 DIY Robotic Arm Precautions](./0.Configuration%20and%20Operation%20Guide/8.Precautions%20for%20DIY%20Robotic%20Arm/README.md)

## A2. Mobility & Navigation

### 5. Chassis Control Course

- [5.1 ROS 2 Chassis Topic Control](./5.Chassis%20Control%20Course/1.ROS%20control/README.md)
- [5.2 PS2 Gamepad Teleoperation](./5.Chassis%20Control%20Course/2.Handle%20control/README.md)
- [5.3 Keyboard Teleoperation](./5.Chassis%20Control%20Course/3.Keyboard%20control/README.md)
- [5.4 Angular Velocity Calibration](./5.Chassis%20Control%20Course/4.Angular%20velocity%20calibration/README.md)
- [5.5 Linear Velocity Calibration](./5.Chassis%20Control%20Course/5.Line%20velocity%20calibration/README.md)
- [5.6 Autonomous Line Following](./5.Chassis%20Control%20Course/6.Line%20patrol%20automatic%20driving/README.md)
- [5.7 LiDAR-Aware Patrol Routes](./5.Chassis%20Control%20Course/7.Patrol/README.md)

### 6. LiDAR Course

- [6.1 LiDAR Introduction and Usage](./6.Lidar%20Course/1.Lidar%20introduction%20and%20use/README.md)
- [6.2 Dual LiDAR Fusion and Filtering](./6.Lidar%20Course/2.Dual%20Lidar%20fusion/README.md)
- [6.3 LiDAR Obstacle Avoidance](./6.Lidar%20Course/3.Lidar%20obstacle%20avoidance/README.md)
- [6.4 LiDAR Tracking](./6.Lidar%20Course/4.Lidar%20tracking/README.md)
- [6.5 LiDAR Guard](./6.Lidar%20Course/5.Lidar%20guard/README.md)
- [6.6 Gmapping-SLAM Mapping](./6.Lidar%20Course/6.Gmapping-SLAM%20mapping/README.md)
- [6.7 Cartographer-SLAM Mapping](./6.Lidar%20Course/7.Cartographer-SLAM%20mapping/README.md)
- [6.8 slam_toolbox Mapping](./6.Lidar%20Course/8.slam_toolbox%20mapping/README.md)
- [6.9 Navigation2 Single-Point Navigation and Obstacle Avoidance](./6.Lidar%20Course/9.Navigation2%20single-point%20navigation%20avoid/README.md)
- [6.10 Navigation2 Multi-Point Navigation and Obstacle Avoidance](./6.Lidar%20Course/10.Navigation2%20multi-point%20navigation%20avoid/README.md)
- [6.11 Rapid Relocalization and Navigation](./6.Lidar%20Course/11.Repositioning%20navigation/README.md)
- [6.12 RTAB-Map Mapping](./6.Lidar%20Course/12.RTAB-Map%20mapping/README.md)
- [6.13 RTAB-Map Navigation](./6.Lidar%20Course/13.RTAB-Map%20navigation/README.md)
- [6.14 App Mapping and Navigation](./6.Lidar%20Course/14.APP%20mapping%20navigation/README.md)
- [6.15 AprilTag Object Transport](./6.Lidar%20Course/15.Machine%20code%20handling/README.md)
- [6.16 Colored Block Transport](./6.Lidar%20Course/16.Color%20block%20transport/README.md)

### 11. Multi-vehicle Course

- [11.1 Multi-Vehicle Chassis Control](./11.Multi-vehicle%20Course/1.Multi-vehicle%20chassis%20control/README.md)
- [11.2 Multi-Vehicle Robotic Arm Control](./11.Multi-vehicle%20Course/2.Multi-vehicle%20robotic%20arm%20control/README.md)
- [11.3 Multi-Vehicle Navigation](./11.Multi-vehicle%20Course/3.Multi-vehicle%20navigation/README.md)
- [11.4 Multi-Vehicle Formation (Platoon)](./11.Multi-vehicle%20Course/4.Multi-vehicle%20formation/README.md)

## A3. Manipulation — Robotic Arm

### 9. Robotic Arm and 3D Space Gripping Course

- [9.1 Robotic Arm Solution](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/1.Robotic%20arm%20solution/README.md)
- [9.2 Robotic Arm + Chassis Linkage Control](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/2.Robotic%20arm%20chassis%20linkage%20control/README.md)
- [9.3 AprilTag ID Sorting](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/3.Machine%20code%20ID%20sorting/README.md)
- [9.4 AprilTag Height-Anomaly Sorting](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/4.Sorting%20height%20abnormality%20machine%20code/README.md)
- [9.5 Tracking and Gripping (AprilTag)](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/5.Tracking%20and%20gripping%20machine%20code/README.md)
- [9.6 Color Block Sorting](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/6.Color%20block%20color%20sorting/README.md)
- [9.7 Color Block Height-Anomaly Sorting](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/7.Sorting%20height%20abnormality%20color%20block/README.md)
- [9.8 Tracking and Gripping Color Blocks](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/8.Tracking%20and%20gripping%20color%20block/README.md)
- [9.9 Wood Block Shape Sorting](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/9.Wood%20block%20shape%20sorting/README.md)
- [9.10 KCF Tracking and Gripping](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/10.KCF%20tracking%20and%20gripping%20objects/README.md)
- [9.11 MediaPipe Gesture ID Sorting (AprilTag)](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/11.Medipipe%20gesture%20ID%20sorting%20machine%20code/README.md)
- [9.12 MediaPipe Gesture Height Sorting (AprilTag)](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/12.Mediapipe%20gesture%20height%20sorting%20machine%20code/README.md)
- [9.13 Desktop Tracking and Gripping (AprilTag)](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/13.Desktop%20tracking%20and%20gripping%20machine%20code/README.md)
- [9.14 3D Tracking (AprilTag)](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/14.3D%20tracking%20machine%20code/README.md)
- [9.15 Line Patrol and Obstacle Removal](./9.Robotic%20Arm%20and%203D%20Space%20Gripping%20Course/15.Line%20patrol%20and%20obstacle%20removal/README.md)

### 10. MoveIt2 Simulation Course

- [10.1 MoveIt2 Configuration](./10.MoveIt2%20Simulation%20Course/1.MovelT2%20configuration/README.md)
- [10.2 MoveIt2 Simulation–Reality Linkage](./10.MoveIt2%20Simulation%20Course/2.MovelT2%20simulation-reality%20linkage/README.md)
- [10.3 Random Movement](./10.MoveIt2%20Simulation%20Course/3.Random%20movement/README.md)
- [10.4 Forward Kinematics Design](./10.MoveIt2%20Simulation%20Course/4.Forward%20kinematics%20design/README.md)
- [10.5 Inverse Kinematics Design](./10.MoveIt2%20Simulation%20Course/5.Inverse%20kinematics%20design/README.md)
- [10.6 Cartesian Path](./10.MoveIt2%20Simulation%20Course/6.Cartesian%20path/README.md)
- [10.7 Trajectory Planning](./10.MoveIt2%20Simulation%20Course/7.Trajectory%20planning/README.md)
- [10.8 Collision Detection](./10.MoveIt2%20Simulation%20Course/8.Collision%20detection/README.md)
- [10.9 Scene Design](./10.MoveIt2%20Simulation%20Course/9.Scene%20design/README.md)

## A4. Perception & Vision

### 7. Depth Camera Course

- [7.1 Orbbec Dabai DCW2 Camera Overview](./7.Depth%20Camera%20Course/1.Dabai_DCW2%20camera%20introduction/README.md)
- [7.2 Depth Pseudocolor Visualization](./7.Depth%20Camera%20Course/2.Depth%20pseudo-color%20image/README.md)
- [7.3 Depth-Based Distance Measurement](./7.Depth%20Camera%20Course/3.Depth%20camera%20distance%20measurement/README.md)
- [7.4 Depth-Based Object Volume Measurement](./7.Depth%20Camera%20Course/4.Wood%20block%20volume%20measurement/README.md)
- [7.5 MediaPipe Gesture Recognition](./7.Depth%20Camera%20Course/5.Mediapipe%20gesture%20recognition/README.md)
- [7.6 Depth-Based Edge Detection](./7.Depth%20Camera%20Course/6.Edge%20detection/README.md)
- [7.7 YOLOv8 Object Detection](./7.Depth%20Camera%20Course/7.YOLOv8%20object%20detection/README.md)
- [7.8 TensorRT Object Tracking](./7.Depth%20Camera%20Course/8.Deep%20learning%20object%20tracking/README.md)

### 8. MediaPipe Visual Course

- [8.1 Hand Detection](./8.Mediapipe%20Visual%20Course/1.Hand%20detection/README.md)
- [8.2 Posture Detection](./8.Mediapipe%20Visual%20Course/2.Posture%20detection/README.md)
- [8.3 Holistic Detection](./8.Mediapipe%20Visual%20Course/3.Overall%20detection/README.md)
- [8.4 Facial Landmark Detection](./8.Mediapipe%20Visual%20Course/4.Facial%20Landmark%20Detection/README.md)
- [8.5 Face Detection](./8.Mediapipe%20Visual%20Course/5.Face%20detection/README.md)
- [8.6 Face Special Effects](./8.Mediapipe%20Visual%20Course/6.Face%20special%20effects/README.md)
- [8.7 3D Object Recognition](./8.Mediapipe%20Visual%20Course/7.3D%20object%20recognition/README.md)
- [8.8 Air-Drawing Brush](./8.Mediapipe%20Visual%20Course/8.Brush/README.md)
- [8.9 Finger Control](./8.Mediapipe%20Visual%20Course/9.Finger%20control/README.md)
- [8.10 Palm Target Positioning](./8.Mediapipe%20Visual%20Course/10.Palm%20target%20positioning/README.md)
- [8.11 Fingertip Trajectory Recognition](./8.Mediapipe%20Visual%20Course/11.Fingertip%20trajectory%20recognition/README.md)
- [8.12 Fingertip Gesture Control of Robotic Arm](./8.Mediapipe%20Visual%20Course/12.Fingertip%20gesture%20control%20robotic%20arm/README.md)
- [8.13 Gesture Grabbing and Releasing Objects](./8.Mediapipe%20Visual%20Course/13.Gesture%20grabbing%20and%20releasing%20objects/README.md)
- [8.14 Finger Control of Robotic Arm](./8.Mediapipe%20Visual%20Course/14.Finger%20control%20robotic%20arm/README.md)
- [8.15 MediaPipe Gesture Control of Arm Action Group](./8.Mediapipe%20Visual%20Course/15.Medipipe%20gesture%20control%20robotic%20arm%20action%20group/README.md)

## A5. Embodied AI

### 1. AI Model Basics

- [1.1 Large Model Types and Core Principles](./1.AI%20Model%20Basics/1.AI%20large%20model%20types%20and%20principles/README.md)
- [1.2 RAG Retrieval and Training Examples](./1.AI%20Model%20Basics/2.RAG%20retrieval%20enhancement%20and%20model%20training%20samples/README.md)
- [1.3 `multi_brains` Embodied AI Architecture](./1.AI%20Model%20Basics/3.Embodied%20intelligent%20robot%20system%20architecture/README.md)
- [1.4 `multi_brains` Core Source Code Walkthrough](./1.AI%20Model%20Basics/4.Embodied%20intelligent%20functions%20core%20source%20code/README.md)

### 2. AI Model Development (Dify and RAG)

- [2.1 Model Provider Accounts and API Keys](./2.AI%20Model%20Development/01.Register%20a%20model%20service%20provider%20account/1.Register%20a%20model%20service%20account/README.md)
- [2.2 Configure Model API Access](./2.AI%20Model%20Development/02.%20Configuring%20API-KEY/2.Configuring%20API-KEY/README.md)
- [2.3 Dify Platform Overview](./2.AI%20Model%20Development/03.%20Introduction%20to%20Dify/3.%20Introduction%20to%20Dify/README.md)
- [2.4 Dify Operations and Model Switching](./2.AI%20Model%20Development/04.%20Basic%20Dify%20Features/Basic%20Dify%20Features/README.md)
- [2.5 Build a Chatbot in Dify](./2.AI%20Model%20Development/05.%20AI%20Large%20Model%20Development%20-%20chatbot/AI%20Large%20Model%20Development%20-%20chatbot/README.md)
- [2.6 Deploy a Local RAG Knowledge Base](./2.AI%20Model%20Development/06.%20Deploy%20the%20RAG%20knowledge%20base/Deploy%20the%20RAG%20knowledge%20base/README.md)
- [2.7 Connect RAG to a Chatbot](./2.AI%20Model%20Development/07.%20RAG%20knowledge%20base%20%2B%20chatbot/RAG%20knowledge%20base%20%2B%20chatbot/README.md)
- [2.8 Build an AI Agent Workflow](./2.AI%20Model%20Development/08.%20AI%20agent%20workflow/AI%20agent%20workflow/README.md)
- [2.9 Customize Wake-Up Responses](./2.AI%20Model%20Development/09.%20Custom%20wake-up%20response/Custom%20wake-up%20response/README.md)
- [2.10 Test Core AI Modules](./2.AI%20Model%20Development/10.%20Core%20module%20testing%20tools/Core%20Module%20Testing%20Tools/README.md)

### 3. AI Model — Text Version

- [3.1 Text Command Understanding and Action Execution](./3.AI%20Model%20-%20Text%20Version/1.Semantic%20understand%20and%20command%20follow/Semantic%20understand%20and%20command%20follow/README.md)
- [3.2 Text-Based Visual Understanding](./3.AI%20Model%20-%20Text%20Version/2.Multimodal%20visual%20understand/Multimodal%20visual%20understand/README.md)
- [3.3 Text-Guided Visual Grasping](./3.AI%20Model%20-%20Text%20Version/3.%20Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/README.md)
- [3.4 Text-Guided Visual Navigation](./3.AI%20Model%20-%20Text%20Version/4.Multimodal%20visual%20understand%2BSLAM%20navigation/Multimodal%20visual%20understand%2BSLAM%20navigation/README.md)
- [3.5 Text-Guided Navigation and Object Transfer](./3.AI%20Model%20-%20Text%20Version/5.Robotic%20arm%20gripping%2BMultimodal%20visual%20understand%2BSLAM%20navigation/README.md)
- [3.6 Text-Based Personal Intent Understanding](./3.AI%20Model%20-%20Text%20Version/6.Intention%20estimation/Intention%20estimation/README.md)

### 4. AI Model — Voice Version

- [4.1 Voice Command Understanding and Action Execution](./4.AI%20Model%20-%20Voice%20Version/1.Semantic%20understand%20and%20command%20follow/Semantic%20understand%20and%20command%20follow/README.md)
- [4.2 Voice-Based Visual Understanding](./4.AI%20Model%20-%20Voice%20Version/2.Multimodal%20visual%20understand/Multimodal%20visual%20understand/README.md)
- [4.3 Voice-Guided Visual Grasping](./4.AI%20Model%20-%20Voice%20Version/3.%20Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/README.md)
- [4.4 Voice-Guided Visual Navigation](./4.AI%20Model%20-%20Voice%20Version/4.Multimodal%20visual%20understand%2BSLAM%20navigation/Multimodal%20visual%20understand%2BSLAM%20navigation/README.md)
- [4.5 Voice-Guided Navigation and Object Transfer](./4.AI%20Model%20-%20Voice%20Version/5.Robotic%20arm%20gripping%2BMultimodal%20visual%20understand%2BSLAM%20navigation/README.md)
- [4.6 Voice-Based Personal Intent Understanding](./4.AI%20Model%20-%20Voice%20Version/6.Intention%20estimation/Intention%20estimation/README.md)

---

# Part B — Platform & Foundations *(reference)*

## B1. Operating System, ROS 2 & Docker

### 14. Linux System Course

- [14.1 Introduction to Linux](./14.Linux%20System%20Course/1.Introduction%20to%20Linux%20system/README.md)
- [14.2 Ubuntu File System](./14.Linux%20System%20Course/2.Ubuntu%20file%20system/README.md)
- [14.3 Ubuntu Common Commands](./14.Linux%20System%20Course/3.Ubuntu%20common%20commands/README.md)
- [14.4 Ubuntu Common Editors](./14.Linux%20System%20Course/4.Ubuntu%20common%20editors/README.md)
- [14.5 Ubuntu Software Operation Commands](./14.Linux%20System%20Course/5.Ubuntu%20software%20operation%20commands/README.md)
- [14.6 Virtual Machine Installation](./14.Linux%20System%20Course/6.Virtual%20machine%20installation/README.md)
- [14.7 SSH Remote Control](./14.Linux%20System%20Course/7.SSH%20remote%20control/README.md)
- [14.8 VNC Remote Control](./14.Linux%20System%20Course/8.VNC%20remote%20control/README.md)
- [14.9 Transfer Files Remotely](./14.Linux%20System%20Course/9.Transfer%20files%20remotely/README.md)
- [14.10 Driver Library and Communication](./14.Linux%20System%20Course/10.Driver%20library%20and%20communication/README.md)
- [14.11 Static IP and Hotspot Mode](./14.Linux%20System%20Course/11.Static%20IP%20and%20hotspot%20mode/README.md)
- [14.12 Bind Device ID](./14.Linux%20System%20Course/12.Bind%20device%20ID/README.md)
- [14.13 Capacity Expansion and Resource Allocation](./14.Linux%20System%20Course/13.Capacity%20expansion%20and%20resource%20allocation/README.md)
- [14.14 Update System Software Sources](./14.Linux%20System%20Course/14.Update%20system%20software%20sources/README.md)
- [14.15 Set Root User Password](./14.Linux%20System%20Course/15.Set%20root%20user%20password/README.md)
- [14.16 Passwordless sudo](./14.Linux%20System%20Course/16.sudo%20free%20password/README.md)
- [14.17 Connect to Wi-Fi Network](./14.Linux%20System%20Course/17.Connect%20to%20WiFi%20network/README.md)
- [14.18 View System Version](./14.Linux%20System%20Course/18.View%20system%20version/README.md)
- [14.19 Customized Service Management](./14.Linux%20System%20Course/19.Customized%20service%20management/README.md)
- [14.20 Back Up System Image](./14.Linux%20System%20Course/20.Back%20up%20system%20image/README.md)

### 15. ROS 2 Basic Course

- [15.1 Introduction to ROS 2](./15.ROS%20Basic%20Course/1.Introduction%20to%20ROS2/README.md)
- [15.2 Installing Humble](./15.ROS%20Basic%20Course/2.ROS2%20install%20Humble/README.md)
- [15.3 ROS 2 Development Environment](./15.ROS%20Basic%20Course/3.ROS2%20development%20environment/README.md)
- [15.4 ROS 2 Workspace](./15.ROS%20Basic%20Course/4.ROS2%20workspace/README.md)
- [15.5 ROS 2 Function Packages](./15.ROS%20Basic%20Course/5.ROS2%20function%20package/README.md)
- [15.6 ROS 2 Nodes](./15.ROS%20Basic%20Course/6.ROS2%20node/README.md)
- [15.7 ROS 2 Topic Communication](./15.ROS%20Basic%20Course/7.ROS2%20topic%20communication/README.md)
- [15.8 ROS 2 Service Communication](./15.ROS%20Basic%20Course/8.ROS2%20service%20communication/README.md)
- [15.9 ROS 2 Action Communication](./15.ROS%20Basic%20Course/9.ROS2%20action%20communication/README.md)
- [15.10 ROS 2 Custom Interface Messages](./15.ROS%20Basic%20Course/10.ROS2%20custom%20interface%20message/README.md)
- [15.11 ROS 2 Parameter Service Case](./15.ROS%20Basic%20Course/11.ROS2%20parameter%20service%20case/README.md)
- [15.12 ROS 2 Meta-Packages](./15.ROS%20Basic%20Course/12.ROS2%20meta-function%20package/README.md)
- [15.13 ROS 2 Distributed Communication](./15.ROS%20Basic%20Course/13.ROS2%20distributed%20communication/README.md)
- [15.14 ROS 2 DDS](./15.ROS%20Basic%20Course/14.ROS2%20DDS/README.md)
- [15.15 ROS 2 Time-Related API](./15.ROS%20Basic%20Course/15.ROS2%20time%20related%20API/README.md)
- [15.16 ROS 2 Common Command Tools](./15.ROS%20Basic%20Course/16.ROS2%20common%20command%20tools/README.md)
- [15.17 Using ROS 2 RViz2](./15.ROS%20Basic%20Course/17.ROS2%20rviz2%20use/README.md)
- [15.18 ROS 2 rqt Toolbox](./15.ROS%20Basic%20Course/18.ROS2%20rqt%20toolbox/README.md)
- [15.19 ROS 2 Launch File Configuration](./15.ROS%20Basic%20Course/19.ROS2%20Launch%20startup%20file%20configuration/README.md)
- [15.20 ROS 2 Recording and Playback (rosbag)](./15.ROS%20Basic%20Course/20.ROS2%20recording%20and%20playback%20tool/README.md)
- [15.21 ROS 2 URDF Model](./15.ROS%20Basic%20Course/21.ROS2%20URDF%20model/README.md)
- [15.22 ROS 2 Gazebo Simulation Platform](./15.ROS%20Basic%20Course/22.ROS2%20Gazebo%20simulation%20platform/README.md)
- [15.23 ROS 2 TF2 Coordinate Transformation](./15.ROS%20Basic%20Course/23.ROS2%20TF2%20coordinate%20transformation/README.md)

### 16. Docker Course

- [16.1 Docker Overview and Installation](./16.Docker%20Course/1.Docker%20overview%20and%20docker%20installation/README.md)
- [16.2 Common Image / Container Commands](./16.Docker%20Course/2.Common%20commands%20for%20docker%20image%20containers/README.md)
- [16.3 Understanding and Publishing Images](./16.Docker%20Course/3.Docker%20images%20deeply%20understand%20and%20publish%20images/README.md)
- [16.4 Hardware Interaction and Data Processing](./16.Docker%20Course/4.Docker%20hardware%20interaction%20and%20data%20processing/README.md)
- [16.5 Enter the Robot's Docker Container](./16.Docker%20Course/5.Enter%20the%20bot%27s%20docker%20container/README.md)
- [16.6 Build a Robot Dev Environment in Docker](./16.Docker%20Course/6.Robot%20development%20environment%20construction%20in%20Docker/README.md)

## B2. Compute Boards (Main Control)

### 13. Main Control Course

#### 13.1 Jetson Nano B01

- [13.1.1 Jetson Nano B01 SUB Board Introduction](./13.Main%20Control%20Course/Jetson%20Nano%20B01/1.%20Introduction%20to%20the%20Jetson%20Nano%20B01%20SUB%20Board/README.md)
- [13.1.2 Burn the System Image (eMMC)](./13.Main%20Control%20Course/Jetson%20Nano%20B01/2.%20Burn%20the%20system%20image/README.md)
- [13.1.3 Re-burn an Already-Burned Card](./13.Main%20Control%20Course/Jetson%20Nano%20B01/3.%20Re-read%20the%20memory%20card%20or%20USB%20drive%20that%20has%20been%20burned/README.md)
- [13.1.4 Startup System](./13.Main%20Control%20Course/Jetson%20Nano%20B01/4.%20Startup%20system/README.md)
- [13.1.5 System and Desktop Introduction](./13.Main%20Control%20Course/Jetson%20Nano%20B01/5.%20Jetson%20Nano%20B01%20System%20and%20Desktop%20Introduction/README.md)
- [13.1.6 Memory Card / USB Drive Expansion](./13.Main%20Control%20Course/Jetson%20Nano%20B01/6.%20Memory%20card%20or%20USB%20flash%20drive%20expansion/README.md)
- [13.1.7 Network Configuration](./13.Main%20Control%20Course/Jetson%20Nano%20B01/7.%20Network%20Configuration/README.md)
- [13.1.8 SSH Remote Login & File Transfer](./13.Main%20Control%20Course/Jetson%20Nano%20B01/8.%20SSH%20remote%20login%20%26%20file%20transfer/README.md)
- [13.1.9 VNC Remote Login](./13.Main%20Control%20Course/Jetson%20Nano%20B01/9.%20VNC%20Remote%20Login/README.md)
- [13.1.10 System Backup](./13.Main%20Control%20Course/Jetson%20Nano%20B01/10.%20Jetson%20Nano%20B01%20system%20backup/README.md)
- [13.1.11 Swap Space Increase](./13.Main%20Control%20Course/Jetson%20Nano%20B01/11.%20Jetson%20Nano%20Swap%20space%20increased/README.md)
- [13.1.12 Installation and Use of Jtop](./13.Main%20Control%20Course/Jetson%20Nano%20B01/12.%20Installation%20and%20use%20of%20Jtop/README.md)

#### 13.2 Jetson Orin Nano / NX

- [13.2.1 Jetson Orin Board Introduction](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/1.Jetson%20Orin%20board%20introduction/README.md)
- [13.2.2 Restore the Factory Image System](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/2.%20Restore%20the%20factory%20image%20system/README.md)
- [13.2.3 Backup SSD System](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/3.Backup%20SSD%20system/README.md)
- [13.2.4 SSD Expansion](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/4.SSD%20expansion/README.md)
- [13.2.5 Network Configuration](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/5.Network%20configuration/README.md)
- [13.2.6 SSH Remote Login](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/6.SSH%20remote%20login/README.md)
- [13.2.7 VNC Remote Control](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/7.VNC%20remote%20control/README.md)
- [13.2.8 Remote File Transfer](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/8.Remote%20file%20transfer/README.md)
- [13.2.9 Jtop Tool](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/9.Jtop%20tool/README.md)
- [13.2.10 Swap Space Expansion](./13.Main%20Control%20Course/Jetson%20Orin%20Nano_NX/10.Exchange%20space%20expansion/README.md)

#### 13.3 Raspberry Pi 5

- [13.3.1 Introduction to Raspberry Pi 5](./13.Main%20Control%20Course/Raspberry%20Pi/1.Introduction%20to%20Raspberry%20PI%205/README.md)
- [13.3.2 System Installation and Backup](./13.Main%20Control%20Course/Raspberry%20Pi/2.%20Raspberry%20PI%20system%20installation%20and%20backup/README.md)
- [13.3.3 Powering the Raspberry Pi 5](./13.Main%20Control%20Course/Raspberry%20Pi/3.Powering%20the%20Raspberry%20PI%205/README.md)
- [13.3.4 Startup](./13.Main%20Control%20Course/Raspberry%20Pi/4.Startup%20of%20Raspberry%20PI%205/README.md)
- [13.3.5 Update and Upgrade the OS](./13.Main%20Control%20Course/Raspberry%20Pi/5.Update%20and%20upgrade%20operating%20system/README.md)
- [13.3.6 raspi-config Tool](./13.Main%20Control%20Course/Raspberry%20Pi/6.Introduction%20to%20raspi-config%20tool/README.md)
- [13.3.7 config.txt File Description](./13.Main%20Control%20Course/Raspberry%20Pi/7.config.txt%20file%20description/README.md)
- [13.3.8 Network Configuration](./13.Main%20Control%20Course/Raspberry%20Pi/8.Network%20Configuration/README.md)
- [13.3.9 Remote Access](./13.Main%20Control%20Course/Raspberry%20Pi/9.remote%20access/README.md)
- [13.3.10 Transfer Files Remotely](./13.Main%20Control%20Course/Raspberry%20Pi/10.Transfer%20files%20remotely/README.md)
- [13.3.11 Set Display Resolution and Rotation](./13.Main%20Control%20Course/Raspberry%20Pi/11.Set%20display%20resolution%20and%20rotation/README.md)
- [13.3.12 Set Screen to Sleep](./13.Main%20Control%20Course/Raspberry%20Pi/12.Set%20screen%20to%20sleep/README.md)
- [13.3.13 Play Audio and Video](./13.Main%20Control%20Course/Raspberry%20Pi/13.Play%20audio%20and%20video/README.md)
- [13.3.14 Using a USB Camera](./13.Main%20Control%20Course/Raspberry%20Pi/14.Using%20USB%20camera/README.md)
- [13.3.15 Using a MIPI Camera](./13.Main%20Control%20Course/Raspberry%20Pi/15.Using%20MIPI%20camera/README.md)
- [13.3.16 Get Real-Time Raspberry Pi Temperature](./13.Main%20Control%20Course/Raspberry%20Pi/16.Get%20real-time%20temperature%20of%20Raspberry%20Pi/README.md)

## B3. Control-Board Firmware (STM32 / micro-ROS)

### 12. Control Board Course

#### 12.1 Development Environment Setup

- [12.1.1 Introduction to the Control Board](./12.Control%20Board%20Course/1.Development%20environment%20setup/1.Introduction%20to%20the%20Control%20Board/README.md)
- [12.1.2 Set Up the STM32CubeIDE Environment](./12.Control%20Board%20Course/1.Development%20environment%20setup/2.Set%20up%20the%20STM32CUBEIDE%20development%20environment/README.md)
- [12.1.3 Burn STM32 Firmware via SWD](./12.Control%20Board%20Course/1.Development%20environment%20setup/3.Burning%20STM32%20firmware%20using%20SWD/README.md)
- [12.1.4 Burn STM32 Firmware via Serial Port](./12.Control%20Board%20Course/1.Development%20environment%20setup/4.Burning%20STM32%20firmware%20using%20serial%20port/README.md)
- [12.1.5 Compile the micro-ROS Driver Library](./12.Control%20Board%20Course/1.Development%20environment%20setup/5.Compile%20the%20microros%20driver%20library/README.md)
- [12.1.6 Install and Start the micro-ROS Agent](./12.Control%20Board%20Course/1.Development%20environment%20setup/6.Install%20and%20start%20the%20microros%20agent/README.md)
- [12.1.7 Import Project](./12.Control%20Board%20Course/1.Development%20environment%20setup/7.Import%20Project/README.md)

#### 12.2 STM32 Basic Routines

- [12.2.1 Light Up the LED](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/1.Turn%20on%20the%20LED%20light/README.md)
- [12.2.2 Button Functions](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/2.Button%20functions/README.md)
- [12.2.3 Drive the Buzzer](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/3.Drive%20the%20buzzer/README.md)
- [12.2.4 Serial Communication](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/4.Serial%20communication/README.md)
- [12.2.5 Battery Voltage Detection](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/5.Battery%20voltage%20detection/README.md)
- [12.2.6 Driving PWM Servos](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/6.Driving%20PWM%20Servo/README.md)
- [12.2.7 Drive Motor](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/7.Drive%20motor/README.md)
- [12.2.8 Read Motor Encoder Data](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/8.Read%20motor%20encoder%20data/README.md)
- [12.2.9 PID Motor Speed Control](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/9.PID%20control%20of%20motor%20speed/README.md)
- [12.2.10 Robot Kinematics Analysis Theory](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/10.Robot%20kinematics%20analysis%20theory/README.md)
- [12.2.11 Read IMU Data](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/11.Read%20IMU%20data/README.md)
- [12.2.12 Read LiDAR Data](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/12.Read%20Lidar%20data/README.md)
- [12.2.13 Flash Data Access](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/13.Flash%20access%20data/README.md)
- [12.2.14 Driving OLED Displays](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/14.Driving%20OLED%20Displays/README.md)
- [12.2.15 Driving RGB Light Strips](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/15.Driving%20RGB%20light%20strip/README.md)
- [12.2.16 SBUS Model Aircraft Remote Control](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/16.SBUS%20model%20aircraft%20remote%20control/README.md)
- [12.2.17 USB Controller Remote Control](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/17.USB%20controller%20remote%20control/README.md)
- [12.2.18 CAN Bus Communication](./12.Control%20Board%20Course/2.Control%20board%20STM32%20basic%20routine/18.CAN%20bus%20communication/README.md)

#### 12.3 micro-ROS Basic Routines

- [12.3.1 Publish a Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/1.Post%20a%20topic/README.md)
- [12.3.2 Subscribe to a Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/2.Subscribe%20to%20a%20topic/README.md)
- [12.3.3 Multi-Topic Subscription and Publishing](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/3.Multi-topic%20subscription%20and%20publishing/README.md)
- [12.3.4 Subscribe to the Buzzer Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/4.Subscribe%20to%20the%20buzzer%20topic/README.md)
- [12.3.5 Subscribe to the Bus Servo Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/5.Subscribe%20to%20the%20bus%20servo%20topic/README.md)
- [12.3.6 Subscribe to the Speed Control Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/6.Subscribe%20to%20the%20rate%20control%20topic/README.md)
- [12.3.7 Publish Speed Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/7.Release%20Speed%20Topic/README.md)
- [12.3.8 Publish IMU Data Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/8.Publish%20IMU%20data%20topic/README.md)
- [12.3.9 Publish LiDAR Data Topic](./12.Control%20Board%20Course/3.Control%20board%20micro_ros%20basic%20routine/9.Publish%20radar%20data%20topic/README.md)

## B4. Image-Processing Basics (OpenCV)

### 17. Image Processing Basics Course

- [17.1 Introduction to OpenCV](./17.Image%20Processing%20Basics%20Course/1.%20Introduction%20to%20Open%20Source%20CV/README.md)
- [17.2 Image Reading and Display](./17.Image%20Processing%20Basics%20Course/2.%20Image%20reading%20and%20display/README.md)
- [17.3 Image Writing](./17.Image%20Processing%20Basics%20Course/3.%20Image%20writing/README.md)
- [17.4 Image Quality](./17.Image%20Processing%20Basics%20Course/4.%20Image%20quality/README.md)
- [17.5 Pixel Operations](./17.Image%20Processing%20Basics%20Course/5.%20Pixel%20Operation/README.md)
- [17.6 Image Zoom](./17.Image%20Processing%20Basics%20Course/6.%20Image%20zoom/README.md)
- [17.7 Image Cropping](./17.Image%20Processing%20Basics%20Course/7.%20Image%20cutting/README.md)
- [17.8 Image Translation](./17.Image%20Processing%20Basics%20Course/8.%20Image%20translation/README.md)
- [17.9 Image Mirroring](./17.Image%20Processing%20Basics%20Course/9.%20Image%20Mirroring/README.md)
- [17.10 Affine Transformation](./17.Image%20Processing%20Basics%20Course/10.%20Affine%20Transformation/README.md)
- [17.11 Image Rotation](./17.Image%20Processing%20Basics%20Course/11.%20Image%20Rotation/README.md)
- [17.12 Perspective Transformation](./17.Image%20Processing%20Basics%20Course/12.%20Perspective%20Transformation/README.md)
- [17.13 Grayscale Processing](./17.Image%20Processing%20Basics%20Course/13.%20Grayscale%20processing/README.md)
- [17.14 Image Binarization](./17.Image%20Processing%20Basics%20Course/14.%20Image%20Binarization/README.md)
- [17.15 Edge Detection](./17.Image%20Processing%20Basics%20Course/15.%20Edge%20Detection/README.md)
- [17.16 Line Drawing](./17.Image%20Processing%20Basics%20Course/16.%20Line%20drawing/README.md)
- [17.17 Rectangle and Circle Drawing](./17.Image%20Processing%20Basics%20Course/17.%20Rectangle%20and%20circle%20drawing/README.md)
- [17.18 Text and Picture Drawing](./17.Image%20Processing%20Basics%20Course/18.%20Drawing%20text%20and%20pictures/README.md)

---
