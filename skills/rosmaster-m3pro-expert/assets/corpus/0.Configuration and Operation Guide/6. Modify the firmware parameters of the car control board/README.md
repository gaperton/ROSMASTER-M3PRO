# Modify the Firmware Parameters of the Car Control Board

This section explains how to modify the firmware parameters of the car control board.

- Hardware connection
- Modify parameters
- Write the configuration

The robot must already be flashed with the factory firmware before you configure these parameters. The purpose of modifying the control board firmware parameters is to adjust the robot behavior for your own use case. The factory firmware already includes default parameters, and you do not need to change them unless necessary.

The car control board is flashed with the factory firmware before shipment. If you have flashed other firmware, re-flash the factory firmware by following **12. Control Board Course - 1. Development Environment Setup - 4. Burning STM32 Firmware via Serial Port**. The factory firmware is stored in **Appendix - Control Board Factory Firmware**.

This section uses a Jetson Orin series mainboard as the example. The operation is the same for other mainboards.

Note: Before running the configuration script, stop the micro-ROS agent.

## 1. Hardware Connection

Make sure the Type-C **USB Connect** port on the control board is connected to a USB port on the mainboard.

## 2. Modify Parameters

Open a system terminal and edit the `config_robot.py` file in the user directory:

```bash
vim ~/config_robot.py
```

Scroll to the bottom of the file. The main configuration functions are `set_ros_domain_id`, `set_ros_namespace`, `set_motor_pid_parm`, `set_imu_yaw_pid_parm`, `set_ros_scale_line`, `set_ros_scale_angular`, and `set_arm_mid_value`.

To modify a parameter, remove the comment symbol (`#`) before the corresponding function call.

```python
# robot.set_ros_domain_id(30)
# robot.set_ros_namespace("")
# robot.set_motor_pid_parm(0.8, 0.06, 0.5)
# robot.set_imu_yaw_pid_parm(0.6, 0, 0.3)
# robot.set_ros_scale_line(1.0)
# robot.set_ros_scale_angular(1.0)
# arm_mid_value = [2000, 2000, 2000, 2000, 1486, 3100]
# robot.set_arm_mid_value(arm_mid_value)
```

`set_ros_domain_id` sets the robot's ROS domain ID. The value range is 0 to 100. If multiple robots or ROS devices are on the same LAN, assign each one a different ROS domain ID to avoid interference. The `ROS_DOMAIN_ID` value must also match the value in the system terminal's `.bashrc` file so ROS communication works correctly.

`set_ros_namespace` sets the robot's ROS namespace. This is mainly used for multi-robot control on a LAN.

`set_motor_pid_parm` sets the PID parameters for motor speed control.

`set_imu_yaw_pid_parm` sets the PID parameters used by the IMU yaw correction.

`set_ros_scale_line` sets the ROS linear velocity scale.

`set_ros_scale_angular` sets the ROS angular velocity scale.

`set_arm_mid_value` sets the robotic arm center-position offset values. It is mainly used to quickly restore robotic arm calibration values and usually does not need to be modified. Changing this value affects robotic arm calibration. If you need to calibrate the arm, refer to the robotic arm calibration tutorial.

The following example changes the domain ID to `31`.

## 3. Write the Configuration

Note: Before running the configuration script, stop the micro-ROS agent.

Open a system terminal and run the following command to write the configuration:

```bash
python3 ~/config_robot.py
```

After the script finishes, it prints the parameter values read back from the control board.
