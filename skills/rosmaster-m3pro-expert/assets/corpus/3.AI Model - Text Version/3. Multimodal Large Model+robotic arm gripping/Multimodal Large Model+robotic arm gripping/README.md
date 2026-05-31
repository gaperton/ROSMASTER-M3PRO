# Multimodal Visual Understanding + Robotic Arm Grasping

## 1. Course Content

Run the example program and use the robot's visual understanding together with robotic arm grasping to complete integrated tasks.

> [!NOTE]
> The only difference between the text version and the voice version is the command input method. The text version does not use speech recognition or speech synthesis playback.

## 2. Start the Agent

If the agent is already running, you do not need to start it again.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

## 3. Run the Example

### 3.1 Start the Program

Connect to the robot screen through VNC and start the AI agent:

```bash
ros2 launch multi_brains llm_agent_control.launch.py text_chat_mode:=True
```

Start text interaction in any terminal:

```bash
ros2 run text_chat text_chat
```

### 3.2 Test Cases

The following are reference test cases. You can also create your own dialogue commands.

- Find the red cube in front of you and grasp it. Wooden blocks used: 30 x 30 x 30 mm blocks.
- Place the red cube in front of you to the right of the blue cube. Wooden blocks used: 30 x 30 x 30 mm blocks.
- Please remove the AprilTag block in front of you that is taller than 5 centimeters. Wooden blocks used: 30 x 30 x 30 mm blocks.
- Track AprilTag number three. Wooden blocks used: 40 x 40 x 40 mm blocks.

#### 3.2.1 Case 1: "Find the red cube in front of you and grasp it"

Enter `Find the red cube in front of you and grasp it` in the terminal. The terminal prints the following information:

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

After `grasp_obj()` is called, a window named **rgb_img** opens on the VNC screen and displays the robot's view. The robot automatically adjusts its distance from the target object. After distance adjustment is complete, the robotic arm grasps the target object.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

After the robot picks up an object, the robotic arm remains in its current position. To return the arm to its initial posture, use one of the following methods:

- Method 1: Enter `Put down the block you just picked up` so the robot puts down the red block.
- Method 2: Enter `End the current task` so the robot ends the current task cycle. After the cycle ends, the robotic arm resets to its initial posture.

This example uses Method 2 to end the task and reset the task cycle.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

#### 3.2.2 Case 2: "Put the red block in front of you to the right of the blue block"

Enter `Put the red block in front of you to the right of the blue block` in the terminal. The terminal prints the following information:

![Figure: page 3: figure 3](_page_3_Figure_3.jpeg)

A window named **rgb_img** opens on the VNC screen and displays the robot's view. The robot automatically adjusts its distance from the target object. After distance adjustment is complete, the robotic arm picks up the target object.

![Picture: page 4: picture 1](_page_4_Picture_1.jpeg)

Then the robot translates to the right, puts down the red block with the robotic arm, and reports that the task is complete.

![Figure: page 4: figure 3](_page_4_Figure_3.jpeg)

When you enter commands such as `End current task` or `You can rest now`, the robot ends the current task.

#### 3.2.3 Case 3: "Please help me remove the AprilTag block in front of you that is taller than 5 centimeters"

Enter `Please help me remove the AprilTag block in front of you that is taller than 5 centimeters` in the terminal. The terminal prints the following information:

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

A window named **result_image** opens on the VNC screen and displays the robot's view. The height of each AprilTag block is shown. After distance measurement stabilizes, the robot automatically adjusts its distance from the target, then uses the robotic arm to pick up the AprilTag block at the target height and move it to the right side of the robot.

![Figure: page 6: figure 2](_page_6_Figure_2.jpeg)

When you enter a command such as `end current task` or `you can rest now`, the robot ends the current task.

## 4. Source Code Analysis

Robot action source code path:

```text
~/M3Pro_ws/src/multi_brains/multi_brains/action_service.py
```

### 4.1 Case 1

Case 1 uses the `seewhat` and `grasp_obj` methods in the `ActionController` class. The `seewhat` function obtains the color image from the depth camera and was explained in **Multimodal Visual Understanding**. This section explains `grasp_obj`.

The coordinate rules for objects in the robotic arm grasping view are shown below.

![Picture: page 7: picture 9](_page_7_Picture_9.jpeg)

The `grasp_obj(x1, y1, x2, y2)` function calls the robotic arm to grasp the target object. The parameters are the top-left and bottom-right coordinates of the target object's bounding box. The top-left corner of the image is the pixel coordinate origin.

For example, in Case 1, the large model response provides the bounding box coordinates for the red square: top-left `(365, 200)` and bottom-right `(408, 261)`.

`grasp_obj` starts three subprocesses: `grasp_desktop`, `KCF_follow`, and `ALM_KCF_Tracker_Node`. It then passes the parameters provided by the large model to the `ALM_KCF_Tracker_Node` node through a topic.

After grasping is complete, the `KCF_follow` node publishes `grasp_obj_done` on the `largemodel_arm_done` topic. The `action_feedback_callback` function uses this signal to set the `grasp_obj_future` object.

### 4.2 Case 2

The `set_cmdvel` function controls the robot base by publishing the `cmd_vel` velocity topic.

```python
def set_cmdvel(self, linear_x: str, linear_y: str, angular_z: str, duration: str) -> None:
    '''Publish cmd_vel velocity command'''
    linear_x = float(linear_x)
    linear_y = float(linear_y)
    angular_z = float(angular_z)
    duration = float(duration)
    twist = Twist()
    twist.linear.x = linear_x
    twist.linear.y = linear_y
    twist.angular.z = angular_z
    self._execute_action(twist, durationtime=duration)
    self.stop()
    return True
```

The `putdown` method makes the robotic arm put down the object it is holding.

```python
def putdown(self):
    self.pubSix_Arm(self.putsown_joints) # Deploy the robotic arm.
    time.sleep(4)
    self.pubSingle_Arm(6, 30, 1000) # Open the gripper and release the object.
    time.sleep(3)
    self.pubSix_Arm(self.init_joints) # Retract the robotic arm.
    return True
```

### 4.3 Case 3

The `apriltag_remove_higher` method starts the external `grasp_desktop_remove` and `apriltag_remove_higher` nodes through subprocesses. This function removes an AprilTag block at a specified height.
