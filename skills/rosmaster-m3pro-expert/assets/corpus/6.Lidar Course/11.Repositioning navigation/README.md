# Rapid Relocalization and Navigation

## 1. Course Content

- Learn how to use rapid relocalization with Navigation2.
- Run the program in RViz and observe how the robot localizes itself on the map while continuing SLAM-based localization and navigation.

## 2. Principle Overview

### 2.1 Introduction

- Navigation2 (Nav2) is the ROS 2 navigation framework for safely moving a mobile robot from one pose to another.
- Navigation2 normally uses AMCL (Adaptive Monte Carlo Localization) for localization on a known map. This example replaces AMCL with Cartographer localization while keeping the rest of the navigation stack unchanged.

### 2.2 Differences Between the Two Localization Methods

- **AMCL**: Best for a known environment with a pre-built map, such as repeated indoor navigation tasks.
- **Cartographer**: Better when the robot must localize while updating or building a map, especially in a new or changing environment.

## 3. Preparation

### 3.1 Content Description

This lesson uses the Jetson Orin NX as an example. On Raspberry Pi and Jetson Nano boards, open a terminal and enter the Docker container before running the commands in this lesson. For Docker entry steps, refer to **[Configuration and Operation Guide]--[Entering the Docker (Jetson Nano and Raspberry Pi 5 users, see here)]**. On Orin and NX boards, run the commands directly in a terminal.

### 3.2 Map Preparation

Before running rapid relocalization, save a PBStream map by following [6. LiDAR - 7. Cartographer Mapping]. The PBStream file is saved in the home directory. On Raspberry Pi and Jetson Nano, it is saved under /root inside Docker.

## 4. Running the Example

### 4.1 Single-Point Navigation Function

#### Note:

The Jetson Nano and Raspberry Pi series controllers must first enter the Docker container (see the [Docker Course Chapter - Entering the Robot's Docker Container] for steps).

Start the low-level sensors from the robot terminal:

```bash
ros2 launch M3Pro_navigation base_bringup.launch.py
```

Start the Cartographer localization node:

```bash
ros2 launch M3Pro_navigation cartographer_localization.launch.py
```

Finally, start Navigation2.

```bash
ros2 launch M3Pro_navigation navigation_launch.py
```

RViz can be launched from either the robot or the virtual machine. **Choose one method only**; do not start RViz in both places at the same time.

To launch RViz from the virtual machine:

```bash
ros2 launch slam_view nav_rviz.launch.py
```

To launch RViz from the robot:

```bash
ros2 launch M3Pro_navigation nav_rviz.launch.py
```

![Figure: page 2: figure 1](_page_2_Figure_1.jpeg)

- RViz shows the robot automatically estimating its initial position, so manual initialization is usually not required.
- If the initial pose is far from the real robot pose, use [2D Pose Estimate] in RViz to give the approximate position and speed up localization.

### 4.3 Viewing the Node Communication Graph

Run in the VM terminal:

```bash
ros2 run rqt_graph rqt_graph
```

If the graph does not display at first, select [Nodes/Topics (all)] and click the refresh button in the upper left corner. The original image is large and can be viewed in this lesson folder.

![Picture: page 2: picture 8](_page_2_Picture_8.jpeg)

### 4.4 Viewing the TF Tree

Enter the VM terminal:

```bash
ros2 run rqt_tf_tree rqt_tf_tree
```

If the page doesn't display initially, click the refresh icon in the upper left corner to refresh the page. The original image is too large; you can view it in the current lesson folder.

![Figure: page 3: figure 4](_page_3_Figure_4.jpeg)

## 5. Principle Explanation

Rapid relocalization works by replacing Navigation2's default AMCL localization with Cartographer localization. The rest of the Navigation2 stack remains unchanged. The following files show how that replacement is configured.

Source code location:

Jetson Orin Nano, Jetson Orin NX:

```
/home/jetson/M3Pro_ws/M3Pro_navigation/launch
```

Jetson Nano, Raspberry Pi:

You need to first enter Docker.

```
/root/M3Pro_ws/M3Pro_navigation/launch
```

Find the navigation_launch.py file in the launch directory. The contents are as follows:

This file modifies the default Navigation2 launch file, removing the node that originally enabled the AMCL localization method. The rest of the navigation stack remains unchanged.

```python
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction,
SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
```

```python
from launch_ros.actions import LoadComposableNodes
from launch_ros.actions import Node
from launch_ros.descriptions import ComposableNode, ParameterFile
from nav2_common.launch import RewrittenYaml
def generate_launch_description():
    # Get the launch directory
    bringup_dir = get_package_share_directory('nav2_bringup')
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    use_composition = LaunchConfiguration('use_composition')
    container_name = LaunchConfiguration('container_name')
    container_name_full = (namespace, '/', container_name)
    use_respawn = LaunchConfiguration('use_respawn')
    log_level = LaunchConfiguration('log_level')
    param_file_name = "yahboom_M3Pro_carto.yaml"
    lifecycle_nodes = ['controller_server',
                       'smoother_server',
                       'planner_server',
                       'behavior_server',
                       'bt_navigator',
                       'waypoint_follower',
                       'velocity_smoother']
    # Map fully qualified names to relative ones so the node's namespace can be
prepended.
    # In case of the transforms (tf), currently, there doesn't seem to be a
better alternative
    # https://github.com/ros/geometry2/issues/32
    # https://github.com/ros/robot_state_publisher/pull/30
    # TODO(orduno) Substitute with `PushNodeRemapping`
    # https://github.com/ros2/launch_ros/issues/56
    remappings = [('/tf', '/tf'),
                  ('/tf_static', '/tf_static')]
    # Create our own temporary YAML files that include substitutions
    param_substitutions = {
        'use_sim_time': use_sim_time,
        'autostart': autostart}
    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True),
        allow_substs=True)
    stdout_linebuf_envvar = SetEnvironmentVariable(
        'RCUTILS_LOGGING_BUFFERED_STREAM', '1')
    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
```

```
default_value='',
        description='Top-level namespace')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')
    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        # default_value=os.path.join(bringup_dir, 'params', 'nav2_params.yaml'),
 default_value=os.path.join(get_package_share_directory("M3Pro_navigation"),
"param", param_file_name ),
        description='Full path to the ROS2 parameters file to use for all
launched nodes')
    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart', default_value='true',
        description='Automatically startup the nav2 stack')
    declare_use_composition_cmd = DeclareLaunchArgument(
        'use_composition', default_value='False',
        description='Use composed bringup if True')
    declare_container_name_cmd = DeclareLaunchArgument(
        'container_name', default_value='nav2_container',
        description='the name of container that nodes will load in if use
composition')
    declare_use_respawn_cmd = DeclareLaunchArgument(
        'use_respawn', default_value='False',
        description='Whether to respawn if a node crashes. Applied when
composition is disabled.')
    declare_log_level_cmd = DeclareLaunchArgument(
        'log_level', default_value='info',
        description='log level')
    load_nodes = GroupAction(
        condition=IfCondition(PythonExpression(['not ', use_composition])),
        actions=[
            Node(
                package='nav2_controller',
                executable='controller_server',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings + [('cmd_vel', 'cmd_vel_nav')]),
            Node(
                package='nav2_smoother',
                executable='smoother_server',
                name='smoother_server',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
```

```
parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
           Node(
                package='nav2_planner',
                executable='planner_server',
                name='planner_server',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
           Node(
                package='nav2_behaviors',
                executable='behavior_server',
                name='behavior_server',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
           Node(
                package='nav2_bt_navigator',
                executable='bt_navigator',
                name='bt_navigator',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
           Node(
                package='nav2_waypoint_follower',
                executable='waypoint_follower',
                name='waypoint_follower',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings),
           Node(
                package='nav2_velocity_smoother',
                executable='velocity_smoother',
                name='velocity_smoother',
                output='screen',
                respawn=use_respawn,
                respawn_delay=2.0,
                parameters=[configured_params],
                arguments=['--ros-args', '--log-level', log_level],
                remappings=remappings +
                        [('cmd_vel', 'cmd_vel_nav'), ('cmd_vel_smoothed',
'cmd_vel')]),
           Node(
                package='nav2_lifecycle_manager',
                executable='lifecycle_manager',
```

```
name='lifecycle_manager_navigation',
               output='screen',
               arguments=['--ros-args', '--log-level', log_level],
               parameters=[{'use_sim_time': use_sim_time},
                            {'autostart': autostart},
                            {'node_names': lifecycle_nodes}]),
       ]
   )
   load_composable_nodes = LoadComposableNodes(
       condition=IfCondition(use_composition),
       target_container=container_name_full,
       composable_node_descriptions=[
           ComposableNode(
               package='nav2_controller',
               plugin='nav2_controller::ControllerServer',
               name='controller_server',
               parameters=[configured_params],
               remappings=remappings + [('cmd_vel', 'cmd_vel_nav')]),
           ComposableNode(
               package='nav2_smoother',
               plugin='nav2_smoother::SmootherServer',
               name='smoother_server',
               parameters=[configured_params],
               remappings=remappings),
           ComposableNode(
               package='nav2_planner',
               plugin='nav2_planner::PlannerServer',
               name='planner_server',
               parameters=[configured_params],
               remappings=remappings),
           ComposableNode(
               package='nav2_behaviors',
               plugin='behavior_server::BehaviorServer',
               name='behavior_server',
               parameters=[configured_params],
               remappings=remappings),
           ComposableNode(
               package='nav2_bt_navigator',
               plugin='nav2_bt_navigator::BtNavigator',
               name='bt_navigator',
               parameters=[configured_params],
               remappings=remappings),
           ComposableNode(
               package='nav2_waypoint_follower',
               plugin='nav2_waypoint_follower::WaypointFollower',
               name='waypoint_follower',
               parameters=[configured_params],
               remappings=remappings),
           ComposableNode(
               package='nav2_velocity_smoother',
               plugin='nav2_velocity_smoother::VelocitySmoother',
               name='velocity_smoother',
               parameters=[configured_params],
               remappings=remappings +
                           [('cmd_vel', 'cmd_vel_nav'), ('cmd_vel_smoothed',
'cmd_vel')]),
           ComposableNode(
```

```
package='nav2_lifecycle_manager',
            plugin='nav2_lifecycle_manager::LifecycleManager',
            name='lifecycle_manager_navigation',
            parameters=[{'use_sim_time': use_sim_time,
                         'autostart': autostart,
                         'node_names': lifecycle_nodes}]),
    ],
)
# Create the launch description and populate
ld = LaunchDescription()
# Set environment variables
ld.add_action(stdout_linebuf_envvar)
# Declare the launch options
ld.add_action(declare_namespace_cmd)
ld.add_action(declare_use_sim_time_cmd)
ld.add_action(declare_params_file_cmd)
ld.add_action(declare_autostart_cmd)
ld.add_action(declare_use_composition_cmd)
ld.add_action(declare_container_name_cmd)
ld.add_action(declare_use_respawn_cmd)
ld.add_action(declare_log_level_cmd)
# Add the actions to launch all of the navigation nodes
ld.add_action(load_nodes)
ld.add_action(load_composable_nodes)
return ld
```

Find the cartographer_localization.launch.py file in the launch directory. The contents are as follows:

This file starts the Cartographer node and replaces the default Navigation2 localization method.

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import Shutdown
def generate_launch_description():
    load_state_filename_arg = DeclareLaunchArgument(
        'load_state_filename',
        default_value='/home/jetson/yahboom_map.pbstream'
        )
    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='true',
    )
    cartographer_node = Node(
```

```
package = 'cartographer_ros',
        executable = 'cartographer_node',
        parameters = [{'use_sim_time': False}],
        arguments = [
            '-configuration_directory',
FindPackageShare('M3Pro_navigation').find('M3Pro_navigation') + '/param',
            '-configuration_basename', 'yahboom_M3Pro.lua',
            '-load_state_filename', LaunchConfiguration('load_state_filename')],
        remappings = [
            ('imu', '/imu/data')],
        output = 'screen'
        )
    cartographer_occupancy_grid_node = Node(
        package = 'cartographer_ros',
        executable = 'cartographer_occupancy_grid_node',
        parameters = [
            {'use_sim_time': False},
            {'resolution': 0.05}],
        )
    rviz_node = Node(
        package = 'rviz2',
        executable = 'rviz2',
        on_exit = Shutdown(),
        arguments = ['-d',
FindPackageShare('cartographer_ros').find('cartographer_ros') +
'/configuration_files/demo_2d.rviz'],
        parameters = [{'use_sim_time': False}],
        condition=IfCondition(LaunchConfiguration('use_rviz'))
    )
    return LaunchDescription([
        # Launch arguments
        load_state_filename_arg,
        use_rviz_arg,
        # Nodes
        cartographer_node,
        cartographer_occupancy_grid_node,
        #rviz_node,
    ])
```
