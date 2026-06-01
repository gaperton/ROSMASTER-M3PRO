# Control Board Course

This section documents the STM32 control board and its micro-ROS integration. It covers the firmware development environment, basic STM32 peripheral routines, and ROS-facing topic examples for robot control data.

## Development Environment Setup

- [12.1.1 Introduction to the Control Board](./1.Development%20environment%20setup/1.Introduction%20to%20the%20Control%20Board/README.md)
- [12.1.2 Set Up the STM32CubeIDE Environment](./1.Development%20environment%20setup/2.Set%20up%20the%20STM32CUBEIDE%20development%20environment/README.md)
- [12.1.3 Burn STM32 Firmware via SWD](./1.Development%20environment%20setup/3.Burning%20STM32%20firmware%20using%20SWD/README.md)
- [12.1.4 Burn STM32 Firmware via Serial Port](./1.Development%20environment%20setup/4.Burning%20STM32%20firmware%20using%20serial%20port/README.md)
- [12.1.5 Compile the micro-ROS Driver Library](./1.Development%20environment%20setup/5.Compile%20the%20microros%20driver%20library/README.md)
- [12.1.6 Install and Start the micro-ROS Agent](./1.Development%20environment%20setup/6.Install%20and%20start%20the%20microros%20agent/README.md)
- [12.1.7 Import Project](./1.Development%20environment%20setup/7.Import%20Project/README.md)

## STM32 Basic Routines

- [12.2.1 Light Up the LED](./2.Control%20board%20STM32%20basic%20routine/1.Turn%20on%20the%20LED%20light/README.md)
- [12.2.2 Button Functions](./2.Control%20board%20STM32%20basic%20routine/2.Button%20functions/README.md)
- [12.2.3 Drive the Buzzer](./2.Control%20board%20STM32%20basic%20routine/3.Drive%20the%20buzzer/README.md)
- [12.2.4 Serial Communication](./2.Control%20board%20STM32%20basic%20routine/4.Serial%20communication/README.md)
- [12.2.5 Battery Voltage Detection](./2.Control%20board%20STM32%20basic%20routine/5.Battery%20voltage%20detection/README.md)
- [12.2.6 Driving PWM Servos](./2.Control%20board%20STM32%20basic%20routine/6.Driving%20PWM%20Servo/README.md)
- [12.2.7 Drive Motor](./2.Control%20board%20STM32%20basic%20routine/7.Drive%20motor/README.md)
- [12.2.8 Read Motor Encoder Data](./2.Control%20board%20STM32%20basic%20routine/8.Read%20motor%20encoder%20data/README.md)
- [12.2.9 PID Motor Speed Control](./2.Control%20board%20STM32%20basic%20routine/9.PID%20control%20of%20motor%20speed/README.md)
- [12.2.10 Robot Kinematics Analysis Theory](./2.Control%20board%20STM32%20basic%20routine/10.Robot%20kinematics%20analysis%20theory/README.md)
- [12.2.11 Read IMU Data](./2.Control%20board%20STM32%20basic%20routine/11.Read%20IMU%20data/README.md)
- [12.2.12 Read LiDAR Data](./2.Control%20board%20STM32%20basic%20routine/12.Read%20Lidar%20data/README.md)
- [12.2.13 Flash Data Access](./2.Control%20board%20STM32%20basic%20routine/13.Flash%20access%20data/README.md)
- [12.2.14 Driving OLED Displays](./2.Control%20board%20STM32%20basic%20routine/14.Driving%20OLED%20Displays/README.md)
- [12.2.15 Driving RGB Light Strips](./2.Control%20board%20STM32%20basic%20routine/15.Driving%20RGB%20light%20strip/README.md)
- [12.2.16 SBUS Model Aircraft Remote Control](./2.Control%20board%20STM32%20basic%20routine/16.SBUS%20model%20aircraft%20remote%20control/README.md)
- [12.2.17 USB Controller Remote Control](./2.Control%20board%20STM32%20basic%20routine/17.USB%20controller%20remote%20control/README.md)
- [12.2.18 CAN Bus Communication](./2.Control%20board%20STM32%20basic%20routine/18.CAN%20bus%20communication/README.md)

## micro-ROS Basic Routines

- [12.3.1 Publish a Topic](./3.Control%20board%20micro_ros%20basic%20routine/1.Post%20a%20topic/README.md)
- [12.3.2 Subscribe to a Topic](./3.Control%20board%20micro_ros%20basic%20routine/2.Subscribe%20to%20a%20topic/README.md)
- [12.3.3 Multi-Topic Subscription and Publishing](./3.Control%20board%20micro_ros%20basic%20routine/3.Multi-topic%20subscription%20and%20publishing/README.md)
- [12.3.4 Subscribe to the Buzzer Topic](./3.Control%20board%20micro_ros%20basic%20routine/4.Subscribe%20to%20the%20buzzer%20topic/README.md)
- [12.3.5 Subscribe to the Bus Servo Topic](./3.Control%20board%20micro_ros%20basic%20routine/5.Subscribe%20to%20the%20bus%20servo%20topic/README.md)
- [12.3.6 Subscribe to the Speed Control Topic](./3.Control%20board%20micro_ros%20basic%20routine/6.Subscribe%20to%20the%20rate%20control%20topic/README.md)
- [12.3.7 Publish Speed Topic](./3.Control%20board%20micro_ros%20basic%20routine/7.Release%20Speed%20Topic/README.md)
- [12.3.8 Publish IMU Data Topic](./3.Control%20board%20micro_ros%20basic%20routine/8.Publish%20IMU%20data%20topic/README.md)
- [12.3.9 Publish LiDAR Data Topic](./3.Control%20board%20micro_ros%20basic%20routine/9.Publish%20radar%20data%20topic/README.md)
