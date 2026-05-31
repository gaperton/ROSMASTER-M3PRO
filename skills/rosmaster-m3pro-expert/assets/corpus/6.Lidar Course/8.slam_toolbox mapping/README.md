# slam_toolbox Mapping

## 1. Course Content

Learn how to use slam_toolbox for robot SLAM mapping. After starting the sample program, drive the robot with the keyboard or gamepad to scan the environment, build a map, and save the result.

## 2. Introduction to slam_toolbox

slam_toolbox is an open-source ROS package for 2D SLAM and localization with mobile robots. It uses graph optimization to combine 2D LiDAR and IMU data, build a 2D occupancy grid map, and update the robot pose in real time.

### 2.1 Core Technology Principles

#### 2.1.1 Front-end Processing (Laser Scan Matching)

- **GICP Algorithm**: Estimates the robot's relative pose by iteratively matching the current laser scan against the map. Compared with traditional ICP, GICP uses a probabilistic model and is more robust to outliers.
- **Motion Compensation**: Uses IMU data to reduce laser scan distortion caused by robot motion, improving matching accuracy in dynamic environments.

#### 2.1.2 Backend Optimization (Graph Optimization)

- **Pose Graph Construction**: Builds a graph from robot pose nodes and relative pose constraints obtained through scan matching.
- **Global Optimization**: Uses nonlinear optimization, such as Ceres Solver, to optimize the pose graph, reduce accumulated error, and keep the map globally consistent.

![Figure: page 0: figure 13](_page_0_Figure_13.jpeg)

GitHub project: [https://github.com/SteveMacenski/slam\\_toolbox](https://github.com/SteveMacenski/slam_toolbox)

## 3. Preparation

### 3.1 Content Description

This lesson uses the Jetson Orin NX as an example. On Raspberry Pi and Jetson Nano boards, open a terminal and enter the Docker container before running the commands in this lesson. For Docker entry steps, refer to **[Configuration and Operation Guide]--[Entering the Docker (Jetson Nano and Raspberry Pi 5 users, see here)]**. On Orin and NX boards, run the commands directly in a terminal.

### 3.2 Starting the Agent

Note: To test all cases, you must first start the agent. If it has already been started, you do not need to restart it.

Run the following command in the robot terminal:

```
sh start_agent.sh
```

The terminal prints a success message when the connection is established.

![Picture: page 1: picture 7](_page_1_Picture_7.jpeg)

## 4. Running the Example

### 4.1 Map Creation Process

#### Note:

- **Move slowly while mapping, especially during rotation. Fast motion usually produces poor map quality.**
- For the Jetson Nano and Raspberry Pi series controllers, you must first enter the Docker container (for steps, see the [Docker course chapter - Entering the Robot's Docker Container]).

Start mapping from the robot terminal:

```bash
ros2 launch slam_mapping slam_toolbox.launch.py
```

For example, on the virtual machine, open a terminal and start RViz:

```bash
ros2 launch slam_view slam_view.launch.py
```

To start RViz on the robot, run:

```bash
ros2 launch slam_mapping slam_view.launch.py
```

![Figure: page 2: figure 3](_page_2_Figure_3.jpeg)

Open another terminal in the virtual machine and start keyboard control. You can also use a gamepad if the gamepad control node has already been started; see [5. Chassis Control - 2. Controller Control].

```bash
ros2 run yahboomcar_ctrl yahboom_keyboard
```

Click in the terminal window and press z to reduce the speed. Press I, <, J, and L to move the robot forward, backward, left, and right. Drive slowly until the map is complete.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

### 4.2 Saving the Map

Open a new terminal on the robot and save the map:

```bash
ros2 launch slam_mapping save_map.launch.py
```

The terminal prompt **"Map saved successful"** indicates that the map was saved successfully.

The map is saved to:

Jetson Orin Nano and Jetson Orin NX:

```text
/home/jetson/M3Pro_ws/install/M3Pro_navigation/share/M3Pro_navigation/map
```

Jetson Nano and Raspberry Pi:

Enter Docker first, then use:

```text
/root/M3Pro_ws/install/M3Pro_navigation/share/M3Pro_navigation/map/
```

The saved output includes a PGM image and the yahboom_map.yaml YAML file.

```
image: yahboom_map.pgm
mode: trinary
resolution: 0.05
origin: [-10, -10, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

#### Parameter Explanation

- image: The path to the map file, either absolute or relative.
- mode: This attribute can be one of trinary, scale, or raw, depending on the selected mode. Trinary is the default.
- resolution: The map resolution, in meters/pixels.
- origin: The 2D pose (x, y, yaw) of the lower-left corner of the map. yaw is rotated counterclockwise (yaw=0 means no rotation). Currently, many parts of the system ignore the yaw value.
- negate: Whether to invert the meaning of white/black and free/occupied (this does not affect the interpretation of the thresholds).
- occupied_thresh: Pixels with an occupied probability greater than this threshold are considered fully occupied.
- free_thresh: Pixels with an occupied probability less than this threshold are considered completely free.

## 5. Node Analysis

### 5.1 Displaying the Node Computation Graph

```bash
ros2 run rqt_graph rqt_graph
```

![Figure: page 4: figure 15](_page_4_Figure_15.jpeg)

### 5.2 TF Transformation

Run in the VM terminal:

```bash
ros2 run rqt_tf_tree rqt_tf_tree
```

Image size is too large; the original image can be viewed in this lesson folder.

![Figure: page 5: figure 4](_page_5_Figure_4.jpeg)

### 5.3 slam-toolbox Node Details

```bash
ros2 node info /slam_toolbox
```

Run this command to view the topics and services used by the slam_toolbox node.

```
/slam_toolbox
  Subscribers:
    /map: nav_msgs/msg/OccupancyGrid
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /scan: sensor_msgs/msg/LaserScan
    /slam_toolbox/feedback: visualization_msgs/msg/InteractiveMarkerFeedback
  Publishers:
    /map: nav_msgs/msg/OccupancyGrid
    /map_metadata: nav_msgs/msg/MapMetaData
    /parameter_events: rcl_interfaces/msg/ParameterEvent
    /pose: geometry_msgs/msg/PoseWithCovarianceStamped
    /rosout: rcl_interfaces/msg/Log
    /slam_toolbox/graph_visualization: visualization_msgs/msg/MarkerArray
    /slam_toolbox/scan_visualization: sensor_msgs/msg/LaserScan
    /slam_toolbox/update: visualization_msgs/msg/InteractiveMarkerUpdate
    /tf: tf2_msgs/msg/TFMessage
  Service Servers:
    /slam_toolbox/clear_changes: slam_toolbox/srv/Clear
    /slam_toolbox/describe_parameters: rcl_interfaces/srv/DescribeParameters
    /slam_toolbox/deserialize_map: slam_toolbox/srv/DeserializePoseGraph
    /slam_toolbox/dynamic_map: nav_msgs/srv/GetMap
```

```
/slam_toolbox/get_interactive_markers:
visualization_msgs/srv/GetInteractiveMarkers
    /slam_toolbox/get_parameter_types: rcl_interfaces/srv/GetParameterTypes
    /slam_toolbox/get_parameters: rcl_interfaces/srv/GetParameters
    /slam_toolbox/list_parameters: rcl_interfaces/srv/ListParameters
    /slam_toolbox/manual_loop_closure: slam_toolbox/srv/LoopClosure
    /slam_toolbox/pause_new_measurements: slam_toolbox/srv/Pause
    /slam_toolbox/save_map: slam_toolbox/srv/SaveMap
    /slam_toolbox/serialize_map: slam_toolbox/srv/SerializePoseGraph
    /slam_toolbox/set_parameters: rcl_interfaces/srv/SetParameters
    /slam_toolbox/set_parameters_atomically:
rcl_interfaces/srv/SetParametersAtomically
    /slam_toolbox/toggle_interactive_mode: slam_toolbox/srv/ToggleInteractive
  Service Clients:
  Action Servers:
  Action Clients:
```
