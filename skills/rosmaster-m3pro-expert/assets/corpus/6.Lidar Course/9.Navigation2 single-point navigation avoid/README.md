# Navigation2 Single-Point Navigation and Obstacle Avoidance

## 1. Course Content

- Learn how to use Navigation2 for single-point navigation and obstacle avoidance.
- Load a saved map in RViz, set the robot's initial pose with [2D Pose Estimate], and set a navigation target with [2D Goal Pose].
- Observe how the robot plans a path, avoids obstacles, and stops after reaching the goal.
- Learn the basic concepts behind global costmaps, local costmaps, navigation parameters, and AMCL localization.

## 2. Introduction to Navigation2

### 2.1 Introduction

Navigation2 overall architecture:

![Figure: page 0: figure 8](_page_0_Figure_8.jpeg)

Navigation2 provides the following major components:

- **Map Server**: Loads, serves, and saves maps.
- **AMCL**: Localizes the robot on a known map.
- **Nav2 Planner**: Plans a path from the current pose to the goal while avoiding obstacles.
- **Nav2 Controller**: Generates control commands for following the planned path.
- **Nav2 Costmap 2D**: Converts sensor data into costmaps used for planning and control.
- **Behavior Trees and BT Navigator**: Coordinate navigation behavior through behavior trees.
- **Nav2 Recoveries**: Runs recovery behaviors when navigation fails.
- **Nav2 Waypoint Follower**: Follows a sequence of waypoints.
- **Nav2 Lifecycle Manager**: Manages server lifecycle state.
- **Nav2 Core**: Provides plugin interfaces for custom planners, controllers, and behaviors.

Navigation2 (Nav2) is the standard ROS 2 navigation framework. Its job is to move a mobile robot safely from one pose to another by combining localization, global planning, local control, obstacle avoidance, and recovery behavior.

Nav2 uses behavior trees (BTs) to coordinate modular servers. A navigation task may call actions for path planning, control, recovery, or other navigation behavior. These modules run as independent nodes and communicate with the behavior tree through action servers.

### 2.2 Related Materials

Navigation2 Documentation:<https://navigation.ros.org/index.html>

Navigation2 GitHub:<https://github.com/ros-planning/navigation2>

Navigation2 Paper:<https://arxiv.org/pdf/2003.00368.pdf>

## 3. Preparation

### 3.1 Content Description

This lesson uses the Jetson Orin NX as an example. On Raspberry Pi and Jetson Nano boards, open a terminal and enter the Docker container before running the commands in this lesson. For Docker entry steps, refer to **[Configuration and Operation Guide]--[Entering the Docker (Jetson Nano and Raspberry Pi 5 users, see here)]**. On Orin and NX boards, run the commands directly in a terminal.

### 3.2 Starting the Agent

Note: The agent must be started before testing all examples. If it's already started, you don't need to restart it.

Enter the following command in the robot terminal:

```
sh start_agent.sh
```

The terminal prints a success message when the connection is established.

## 4. Running the Example

### 4.1 Single-Point Navigation

#### Note:

- For Jetson Nano and Raspberry Pi series controllers, you must first enter the Docker container (see the [Docker Course Section - Entering the Robot's Docker Container] for steps).
- This section requires at least one existing map. Refer to any of the SLAM mapping courses, such as Gmapping-SLAM Mapping, Cartographer Mapping, or slam_toolbox Mapping.

Start the low-level sensors from the robot terminal:

```bash
ros2 launch M3Pro_navigation base_bringup.launch.py
```

Start Navigation2:

```bash
ros2 launch M3Pro_navigation navigation2.launch.py
```

RViz can be started on either the robot or the virtual machine. **Choose one method only**; do not start RViz in both places at the same time.

For example, on the virtual machine, open a terminal and start RViz:

```bash
ros2 launch slam_view nav_rviz.launch.py
```

To start RViz on the robot, run:

```bash
ros2 launch M3Pro_navigation nav_rviz.launch.py
```

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

After the map loads, click [2D Pose Estimate] to set the robot's initial pose. Based on the robot's actual position in the environment, click and drag in RViz until the robot model matches the real robot pose. If the LiDAR scan roughly overlaps the actual obstacles, the pose estimate is accurate.

![Figure: page 3: figure 2](_page_3_Figure_2.jpeg)

After pose initialization is complete, the robot model and the red LiDAR 2D point cloud will appear in the RViz interface.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

For single-point navigation, click [2D Goal Pose], then click and drag in RViz to set the target position and orientation.

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

The robot plans a path through the known map and moves toward the target while avoiding obstacles.

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

When the robot reaches the target point, the robot terminal displays "Goal succeeded."

![Figure: page 5: figure 2](_page_5_Figure_2.jpeg)

### 4.2 Viewing the Costmap

To view the global costmap, find Global Costmap under the Global Planner group in the left configuration panel and enable it. To view the local costmap, find Local Costmap under the Controller group and enable its Costmap display. Costmaps are explained in the theory section below.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

### 4.3 Viewing the Node Communication Graph

In the VM terminal, enter:

```bash
ros2 run rqt_graph rqt_graph
```

If the graph does not display initially, select [Nodes/Topics (all)] and click the refresh button in the upper left corner. The original graph is too large; you can view it in the current lesson folder.

![Figure: page 6: figure 5](_page_6_Figure_5.jpeg)

### 4.4 Viewing the TF Tree

In the VM terminal, enter:

```bash
ros2 run rqt_tf_tree rqt_tf_tree
```

If the page does not display at first, click the refresh icon in the upper left corner. The original image is large and can be viewed in this course folder.

![Picture: page 7: picture 1](_page_7_Picture_1.jpeg)

## 5. Navigation Explanation

### 5.1 Core Steps of the Navigation Process

#### 5.1.1 Phase 1: System Initialization and Map Loading

- **Map acquisition**: map_server loads a pre-built raster map.
- The map stores static obstacle information and provides the base environment model for navigation.

#### Costmap Initialization

- **Global Costmap**: Based on the static map, used for global path planning.
- **Local Costmap**: Combines real-time LiDAR scan data with the robot footprint for dynamic obstacle avoidance.

#### 5.1.2 Phase 2: Sensor Data Processing and Environmental Perception

#### Sensor Data Access

LiDAR (/scan), IMU (/imu/data), and odometry (/odom) data are input via ROS topics.

#### Costmap Update

- The local costmap updates dynamic obstacles in real time. Each grid cell receives an occupancy probability and a cost based on sensor data; cells closer to obstacles receive higher cost.
- Inflation expands obstacle boundaries so the robot keeps a safe distance.

#### 5.1.3 Phase 3: Path Planning (Global and Local Planning)

#### Global Path Planning

- Inputs: current robot pose, goal pose, and global costmap.
- The Dijkstra planner generates an optimal path as a series of coordinate points from start to goal.

#### Local Path Planning and Tracking

The local planner, DWBLocalPlanner, generates short-term control commands that the robot can execute based on the global path and the local costmap.

#### 5.1.4 Phase 4: Control Execution and Behavior Decision-Making

#### Controller Output

- The controller converts the local path into linear velocity (linear.x) and angular velocity (angular.z), then publishes them on /cmd_vel.
- Velocity smoothing prevents abrupt motion changes and improves stability.

#### Behavior Tree Decision Process

The behavior tree defines the priority and state transition logic for navigation tasks. A typical process is as follows:

- **Check whether the goal is reachable**: If global planning fails, trigger a recovery behavior such as replanning.
- **Perform local obstacle avoidance**: When the local costmap detects an obstacle, temporarily deviate from the global path.
- **Reach the goal**: When the error between the robot pose and target pose is below the threshold, mark the task complete.

#### Recovery Behavior Mechanism

When navigation encounters a problem, such as a blocked path, Nav2 triggers a recovery strategy. Common recovery behaviors include rotating to search for a clear path, backing up, and replanning.

### 5.2 Key Technical Principles

#### 5.2.1 Costmap

- **Probabilistic grid representation**: Each cell stores an occupancy probability from 0 to 1 and is updated from sensor observations such as LiDAR raycasts.
- **Multi-layer cost overlay**: The costmap combines static map obstacles, dynamic obstacles from real-time sensors, and inflated safety margins.

A costmap is a 2D or 3D map created and updated by the robot using sensor information. The following figure provides a brief overview.

![Figure: page 9: figure 0](_page_9_Figure_0.jpeg)

In the figure above, the red area represents obstacles in the costmap, the blue area represents inflation based on the robot's inscribed radius, and the red polygon represents the robot footprint. To avoid collisions, the footprint must not intersect the red area, and the robot center must not enter the blue area. ROS costmaps use grid cells with costs from 0 to 255, representing occupied, free, and unknown space.

The specific states and values are shown in the following figure:

The figure divides cost values into five categories:

- **Lethal**: The robot center would overlap an obstacle cell, so collision is certain.
- **Inscribed**: The cell lies within the robot footprint, so collision is certain.
- **Possibly circumscribed**: The cell is close to the robot outline, so collision depends on the exact robot pose.
- **Freespace**: Known free space.
- **Unknown**: Space that has not been observed.

#### Global Costmap

![Picture: page 10: picture 0](_page_10_Picture_0.jpeg)

#### Local Costmap

![Picture: page 10: picture 2](_page_10_Picture_2.jpeg)

#### 5.2.2 AMCL Localization Algorithm

AMCL (Adaptive Monte Carlo Localization) is a probabilistic localization system for 2D mobile robots. It implements an adaptive (or KLD sampling) Monte Carlo localization method that uses a particle filter to estimate the robot's position based on a given map.

As shown in the figure below, if the odometry is error-free, in a perfect world, we can directly use the odometry information (top half) to infer the robot's (base_frame) position relative to the odometry coordinate system. However, in reality, odometry drift and non-negligible cumulative errors exist. Therefore, AMCL uses the method in the bottom half. This method first uses the odometry information to preliminarily locate the base_frame. Then, using the measurement model, we determine the base_frame's position relative to the map_frame (global map coordinate system), thus determining the robot's position within the map. (Note that although the conversion from base to map is estimated here, the conversion from map to odom is finally published, which can be understood as the drift of the odometry.)

![Figure: page 11: figure 4](_page_11_Figure_4.jpeg)

![Figure: page 11: figure 5](_page_11_Figure_5.jpeg)

In the TF tree during navigation, AMCL publishes the transform between map and odom. The **ekf_filter_node** from the **robot_localization** package publishes the transform between odom and base_footprint after fusing IMU data with raw encoder odometry.

![Figure: page 12: figure 1](_page_12_Figure_1.jpeg)

In the node communication diagram above, we can see the communication data flow for the ekf_filter_node.

The /YB_Node node is the robot chassis node, publishing **/imu/data_raw** (raw IMU sensor data) and **/odom_raw** (raw encoder odometry data).

The imu_filter node subscribes to **/imu/data_raw** from the robot chassis, filters the raw IMU data, and publishes the result to **/imu/data**.

The **ekf_filter_node** node subscribes to the **/odom** and **/imu/data** topics, fuses the multi-sensor data, and publishes it to the **/odom** topic.

![Picture: page 13: picture 0](_page_13_Picture_0.jpeg)

### 5.3 Path Planning

#### 5.3.1 Global Path Planning

Global path planning calculates an optimal or feasible route from the start pose to the goal pose on the known map. It uses the global costmap and does not directly respond to every real-time obstacle. In the figure below, the arrows show the global path.

![Picture: page 13: picture 4](_page_13_Picture_4.jpeg)

#### 5.3.2 Local Path Planning

Local path planning adjusts the robot motion in real time using LiDAR data and the local costmap. It tracks the global path while avoiding nearby obstacles. In the figure below, the blue line is the local path.

![Picture: page 14: picture 0](_page_14_Picture_0.jpeg)

### 5.4 Navigation Parameter Configuration

Configuration file path:

For Jetson Nano and Raspberry Pi, you must first enter Docker:

```
/root/M3Pro_ws/src/M3Pro_navigation/param/yahboom_M3Pro.yaml
```

For Jetson Orin Nano and NX:

```
/home/jetson/M3Pro_ws/src/M3Pro_navigation/param/yahboom_M3Pro.yaml
```

The default configuration parameters for the navigation function are as follows:

```
# AMCL (Adaptive Monte Carlo Localization) configuration
amcl :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # Control the noise parameters of the odometer model when the robot rotates
    alpha1 : 0.2
    # Control the noise parameters of the odometry model when the robot rotates
and translates
    alpha2 : 0.2
    # Control the noise parameters of the odometer model when the robot
translates
    alpha3 : 0.2
    # Control the noise parameters of the odometer model when the robot is
rotated due to translation
    alpha4 : 0.2
    # Control the noise parameters of the odometry model when the robot rotates
(another aspect)
    alpha5 : 0.2
    # The name of the robot's base coordinate system
    base_frame_id : "base_footprint"
```

```
# The distance threshold for beam skipping, used for laser scanning data
processing
    beam_skip_distance : 0.5
    # The error threshold for beam skipping, used to decide whether to skip
certain beams
    beam_skip_error_threshold : 0.9
    # The beam skipping threshold is used to decide whether to skip certain
beams
    beam_skip_threshold : 0.3
    # Whether to enable beam skipping function
    do_beamskip : false
    # Global coordinate system name
    global_frame_id : "map"
    # Attenuation coefficient of short laser reflection
    lambda_short : 0.1
    # Maximum likelihood distance for laser scanning
    laser_likelihood_max_dist : 2.0
    # Maximum range of laser scanning
    laser_max_range : 100.0
    # Minimum range of laser scanning
    laser_min_range : -1.0
    # Laser model type
    laser_model_type : "likelihood_field"
    # Maximum number of laser beams to use per update
    max_beams : 60
    # Maximum number of particles allowed in the particle filter
    max_particles : 2000
    # Minimum number of particles allowed in the particle filter
    min_particles : 500
    # Odometer coordinate system name
    odom_frame_id : "odom"
    # Error threshold of particle filter
    pf_err : 0.05
    # Confidence threshold for particle filter
    pf_z : 0.99
    # Fast recovery factor, used for the recovery mechanism of the particle
filter
    recovery_alpha_fast : 0.0
    # Slow recovery factor, used for the recovery mechanism of the particle
filter
    recovery_alpha_slow : 0.0
    # Resampling interval
    resample_interval : 1
    # The robot's motion model type
    robot_model_type : "nav2_amcl::DifferentialMotionModel"
    # Save the rate of the robot's posture
    save_pose_rate : 0.5
    # Standard deviation of laser hits
    sigma_hit : 0.2
    # Whether to broadcast TF transformation
    tf_broadcast : true
    # TF Transform Release Rate
    tf_publish_rate : 10.0
    # Transformation tolerance time
    transform_tolerance : 0.2
    # Minimum threshold for angle update
    update_min_a : 0.2
    # Minimum threshold for distance update
```

```
update_min_d : 0.25
    # Weight of laser hit
    z_hit : 0.5
    # Weight of the laser's maximum range
    z_max : 0.05
    # Weights of random laser measurements
    z_rand : 0.5
    # Weight of short laser reflections
    z_short : 0.05
    #Topic name for laser scanning data
    scan_topic : scan
# AMCL map client configuration
amcl_map_client :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
# AMCL RCLCPP node configuration
amcl_rclcpp_node :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
# BT Navigator Configuration
bt_navigator :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # Global coordinate system name
    global_frame : map
    # The name of the robot's base coordinate system
    robot_base_frame : base_link
    # Topic name for odometer data
    odom_topic : /odom
    # Default behavior tree XML file name
    default_bt_xml_filename : "navigate_w_replanning_and_recovery.xml"
    # Behavior Tree Loop
    bt_loop_duration : 10
    #Default server timeout
    default_server_timeout : 20
    # Whether to enable Groot monitoring
    enable_groot_monitoring : True
    # Groot's ZMQ publisher port
    groot_zmq_publisher_port : 1666
    # Groot's ZMQ server port
    groot_zmq_server_port : 1667
    # List of behavior tree plugin library names
    plugin_lib_names :
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
```

```
- nav2_goal_updated_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
# BT Navigator RCLCPP node configuration
bt_navigator_rclcpp_node :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
# Controller Server Configuration
controller_server :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # The controller's operating frequency
    controller_frequency : 5.0
    # Minimum speed threshold in the X direction
    min_x_velocity_threshold : 0.001
    # Minimum speed threshold in the Y direction
    min_y_velocity_threshold : 0.5
    # Minimum speed threshold for rotation direction
    min_theta_velocity_threshold : 0.001
    # Maximum failure tolerance allowed
    failure_tolerance : 0.3
    # Progress checker plugin name
    progress_checker_plugin : "progress_checker"
    # List of target checker plugin names
    goal_checker_plugins : [ "general_goal_checker" ]
    # List of controller plugin names
    controller_plugins : [ "FollowPath" ]
    # Progress Checker Parameters
    progress_checker :
      # Progress Checker Plugin Type
      plugin : "nav2_controller::SimpleProgressChecker"
      # The minimum radius the robot must move
      required_movement_radius : 0.5
      # Maximum allowed movement time
```

```
movement_time_allowance : 10.0
general_goal_checker :
  # Is this a stateful target checker?
  stateful : True
  # Target Inspector Plugin Type
  plugin : "nav2_controller::SimpleGoalChecker"
  # Target tolerance in X and Y directions
  xy_goal_tolerance : 0.15
  # Target tolerance for rotation direction
  yaw_goal_tolerance : 0.15
# DWB local planner parameters
FollowPath :
  # Local planner plugin type
  plugin : "dwb_core::DWBLocalPlanner"
  # Whether to debug trajectory details
  debug_trajectory_details : True
  # Minimum speed in the X direction
  min_vel_x : 0.0
  # Minimum speed in the Y direction
  min_vel_y : 0.0
  # Maximum speed in the X direction
  max_vel_x : 0.35
  # Maximum speed in the Y direction
  max_vel_y : 0.0
  # Maximum speed in the direction of rotation
  max_vel_theta : 1.0
  # Minimum speed in the XY plane
  min_speed_xy : 0.0
  # Maximum speed in the XY plane
  max_speed_xy : 0.22
  # Minimum speed in the direction of rotation
  min_speed_theta : 0.0
  # Acceleration limit in X direction
  acc_lim_x : 2.5
  # Acceleration limit in the Y direction
  acc_lim_y : 0.0
  # Acceleration limit in the rotation direction
  acc_lim_theta : 3.2
  # Deceleration limit in X direction
  decel_lim_x : -2.5
  # Deceleration limit in Y direction
  decel_lim_y : 0.0
  # Deceleration limit in the rotation direction
  decel_lim_theta : -3.2
  # Number of velocity samples in the X direction
  vx_samples : 20
  # Number of velocity samples in the Y direction
  vy_samples : 0
  # Number of speed samples in the rotation direction
  vtheta_samples : 40
  # Simulation time
  sim_time : 1.5
  Linear resolution
  linear_granularity : 0.05
  # Angular resolution
  angular_granularity : 0.025
```

```
# Transformation tolerance time
      transform_tolerance : 0.2
      # Target tolerance in X and Y directions
      xy_goal_tolerance : 0.05
      # Speed threshold for panning to stop
      trans_stopped_velocity : 0.25
      # Whether to short-circuit trajectory evaluation
      short_circuit_trajectory_evaluation : True
      # Is it a stateful planner?
      stateful : True
      # Evaluator list
      critics : [ "RotateToGoal" , "Oscillation" , "BaseObstacle" ,
 "GoalAlign" , "PathAlign" , "PathDist" , "GoalDist" ]
      # Weight of the basic obstacle evaluator
      BaseObstacle.scale : 0.02
      # Weights of the path alignment evaluator
      PathAlign.scale : 32.0
      # Forward point distance of path alignment evaluator
      PathAlign.forward_point_distance : 0.1
      # Weights of the target alignment evaluator
      GoalAlign.scale : 24.0
      # Forward point distance of target alignment evaluator
      GoalAlign.forward_point_distance : 0.1
      # Weight of the path distance evaluator
      PathDist.scale : 32.0
      # Weight of target distance evaluator
      GoalDist.scale : 24.0
      # Rotate to the target evaluator weights
      RotateToGoal.scale : 32.0
      #Deceleration factor for rotating to target evaluator
      RotateToGoal.slowing_factor : 5.0
      # Rotate to the look-ahead time of the target evaluator
      RotateToGoal.lookahead_time : -1.0
# Controller server RCLCPP node configuration
controller_server_rclcpp_node :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
# Local costmap configuration
local_costmap :
  local_costmap :
    ros__parameters :
      # Costmap update frequency
      update_frequency : 5.0
      # How often the costmap is published
      publish_frequency : 2.0
      # Global coordinate system name
      global_frame : odom
      # The name of the robot's base coordinate system
      robot_base_frame : base_link
      # Whether to use simulation time, False means use real time
      use_sim_time : False
      # Whether to use rolling window
      rolling_window : true
      # The width of the costmap
      width : 3
```

```
# The height of the costmap
height : 3
# Costmap resolution
resolution : 0.05
# The radius of the robot
robot_radius : 0.15
# List of costmap plugins
plugins : [ "obstacle_layer" , "voxel_layer" , "inflation_layer" ]
inflation_layer :
  # Expansion layer plugin type
  plugin : "nav2_costmap_2d::InflationLayer"
  # Expansion radius
  inflation_radius : 0.3
  # Cost scaling factor
  cost_scaling_factor : 3.0
obstacle_layer :
  # Obstacle layer plugin type
  plugin : "nav2_costmap_2d::ObstacleLayer"
  # Whether to enable the obstacle layer
  enabled : True
  # Observation source name
  observation_sources : scan
  scan :
    #Topic name for laser scanning data
    topic : /scan
    # Maximum obstacle height
    max_obstacle_height : 2.0
    # Whether to clear obstacles
    clearing : True
    # Whether to mark obstacles
    marking : True
    # Data Types
    data_type : "LaserScan"
voxel_layer :
  # Voxel layer plugin type
  plugin : "nav2_costmap_2d::VoxelLayer"
  # Whether to enable voxel layer
  enabled : True
  # Whether to publish voxel map
  publish_voxel_map : True
  # Z-origin
  origin_z : 0.0
  # Z resolution
  z_resolution : 0.05
  # Number of voxels in the Z direction
  z_voxels : 16
  # Maximum obstacle height
  max_obstacle_height : 2.0
  # Marking threshold
  mark_threshold : 0
  # Observation source name
  observation_sources : scan
  scan :
    #Topic name for laser scanning data
    topic : /scan
    # Maximum obstacle height
    max_obstacle_height : 2.0
    # Whether to clear obstacles
```

```
clearing : True
          # Whether to mark obstacles
          marking : True
          # Data Types
          data_type : "LaserScan"
          # Maximum range of ray tracing
          raytrace_max_range : 3.0
          # Minimum range for ray tracing
          raytrace_min_range : 0.0
          # Maximum detection range of obstacles
          obstacle_max_range : 2.5
          # Minimum obstacle detection range
          obstacle_min_range : 0.0
      static_layer :
        # Whether to subscribe to transient local map
        map_subscribe_transient_local : True
      # Whether to always send the full costmap
      always_send_full_costmap : True
  local_costmap_client :
    ros__parameters :
      # Whether to use simulation time, False means use real time
      use_sim_time : False
  local_costmap_rclcpp_node :
    ros__parameters :
      # Whether to use simulation time, False means use real time
      use_sim_time : False
# Global costmap configuration
global_costmap :
  global_costmap :
    ros__parameters :
      # Costmap update frequency
      update_frequency : 1.0
      # How often the costmap is published
      publish_frequency : 1.0
      # Global coordinate system name
      global_frame : map
      # The name of the robot's base coordinate system
      robot_base_frame : base_link
      # Whether to use simulation time, True means to use simulation time
      use_sim_time : True
      # The radius of the robot
      robot_radius : 0.2
      # Costmap resolution
      resolution : 0.05
      # Whether to track unknown space
      track_unknown_space : false
      # List of costmap plugins
      plugins : [ "static_layer" , "obstacle_layer" , "voxel_layer" ,
 "inflation_layer" ]
      obstacle_layer :
        # Obstacle layer plugin type
        plugin : "nav2_costmap_2d::ObstacleLayer"
        # Whether to enable the obstacle layer
        enabled : True
        # Observation source name
        observation_sources : scan
        scan :
```

```
#Topic name for laser scanning data
    topic : /scan
    # Maximum obstacle height
    max_obstacle_height : 2.0
    # Whether to clear obstacles
    clearing : True
    # Whether to mark obstacles
    marking : True
    # Data Types
    data_type : "LaserScan"
    # Maximum range of ray tracing
    raytrace_max_range : 3.0
    # Minimum range for ray tracing
    raytrace_min_range : 0.0
    # Maximum detection range of obstacles
    obstacle_max_range : 2.5
    # Minimum obstacle detection range
    obstacle_min_range : 0.0
voxel_layer :
  # Voxel layer plugin type
  plugin : "nav2_costmap_2d::VoxelLayer"
  # Whether to enable voxel layer
  enabled : True
  # Whether to publish voxel map
  publish_voxel_map : True
  # Z-origin
  origin_z : 0.0
  # Z resolution
  z_resolution : 0.05
  # Number of voxels in the Z direction
  z_voxels : 16
  # Maximum obstacle height
  max_obstacle_height : 2.0
  # Marking threshold
  mark_threshold : 0
  # Observation source name
  observation_sources : scan
  scan :
    #Topic name for laser scanning data
    topic : /scan
    # Maximum obstacle height
    max_obstacle_height : 2.0
    # Whether to clear obstacles
    clearing : True
    # Whether to mark obstacles
    marking : True
    # Data Types
    data_type : "LaserScan"
    # Maximum range of ray tracing
    raytrace_max_range : 3.0
    # Minimum range for ray tracing
    raytrace_min_range : 0.0
    # Maximum detection range of obstacles
    obstacle_max_range : 2.5
    # Minimum obstacle detection range
    obstacle_min_range : 0.0
static_layer :
  # Static layer plugin type
```

```
plugin : "nav2_costmap_2d::StaticLayer"
        # Whether to subscribe to transient local map
        map_subscribe_transient_local : True
      inflation_layer :
        # Expansion layer plugin type
        plugin : "nav2_costmap_2d::InflationLayer"
        # Cost scaling factor
        cost_scaling_factor : 3.0
        # Expansion radius
        inflation_radius : 0.3
      # Whether to always send the full costmap
      always_send_full_costmap : True
  global_costmap_client :
    ros__parameters :
      # Whether to use simulation time, False means use real time
      use_sim_time : False
  global_costmap_rclcpp_node :
    ros__parameters :
      # Whether to use simulation time, False means use real time
      use_sim_time : False
# Map server configuration
map_server :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # Name of the map YAML file
    yaml_filename : "map.yaml"
# Map saver configuration
map_saver :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # Timeout for saving the map
    save_map_timeout : 5.0
    # Default idle threshold
    free_thresh_default : 0.25
    #Default occupancy threshold
    occupied_thresh_default : 0.65
    # Whether to subscribe to transient local map
    map_subscribe_transient_local : True
-
# Planner server configuration
planner_server :
  ros__parameters :
    # Desired planner frequency
    expected_planner_frequency : 5.0
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # List of planner plugin names
    planner_plugins : [ "GridBased" ]
    GridBased :
      # Grid-based planner plugin types
      plugin : "nav2_navfn_planner/NavfnPlanner"
      # Planning tolerance
      tolerance : 0.5
      # Whether to use the A* algorithm
```

```
use_astar : false
      # Whether to allow unknown space
      allow_unknown : true
# Planner server RCLCPP node configuration
planner_server_rclcpp_node :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
# Restore server configuration
recoveries_server :
  ros__parameters :
    # The topic name of the costmap
    costmap_topic : local_costmap/costmap_raw
    # Topic name of the robot footprint
    footprint_topic : local_costmap/published_footprint
    # Loop frequency
    cycle_frequency : 5.0
    # Restore plugin name list
    recovery_plugins : [ "spin" , "backup" , "wait" ]
    spin :
      # Rotation recovery plugin type
      plugin : "nav2_recoveries/Spin"
    backup :
      # Back restore plugin type
      plugin : "nav2_recoveries/BackUp"
    wait :
      # Waiting to restore plugin type
      plugin : "nav2_recoveries/Wait"
    # Global coordinate system name
    global_frame : odom
    # The name of the robot's base coordinate system
    robot_base_frame : base_link
    # Transformation timeout
    transform_timeout : 0.1
    # Whether to use simulation time, False means use real time
    use_sim_time : False
    # Look-ahead simulation time
    simulate_ahead_time : 2.0
    # Maximum rotation speed
    max_rotational_vel : 1.0
    # Minimum rotation speed
    min_rotational_vel : 0.4
    # Rotational acceleration limit
    rotational_acc_lim : 3.2
# Robot status publisher configuration
robot_state_publisher :
  ros__parameters :
    # Whether to use simulation time, False means use real time
    use_sim_time : False
# Waypoint follower configuration
waypoint_follower :
  ros__parameters :
    # Loop rate
    loop_rate : 2000
```

```
# Whether to stop on failure
stop_on_failure : false
#Waypoint task executor plugin name
waypoint_task_executor_plugin : "wait_at_waypoint"
wait_at_waypoint :
  #Waypoint wait plugin type
  plugin : "nav2_waypoint_follower::WaitAtWaypoint"
  # Whether to enable the plugin
  enabled : True
  #Waypoint pause duration
  waypoint_pause_duration : 200
```

These are the configurable parameters of Navigation2. If you need to modify the configuration parameters, after editing, the M3Pro_navigation package must be recompiled in the M3Pro_ws workspace to take effect:

```bash
colcon build --packages-select M3Pro_navigation
```
