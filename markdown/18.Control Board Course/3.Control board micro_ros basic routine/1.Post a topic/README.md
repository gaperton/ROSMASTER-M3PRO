# Post a topic
Post a topic

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Learn about the STM32-microROS component, access the ROS2 environment, and publish int32

topics.

## 2. Hardware Connection
As shown in the figure below, the STM32 control board integrates the STM32H743 chip and can

use the microros framework program.


Please connect the Type-C data cable to the USB port of the main control board and the USB

Connect port of the STM32 control board.


If you have a USB-to-serial module such as CH340, you can connect to the serial port assistant to

view debugging information.


Since ROS2 requires the Ubuntu environment, it is recommended to install Ubuntu22.04 and

ROS2 environment on the main control board.


![](1.Post-a-topic.pdf-0-0.jpeg)
Note: There are many types of main control boards. Here we take the Jetson Orin series main

control board as an example, with the default factory image burned.

## 3. Core code analysis
The virtual machine path corresponding to the program source code is:


Since microros needs to handle more complex tasks, it is recommended to enable the FREERTOS

function of STM32 and create a new microros processing task.


Since the FreeRTOS component is used, in order to avoid warnings, the system basic clock source

needs to be replaced with a timer, here it is replaced with timer 7.


Since Microros needs to transmit a large amount of data, the baud rate is changed to 2Mbps and

the DMA channels of TX and RX are enabled.


![](1.Post-a-topic.pdf-1-1.jpeg)

![](1.Post-a-topic.pdf-1-2.jpeg)
![](1.Post-a-topic.pdf-2-0.jpeg)

![](1.Post-a-topic.pdf-2-1.jpeg)

Since serial port 1 is used for Microros communication, the debug information printing is changed

to serial port 7. Set the baud rate to 115200, 8-bit data, no parity, and 1 stop bit.


![](1.Post-a-topic.pdf-2-2.jpeg)
For ease of viewing, the debugging serial port of subsequent microros routines is redefined as

serial port 7.


![](1.Post-a-topic.pdf-3-0.jpeg)


Right-click to open the project properties, then click [Settings]->[MCU/MPU GCC Compiler]->

[include paths] to add the microros include directory path, and then click [Apply] to take effect.


Add the microros folder as the project source code path.


Import the microros library path


![](1.Post-a-topic.pdf-3-1.jpeg)

![](1.Post-a-topic.pdf-3-2.jpeg)
![](1.Post-a-topic.pdf-4-0.jpeg)

Link the microros library file to the project. Make sure the name matches the libmicroros.a static

library file name (excluding the prefix and suffix "microros").


Initialize the configuration of microROS. The default value of ros2_domain_id is 30, which is

consistent with the factory image configuration. If the DOMAINID of the ROS2 environment is

changed to another value, the ros2_domain_id variable must also be changed to the same value

for normal communication.


![](1.Post-a-topic.pdf-4-1.jpeg)

![](1.Post-a-topic.pdf-4-2.jpeg)


Set the microros communication serial port and specify it as serial port 1.

```
 int32_t set_microros_serial_transports_with_options(rmw_init_options_t *

 rmw_options)

 {

 int32_t ret = 0;

 ret = rmw_uros_options_set_custom_transport(

```

```
 true,

 (void *) &huart1,

 cubemx_transport_open,

 cubemx_transport_close,

 cubemx_transport_write,

 cubemx_transport_read,

 rmw_options

 );

 return ret;

 }

```

Set the method for requesting memory in the Microros system.


![](1.Post-a-topic.pdf-5-0.jpeg)


Try to connect to the proxy. Only proceed to the next step if the connection is successful. If the

connection to the proxy fails, it will remain in the connecting state. In this case, you need to

enable the proxy script on the control panel to connect.


![](1.Post-a-topic.pdf-5-1.jpeg)


After connecting to the proxy, create the node "YB_Example_Node" where ros2_namespace is

empty by default, indicating the namespace of the node.


![](1.Post-a-topic.pdf-5-2.jpeg)


Create a publisher "int32_publisher" and specify that the publisher's information is of type

std_msgs/msg/Int32.


![](1.Post-a-topic.pdf-6-0.jpeg)


Create a publisher timer with a publishing frequency of 1HZ.


![](1.Post-a-topic.pdf-6-1.jpeg)


Create an executor, where the executor_count parameter is the number of executors controlled

by the executor, which must be greater than or equal to the sum of the number of subscribers

and publishers added to the executor. Add the publisher's timer to the executor.


![](1.Post-a-topic.pdf-6-2.jpeg)


The function of publishing information is executed in the publisher timer callback. In order to

facilitate viewing, the current value of msg.data is printed. After the publishing is completed,

msg.data is automatically increased by 1.


![](1.Post-a-topic.pdf-6-3.jpeg)


The node and topic are processed, and the power LED_MCU indicator is on. Call

rclc_executor_spin_some in the loop to make Microros work normally.


![](1.Post-a-topic.pdf-6-4.jpeg)


If the agent is disconnected or the topic is abnormal, the system will automatically restart the

microcontroller.


![](1.Post-a-topic.pdf-7-0.jpeg)


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


![](1.Post-a-topic.pdf-7-2.jpeg)


![](1.Post-a-topic.pdf-7-1.jpeg)

After the connection is successful, a node and a publisher are created.


![](1.Post-a-topic.pdf-8-0.jpeg)

At this point, you can open another terminal in the virtual machine/computer to view the

/YB_Example_Node node.


Subscribe to data from the /int32_publisher topic


Press Ctrl+C to end the command.


Check the frequency of the /int32_publisher topic. A frequency of about 1 Hz is normal.


![](1.Post-a-topic.pdf-8-3.jpeg)


Press Ctrl+C to end the command.


![](1.Post-a-topic.pdf-9-0.jpeg)
