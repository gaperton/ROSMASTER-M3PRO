# Publish IMU data topic
Publish IMU data topic

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Learn about STM32-microROS components, access the ROS2 environment, and publish IMU data

topics.

## 2. Hardware Connection
As shown in the figure below, the STM32 control board integrates a nine-axis IMU attitude sensor.


Use a Type-C data cable to connect the USB port of the main control board and the USB Connect

port of the STM32 control board.


Note: There are many types of main control boards. Here we take the Jetson Orin series main

control board as an example, with the default factory image burned.


![](8.Publish-IMU-data-topic.pdf-0-0.jpeg)
## 3. Core code analysis
The virtual machine path corresponding to the program source code is:


Initialize imu topic information.


![](8.Publish-IMU-data-topic.pdf-1-1.jpeg)


Create the node "imu_publisher". The ROS_NAMESPACE is empty by default and can be modified

in the IDF configuration tool according to actual needs.


![](8.Publish-IMU-data-topic.pdf-1-2.jpeg)


Create the publisher "imu/data_raw" and specify the publisher's message type as

sensor_msgs/msg/Imu.


![](8.Publish-IMU-data-topic.pdf-1-3.jpeg)


To create the publisher "imu/mag", you need to specify that the publisher's information is of the

sensor_msgs/msg/MagneticField type.


![](8.Publish-IMU-data-topic.pdf-1-4.jpeg)


Create a publisher timer with a publishing frequency of 25HZ.


![](8.Publish-IMU-data-topic.pdf-2-0.jpeg)


Add the publisher's timer to the executor


Update the imu information data regularly.


![](8.Publish-IMU-data-topic.pdf-2-2.jpeg)


Update mag information data regularly.


![](8.Publish-IMU-data-topic.pdf-2-3.jpeg)


The main function of the IMU timer callback function is to send the IMU data.

```
 void imu_publisher_callback(rcl_timer_t *timer, int64_t last_call_time)

 {

 RCLC_UNUSED(last_call_time);

 if (timer != NULL)

 {

 publish_imu_data();

 publish_mag_data();

 }

 }

 void publish_imu_data(void)

 {

 imu_msg_update();

 timespec_t time_stamp = get_ros2_timestamp();

```

```
 imu_msg.header.stamp.sec = time_stamp.tv_sec;

 imu_msg.header.stamp.nanosec = time_stamp.tv_nsec;

 RCSOFTCHECK(rcl_publish(&imu_publisher, &imu_msg, NULL));

 }

 void publish_mag_data(void)

 {

 mag_msg_update();

 timespec_t time_stamp = get_ros2_timestamp();

 mag_msg.header.stamp.sec = time_stamp.tv_sec;

 mag_msg.header.stamp.nanosec = time_stamp.tv_nsec;

 RCSOFTCHECK(rcl_publish(&mag_publisher, &mag_msg, NULL));

 }

```

Call rclc_executor_spin_some in a loop to make microros work properly.


![](8.Publish-IMU-data-topic.pdf-3-0.jpeg)
## 4. Compile, download and burn firmware
Select the project to be compiled in the file management interface of STM32CUBEIDE and click the

compile button on the toolbar to start compiling.


If there are no errors or warnings, the compilation is complete.


Since the Type-C communication serial port used by the microros agent is multiplexed with the

burning serial port, it is recommended to use the STlink tool to burn the firmware.


If you are using the serial port to burn, you need to first plug the Type-C data cable into the

computer's USB port, enter the serial port download mode, burn the firmware, and then plug it

back into the USB port of the main control board.


![](8.Publish-IMU-data-topic.pdf-3-1.jpeg)

![](8.Publish-IMU-data-topic.pdf-3-2.jpeg)
## 5. Experimental Results
The MCU_LED light flashes every 200 milliseconds.


If the proxy is not enabled on the main control board terminal, enter the following command to

enable it. If the proxy is already enabled, disable it and then re-enable it.


After the connection is successful, a node and a publisher are created.


Open another terminal and view the /YB_Example_Node node.


Subscribe to data from the /imu/data_raw topic


![](8.Publish-IMU-data-topic.pdf-4-1.jpeg)


Press Ctrl+C to end the command.


Check the frequency of the /imu/data_raw topic. A frequency of about 25 Hz is normal.


![](8.Publish-IMU-data-topic.pdf-4-4.jpeg)
Press Ctrl+C to end the command.


Subscribe to data on the /imu/mag topic


![](8.Publish-IMU-data-topic.pdf-5-1.jpeg)


Press Ctrl+C to end the command.


Check the frequency of the /imu/mag topic. A frequency of about 25 Hz is normal.


![](8.Publish-IMU-data-topic.pdf-5-3.jpeg)


Press Ctrl+C to end the command.


![](8.Publish-IMU-data-topic.pdf-5-5.jpeg)
