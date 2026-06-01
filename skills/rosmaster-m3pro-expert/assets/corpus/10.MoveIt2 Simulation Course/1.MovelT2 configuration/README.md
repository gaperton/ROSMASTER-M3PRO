# MoveIt2 Configuration

Raspberry Pi 5 and Jetson Nano run ROS in Docker, so MoveIt2 performance is usually limited on those boards. Raspberry Pi 5 and Jetson Nano users should run these MoveIt2 examples in the virtual machine. Orin users can run the same commands directly on the robot because ROS runs directly on the Orin mainboard. This lesson uses the virtual machine as the example environment.

## 1. Content Description

This lesson explains how to configure MoveIt2 and generate the parameter files and launch files required for M3Pro arm simulation.

## 2. Introduction to MoveIt2

MoveIt 2 is the ROS 2 version of **MoveIt**. It is an open-source framework for robotic motion planning, manipulation, 3D perception, kinematics, collision detection, and task planning. It is widely used with industrial robots, service robots, mobile manipulators, and robotics education platforms.

### 2.1. Differences from MoveIt

| Characteristic               | MoveIt               | MoveIt2                                               |
|------------------------------|----------------------|-------------------------------------------------------|
| ROS version                  | ROS 1                | ROS 2                                                 |
| Real-time behavior           | Limited support      | Better real-time performance                          |
| Cross-platform support       | Mainly Linux         | Linux, Windows, and macOS through ROS 2               |
| Motion Planning Interface | ActionLib (ROS 1) | Action (ROS 2)                                        |
| Default planner              | OMPL                 | OMPL, plus more optimization options                  |

### 2.2. MoveIt2 Core Functions

- **Motion Planning**: Supports multiple planning algorithms, such as OMPL, CHOMP, and STOMP, to generate collision-free trajectories.
- **Inverse Kinematics (IK)**: Calculates the robot's joint angles to achieve the target pose.
- **Collision Checking**: Provides collision detection based on **FCL (Flexible Collision Library)**.
- **3D Perception Integration**: Supports point cloud and depth camera data, such as RealSense and Kinect data.
- **Manipulation**: Provides high-level interfaces for grasping and placing objects.
- **Task Planning**: Combines **Behavior Trees** for high-level task orchestration.

### 2.3. Install MoveIt2

MoveIt2 is already installed in the provided virtual machine, so no installation is required there. To install MoveIt2 in a new environment, use:

```bash
#Change the <distro> below to your own ROS version. It is recommended to use
humble (22.04) or Rolling (24.04)
sudo apt install ros-<distro>-moveit -y
```

### 2.4. References

MoveIt2 source code:

[GitHub - moveit/moveit2:](https://github.com/moveit/moveit2)  MoveIt for ROS 2

Official tutorial documentation:

[MoveIt 2 Documentation - MoveIt Documentation: Humble documentation](https://moveit.picknik.ai/humble/index.html)

## 3. Program Startup

In the virtual machine terminal, create a folder under the ROS workspace `src` directory to store the generated MoveIt configuration package. This lesson uses the `moveit2_ws` workspace as the example.

```bash
cd moveit2_ws/src
mkdir test_config
```

Start MoveIt Setup Assistant:

```bash
ros2 run moveit_setup_assistant moveit_setup_assistant
```

After the program starts, the configuration screen appears.

![Figure: page 1: figure 14](_page_1_Figure_14.jpeg)

Click [Create New MoveIt Configuration Package].

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

Click [Browse] and select the M3Pro URDF file from `/home/yahboom/moveit2_ws/src/yahboom_M3Pro_description/urdf`. After selecting the file, click [Load Files]. The setup assistant loads the URDF and displays the M3Pro robot model on the right.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

Click [Self-Collisions] in the left configuration bar. This step configures self-collision detection. Click [Generate Collisions Matrix] to complete the configuration.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

Click [Planning Groups] in the left configuration bar. Click [Add Group] to create the first planning group.

![Figure: page 3: figure 2](_page_3_Figure_2.jpeg)

Create the `arm_group` planning group for the robotic arm.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

Add joints to this planning group. Click [Add Joints], select `arm_Joint1` through `arm_Joint5` on the left, click `>` to add them, then click [Save].

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

After completing the `arm_group` settings, click [Add Group] to add the gripper planning group.

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

Set the parameters as shown below, then click [Add Links] to open the link selection interface.

![Figure: page 5: figure 2](_page_5_Figure_2.jpeg)

In the link selection interface, select `llink1`, `llink2`, `llink3`, `rlink1`, `rlink2`, and `rlink3` on the left. Click `>` to add them, then click [Save].

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

The completed gripper planning group is shown below.

![Figure: page 6: figure 2](_page_6_Figure_2.jpeg)

The planning group settings are now complete. Click [Robot Groups] in the left column to configure preset poses for the robotic arm and gripper.

Click [Add Pose].

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

Configure the `up` pose for the `arm_group` planning group as shown below. Use the middle sliders to set the pose; the URDF preview on the right updates with the selected posture. Click [Save] when finished.

![Figure: page 7: figure 2](_page_7_Figure_2.jpeg)

Use the same process to set the `down` and `init` poses for `arm_group`.

Down posture:

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)

### Init Posture

![Figure: page 8: figure 2](_page_8_Figure_2.jpeg)

After configuring the three `arm_group` poses, configure the `close` and `open` poses for `grip_group`. Make sure [Planning Group] is set to `grip_group`.

#### Close Posture

![Figure: page 9: figure 0](_page_9_Figure_0.jpeg)

#### Open Posture

![Figure: page 9: figure 2](_page_9_Figure_2.jpeg)

The completed [Robot Poses] settings are shown below.

![Figure: page 10: figure 0](_page_10_Figure_0.jpeg)

Click [End Effectors] in the left column to configure the end effector, then click [Add End Effector].

![Figure: page 10: figure 2](_page_10_Figure_2.jpeg)

Enter the settings shown below, then click [Save].

![Figure: page 11: figure 0](_page_11_Figure_0.jpeg)

The completed [End Effectors] settings are shown below.

![Figure: page 11: figure 2](_page_11_Figure_2.jpeg)

Click [ros2_control URDF Modifications] in the left column. No URDF model changes are needed for this lesson; click [Add interfaces] as shown below.

![Figure: page 12: figure 0](_page_12_Figure_0.jpeg)

Click [ROS2 Controllers] in the left column to configure motion controllers. Click [Add Controller].

![Figure: page 12: figure 2](_page_12_Figure_2.jpeg)

Add the `arm_group_controller` controller as shown below.

![Figure: page 13: figure 0](_page_13_Figure_0.jpeg)

Click [Add Planning Group Joints], select `arm_group` on the left, click `>` to add it, then click [Save].

![Figure: page 13: figure 2](_page_13_Figure_2.jpeg)

The first completed controller is shown below.

![Figure: page 14: figure 0](_page_14_Figure_0.jpeg)

Add the second controller. Click [Add Controller] and configure it as shown below.

![Figure: page 14: figure 2](_page_14_Figure_2.jpeg)

Click [Add Planning Group Joints], select `grip_group` on the left, click `>` to add it, then click [Save].

![Figure: page 15: figure 0](_page_15_Figure_0.jpeg)

The completed [ROS2 Controllers] settings are shown below.

![Figure: page 15: figure 2](_page_15_Figure_2.jpeg)

Click [MoveIt Controllers] in the left column. This section configures the trajectory controllers that execute planned trajectories.

The trajectory is sent to the ROS 2 controller. Click [Add Controller] to add a trajectory controller.

![Figure: page 16: figure 0](_page_16_Figure_0.jpeg)

In the settings interface, configure the controller as shown below. The [Controller Name] must match the [ROS2 Controller] name configured in the previous step. Then click [Add Planning Group Joints].

![Figure: page 16: figure 2](_page_16_Figure_2.jpeg)

Select `arm_group` on the left, click `>` to add it, then click [Save].

![Figure: page 17: figure 0](_page_17_Figure_0.jpeg)

The completed controller is shown below.

![Figure: page 17: figure 2](_page_17_Figure_2.jpeg)

Add the gripper trajectory controller. Click [Add Controller], configure it as shown below, then click [Add Planning Group Joints].

![Figure: page 18: figure 0](_page_18_Figure_0.jpeg)

Select `grip_group` on the left, click `>` to add it, then click [Save].

![Figure: page 18: figure 2](_page_18_Figure_2.jpeg)

The completed [MoveIt Controllers] settings are shown below.

![Figure: page 19: figure 0](_page_19_Figure_0.jpeg)

Click [Author Information] in the left column, then enter your name and email address.

![Figure: page 19: figure 2](_page_19_Figure_2.jpeg)

Click [Configuration Files] in the left column, click [Browse], and select the folder created earlier: `/home/yahboom/moveit2_ws/src/test_moveit_config`. Click [OK] when prompted.

![Figure: page 20: figure 0](_page_20_Figure_0.jpeg)

Click [Generate Package] to generate the package. Click [OK] when prompted.

![Figure: page 20: figure 2](_page_20_Figure_2.jpeg)

Click [OK] on the next prompt.

![Figure: page 21: figure 0](_page_21_Figure_0.jpeg)

When **the Configuration package generated successfully** appears, click [Exit Setup Assistant] to finish.

![Figure: page 21: figure 2](_page_21_Figure_2.jpeg)

The generated settings are saved in the `test_moveit_config` package. Next, edit `joint_limits.yaml` in `/home/yahboom/moveit2_ws/src/test_moveit_config/config`. Change integer values to decimal values without changing the numeric value. The modified file should look like this:

```
# joint_limits.yaml allows the dynamics properties specified in the URDF to be
overwritten or augmented as needed
# For beginners, we downscale velocity and acceleration limits.
# You can always specify higher scaling factors (<= 1.0) in your motion requests.
# Increase the values below to 1.0 to always move at maximum speed.
default_velocity_scaling_factor: 0.1
default_acceleration_scaling_factor: 0.1
```

```
# Specific joint properties can be changed with the keys [max_position,
min_position, max_velocity, max_acceleration]
# Joint limits can be turned off with [has_velocity_limits,
has_acceleration_limits]
joint_limits:
  arm1_Joint:
    has_velocity_limits: true
    max_velocity: 1.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  arm2_Joint:
    has_velocity_limits: true
    max_velocity: 1.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  arm3_Joint:
    has_velocity_limits: true
    max_velocity: 1.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  arm4_Joiint:
    has_velocity_limits: true
    max_velocity: 1.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  arm5_Joint:
    has_velocity_limits: true
    max_velocity: 1.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  llink1_Joint:
    has_velocity_limits: false
    max_velocity: 0.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  llink2_Joint:
    has_velocity_limits: false
    max_velocity: 0.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  llink3_Joint:
    has_velocity_limits: false
    max_velocity: 0.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  rlink1_Joint:
    has_velocity_limits: true
    max_velocity: 1.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  rlink2_Joint:
    has_velocity_limits: false
    max_velocity: 0.0
    has_acceleration_limits: false
    max_acceleration: 0.0
  rlink3_Joint:
    has_velocity_limits: false
    max_velocity: 0.0
```

```
has_acceleration_limits: false
max_acceleration: 0.0
```

Save and exit, then return to the workspace directory and build the package:

```bash
cd moveit2_ws
colcon build --packages-select test_moveit_config
```

After the build completes, refresh the environment by running `source ~/.bashrc`, then start MoveIt2:

```bash
ros2 launch test_moveit_config demo.launch.py
```

When the terminal displays **"You can start planning now!"**, MoveIt2 has started successfully.

![Figure: page 23: figure 6](_page_23_Figure_6.jpeg)

Test [Plan & Execute] with `arm_group` first. Set [Planning Group] to `arm_group`, select [Start State], and then select [Goal State]. In this example, the arm plans from the current `up` pose to the previously configured `init` pose.

![Figure: page 24: figure 0](_page_24_Figure_0.jpeg)

Click [Plan & Execute] on the left to plan and move the arm to `init`.

![Figure: page 24: figure 2](_page_24_Figure_2.jpeg)

After motion planning completes, the result is shown below.

![Figure: page 25: figure 0](_page_25_Figure_0.jpeg)

If planning and execution succeed, the `arm_group` configuration is working. Next, test `grip_group`. Set [Planning Group] to `grip_group`, select [Start State], then select [Goal State].

![Figure: page 25: figure 2](_page_25_Figure_2.jpeg)

Click [Plan & Execute] to plan the gripper motion to the `close` state.

![Figure: page 26: figure 0](_page_26_Figure_0.jpeg)

If the gripper closes successfully, the plan executed correctly.

## 4. Set Up RViz

When running MoveIt2, the robotic arm animation may repeat the planned operation because **Loop Animation** is enabled. To disable it, go to [Display] -> [MotionPlanning] -> [Planned Path] -> [Loop Animation] and clear the checkbox.

In MoveIt2, the orange model represents the target pose. To hide it, go to [MotionPlanning] -> [Query Goal State] and clear the checkbox.

After modifying the RViz settings, press **Ctrl+S** to save them.
