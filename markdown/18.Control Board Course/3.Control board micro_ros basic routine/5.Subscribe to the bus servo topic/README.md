# Subscribe to the Bus Servo Topic
Subscribe to the Bus Servo Topic

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Learn about the STM32-microROS component, access the ROS2 environment, and subscribe to

topics related to controlling the servo angle on the bus.

## 2. Hardware Connection
As shown in the figure below, the STM32 control board integrates three bus servo interfaces. You

need to prepare additional bus servos and connect them to see the effect.


Use a Type-C data cable to connect the USB port of the main control board and the USB Connect

port of the STM32 control board.


Since the bus servo has high voltage and current requirements, it must be powered by a battery.


Note: There are many types of main control boards. Here we take the Jetson Orin series main

control board as an example, with the default factory image burned.


![](5.Subscribe-to-the-bus-servo-topic.pdf-0-0.jpeg)
Note: There are three bus servo interfaces (S3/S4/S5), of which S3 is a 6.8V bus servo interface,

and S4 and S5 are 12V bus servo interfaces. Since the M3PRO's robotic arm bus servo is 6.8V, we

will use S3 as an example.

## 3. Core code analysis
The virtual machine path corresponding to the program source code is:


Create a subscriber arm_joint with the message type ArmJoint.


![](5.Subscribe-to-the-bus-servo-topic.pdf-1-1.jpeg)


The message type arm_msgs/msg/ArmJoint is a custom type and has the following format:


![](5.Subscribe-to-the-bus-servo-topic.pdf-1-2.jpeg)


Add subscriber arm_joint to the executor.


![](5.Subscribe-to-the-bus-servo-topic.pdf-1-3.jpeg)


The bus servo receives data callback function to control the bus servo robotic arm.


![](5.Subscribe-to-the-bus-servo-topic.pdf-1-4.jpeg)


Call rclc_executor_spin_some in a loop to make microros work properly.


![](5.Subscribe-to-the-bus-servo-topic.pdf-2-0.jpeg)


## 4. Compile, download and burn firmware
Select the project to be compiled in the file management interface of STM32CUBEIDE and click the

compile button on the toolbar to start compiling.


If there are no errors or warnings, the compilation is complete.


Since the Type-C communication serial port used by the microros agent is multiplexed with the

burning serial port, it is recommended to use the STlink tool to burn the firmware.


If you are using the serial port to burn, you need to first plug the Type-C data cable into the

computer's USB port, enter the serial port download mode, burn the firmware, and then plug it

back into the USB port of the main control board.

## 5. Experimental Results
The MCU_LED light flashes every 200 milliseconds.


If the proxy is not enabled on the main control board terminal, enter the following command to

enable it. If the proxy is already enabled, disable it and then re-enable it.


![](5.Subscribe-to-the-bus-servo-topic.pdf-2-2.jpeg)


![](5.Subscribe-to-the-bus-servo-topic.pdf-2-1.jpeg)

After the connection is successful, a node and two subscribers are created.


![](5.Subscribe-to-the-bus-servo-topic.pdf-3-0.jpeg)

Open another terminal and view the /YB_Example_Node node.


Note: Before running commands to control the robotic arm, please confirm the current position

of the robotic arm to avoid it hitting other objects during movement.


Publish data to the /arm_joint topic to control the bus servo with ID=1 to rotate to 60 degrees.

Observe that servo No. 1 slowly rotates to the 60-degree position.


Publish data to the /arm_joint topic to control the bus servo with ID=1 to rotate to 120 degrees.

Observe that servo No. 1 slowly rotates to the 120-degree position.
