# Multimodal Visual Understanding + SLAM Navigation

## 1. Course Content

- Basic: Run example programs that combine the robot's visual understanding with SLAM navigation.
- Advanced: Learn the key source code introduced in this section.

## 2. Preparation

### 2.1 Content Description

This lesson uses Jetson Orin NX as the example. For Raspberry Pi and Jetson Nano boards, open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For instructions, see **Entering the Robot Docker Container (for Jetson Nano and Raspberry Pi 5 users)** in **0. Configuration and Operation Guide**.

For Orin and NX boards, open a terminal directly on the robot and run the commands from this lesson.

### 2.2 Start the Agent

If the agent is already running, you do not need to start it again.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

> [!NOTE]
> To use this lesson, you must first build at least one grid map by following the LiDAR course.

### 2.3 Configure the Map Mapping File

Connect to the robot desktop through VNC and start the navigation nodes:

```bash
ros2 launch M3Pro_navigation base_bringup.launch.py
ros2 launch M3Pro_navigation navigation2.launch.py
```

Start RViz on the robot:

```bash
ros2 launch M3Pro_navigation nav_rviz.launch.py
```

Alternatively, start the display on the virtual machine. Do not start the display window repeatedly.

```bash
ros2 launch slam_view nav_rviz.launch.py
```

After RViz opens, click **2D Pose Estimate** in the top toolbar and roughly mark the robot's position and orientation on the map.

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

You can give precise points on the map readable names. This example uses **Master Bedroom** and **Kitchen**.

![Picture: page 2: picture 2](_page_2_Picture_2.jpeg)

Click **Nav2 Goal** to navigate the robot to the target point that you want to mark.

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

![Picture: page 3: picture 1](_page_3_Picture_1.jpeg)

Run the following command to get the robot's current pose in the map coordinate system:

```bash
ros2 run tf2_ros tf2_echo map base_footprint
```

Open the `map_mapping.yaml` map mapping file:

```bash
nano ~/M3Pro_ws/multi_brains_file/map_mapping.yaml
```

Modify the symbolic poses under `common_map_areas`. The `name` field is the location name. Fill the `position` and `orientation` fields with the pose information obtained earlier.

```yaml
common_map_areas:
  A:
    name: 'Master Bedroom'
    position:
      x: 3.974
      y: -2.634
    orientation:
      x: 0.0
      y: 0.0
      z: -0.688
      w: 0.726
  B:
    name: 'xxx'
    position:
      x: 1.488
      y: 0.661
      z: 0.0
    orientation:
      x: 0.0
      y: 0.0
      z: 0.725
      w: 0.688
```

After you save the file, the changes take effect immediately.

### 2.4 Configure Map Mapping Variables in Dify

After configuring the map mapping file, tell the large language model the relationship between map symbols and location names.

Start Dify if it is not already running:

```bash
bringup_dify
```

Enter the robot's IP address in the browser address bar to open the Dify management page, then select the corresponding AI application.

> [!NOTE]
> International users: `multi_brains_en`

![Picture: page 5: picture 9](_page_5_Picture_9.jpeg)

Click **Session Variables** in the upper-right corner, then click the edit button for the `map_mapping` variable.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

In the **Edit Session Variables** pop-up window, edit the mapping relationship according to the map mapping file, then click **Save**.

![Figure: page 6: figure 2](_page_6_Figure_2.jpeg)

Finally, click **Publish** -> **Publish Update** to save the changes.

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

## 3. Run the Example

### 3.1 Start the Program

On the robot terminal, start the AI agent system:

```bash
ros2 launch multi_brains llm_agent_control.launch.py
```

Alternatively, use the shortcut command:

```bash
multi_brains
```

Start the navigation nodes on the robot:

```bash
ros2 launch M3Pro_navigation base_bringup.launch.py
```

```bash
ros2 launch M3Pro_navigation navigation2.launch.py
```

Start RViz on the robot:

```bash
ros2 launch M3Pro_navigation nav_rviz.launch.py
```

Initialize navigation in RViz by clicking **2D Pose Estimate** and roughly marking the robot's position and orientation on the map. After initialization, preparation is complete.

![Picture: page 8: picture 11](_page_8_Picture_11.jpeg)

### 3.2 Test Case

The following case is for reference. Give instructions according to your needs.

```text
Please remember your current location first, then navigate to the kitchen and the master bedroom in sequence, remembering the items you see. Finally, return to your starting position and tell me what you saw in those two places?
```

Wake the robot and speak the command. The execution-layer large model executes subtasks according to the task steps planned by the decision-layer model.

## 4. Source Code Analysis

Robot action source code path:

```text
~/M3Pro_ws/src/multi_brains/multi_brains/action_service.py
```

This case uses the `seewhat`, `navigation`, `load_target_points`, and `get_current_pose` methods in the `CustomActionServer` class. `seewhat` is explained in **Multimodal Visual Understanding + Robotic Arm Grasping**. This section introduces `navigation`, `load_target_points`, and `get_current_pose`.

The initialization function creates a Nav2 navigation client for sending navigation target requests, and creates a TF listener for the coordinate transformation between `map` and `base_footprint`.

```python
# Create a navigation action client to request the navigation action server.
self.navclient = ActionClient(self, NavigateToPose, 'navigate_to_pose')
# Create a TF listener to listen for coordinate transformations.
self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)
```

### `load_target_points`

This function loads target point coordinates from `map_mapping.yaml` and creates a navigation dictionary that stores each symbol and its corresponding map coordinates. Each point coordinate is a `PoseStamped`.

### `navigation`

The navigation function receives a symbol parameter, looks up its coordinates in the dictionary, and uses `self.navclient` to request the ROS 2 navigation action server. When the navigation action server returns status `4`, navigation succeeded. Other values indicate failure, such as obstacles or planning failure. After navigation finishes, the function reports the action result to the large language model.

### `get_current_pose`

The `get_current_pose` function retrieves the robot's current map coordinates in the global coordinate system and stores them in a dictionary for later use.
