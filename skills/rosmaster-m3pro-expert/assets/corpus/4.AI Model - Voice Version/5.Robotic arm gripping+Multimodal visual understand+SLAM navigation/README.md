# Robotic Arm Grasping + Multimodal Visual Understanding + SLAM Navigation

## 1. Course Content

Basic: Run the example program and combine Nav2 navigation, robotic arm grasping, and large-model visual understanding to perform complex tasks.

Advanced: Learn the key source code introduced in this tutorial.

**This chapter requires the map mapping file to be configured first.**

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

## 3. Run the Example

### 3.1 Start the Program

On the robot terminal, start the AI agent:

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

![Picture: page 2: picture 4](_page_2_Picture_4.jpeg)

### 3.2 Test Case

Wooden blocks used: 30 x 30 x 30 mm blocks.

The following case is for reference. You can also create your own dialogue commands.

```text
I am currently in the master bedroom. Please bring the red cube in front of you to the master bedroom.
```

The decision-layer model plans the task steps. According to those steps, the robot first observes the environment in front of it and picks up the red block.

![Picture: page 3: picture 4](_page_3_Picture_4.jpeg)

Then the robot navigates to the target point along the path planned by the global planner.

![Picture: page 4: picture 0](_page_4_Picture_0.jpeg)

After arriving at the navigation target, the robot uses the robotic arm to put down the red block and reports that the task is complete. The robot then enters a waiting state while retaining previous conversation memory. The user can continue the conversation or ask the robot to end the current task and start a new task cycle.

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

## 4. Source Code Analysis

This example uses the `seewhat`, `navigation`, `load_target_points`, `putdown`, and `grasp_obj` methods in the `CustomActionServer` class. `seewhat`, `navigation`, `load_target_points`, and `grasp_obj` were explained in previous sections. This section introduces `putdown`.

### `putdown`

This function controls the robotic arm to release the object it has grasped. After the robot grasps an object, the arm remains in a gripping state. Calling this function releases the object by publishing robotic arm joint topics. A return value of `True` indicates successful execution, and the result is sent back to the large language model for the next operation.

```python
def putdown(self):
    self.pubSix_Arm(self.putsown_joints) # Deploy the robotic arm.
    time.sleep(4)
    self.pubSingle_Arm(6, 30, 1000) # Open the gripper and release the object.
    time.sleep(3)
    self.pubSix_Arm(self.init_joints) # Retract the robotic arm.
    return True
```
