# Multimodal Visual Understanding + SLAM Navigation

## 1. Course Content

Run example programs to perform integrated tasks using the robot's visual understanding and SLAM navigation through text-based interaction.

## 2. Start the Agent

If the agent is already running, you do not need to start it again.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

> [!NOTE]
> To use this lesson, you must first build at least one grid map by following the LiDAR course.

### 2.1 Configure the Map Mapping File

Connect to the robot desktop through VNC and start the navigation nodes:

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

Alternatively, start the display on the virtual machine. Do not start the display window repeatedly.

```bash
ros2 launch slam_view nav_rviz.launch.py
```

After RViz opens, click **2D Pose Estimate** in the top toolbar and roughly mark the robot's position and orientation on the map.

The robot model appears on the map:

![Picture: page 1: picture 10](_page_1_Picture_10.jpeg)

You can give precise points on the map readable names. This example uses **Master Bedroom** and **Kitchen**.

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

Click **Nav2 Goal** to navigate the robot to the target point that you want to mark.

![Picture: page 2: picture 2](_page_2_Picture_2.jpeg)

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

Run the following command to get the robot's current pose in the map coordinate system:

```bash
ros2 run tf2_ros tf2_echo map base_footprint
```

Open the `map_mapping.yaml` map mapping file using VNC, VS Code, the command line, or another method. For example:

```bash
nano ~/M3Pro_ws/multi_brains_file/map_mapping.yaml
```

Modify the symbolic poses under `common_map_areas`. The `name` field is the location name. Fill the `position` and `orientation` fields with the pose information obtained earlier.

```yaml
# According to the actual scene environment, customize the areas in the map.
# You can add any number of areas, as long as they are consistent with the
# map mapping used by the large model.
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

### 2.2 Configure Map Mapping Variables in Dify

After configuring the map mapping file, tell the large language model the relationship between map symbols and location names.

Start Dify if it is not already running:

```bash
bringup_dify
```

Enter the robot's IP address in the browser address bar to open the Dify management page, then select the corresponding AI application.

> [!NOTE]
> International users: `multi_brains_en`

![Picture: page 5: picture 6](_page_5_Picture_6.jpeg)

Click **Session Variables** in the upper-right corner, then click the edit button for the `map_mapping` variable.

![Figure: page 5: figure 8](_page_5_Figure_8.jpeg)

In the **Edit Session Variables** pop-up window, edit the mapping relationship according to the map mapping file, then click **Save**.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

Finally, click **Publish** -> **Publish Update** to save the changes.

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

## 3. Run the Example

### 3.1 Start the Program

Connect to the robot desktop through VNC, open a terminal, and run:

```bash
ros2 launch multi_brains llm_agent_control.launch.py text_chat_mode:=True
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

Initialize navigation by clicking **2D Pose Estimate** in RViz and roughly marking the robot's position and orientation on the map. After initialization, preparation is complete.

![Picture: page 8: picture 9](_page_8_Picture_9.jpeg)

Start the text interaction program:

```bash
ros2 run text_chat text_chat
```

### 3.2 Test Case

The following is a sample test case. You can also create your own dialogue commands.

```text
Please remember your current location, then navigate to the kitchen and the master bedroom in sequence, remembering the items you see in each place. Finally, return to your starting position and tell me what you saw in those two places?
```

Copy and paste the test case into the text interaction terminal.

![Figure: page 9: figure 4](_page_9_Figure_4.jpeg)

The decision-making AI outputs the planned task steps, and the execution-layer AI executes those steps.
