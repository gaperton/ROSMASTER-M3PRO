# Entering the Car Docker

**Entering the Car Docker**

1. Course Content

2. Basic Operations

### 2.1 Launching the m3pro Container

### 2.2 Accessing the m3pro Container Terminal

### 2.4 Issues Encountered After Entering the Docker Container on Jetson Nano Versions of M3Pro, A1,

M1, and M3 Robots

## 1. Course Content


This lesson is only for users with **Raspberry Pi 5** and **Jetson-Nano** motherboards.


[!NOTE]


Because the Raspberry Pi 5 and Jetson Nano system versions cannot directly install the


the host machine does not have a ROS2 environment.


After entering Docker with the Jetson Nano version, you need to open an rviz2 or rqt

window before running the AI large-scale multimodal vision tutorial.
## 2. Basic Operations
### 2.1 Launching the m3pro Container


If you wish to run the example programs featured in this tutorial, you must first launch the


[!WARNING]


graphical interface; otherwise, visualization windows (such as RViz) may fail to display

correctly.

Regarding external peripherals—such as game controllers, AI voice modules, and other

hardware devices—the Docker container will only load devices that were present at the

moment the container was launched. If a hardware device is plugged in _after_ the

container has already started, it will not be automatically synchronized in real-time

within the container. To recognize newly connected devices, you must stop and then

restart the container.


The message `container rosmaster` - `m3pro Started` indicates that the launch was successful.


![](C:/rosmaster_pymupdf__5t73q6f/4.-Enter-the-Docker-(Jetson-Nano-and-Raspberry-Pi-5-users,-see-here).pdf-1-0.jpeg)
### 2.2 Accessing the m3pro Container Terminal

The commands featured in the subsequent tutorials must be executed _inside_ the container.

To open the container terminal, use the following command:


![](C:/rosmaster_pymupdf__5t73q6f/4.-Enter-the-Docker-(Jetson-Nano-and-Raspberry-Pi-5-users,-see-here).pdf-1-2.jpeg)


[!IMPORTANT]


**Important**


Unless explicitly stated otherwise, users of the Raspberry Pi and Jetson Nano platforms

should assume that all subsequent program execution commands are to be performed

_within_ the **m3pro** container. You must first launch the container and then enter the

commands within the container terminal. This requirement will not be reiterated in

subsequent lessons. ### 2.3 Shutting Down the m3pro Container


If you genuinely no longer require the m3pro container and need to shut it down manually

(typically, manual shutdown is not necessary):


![](C:/rosmaster_pymupdf__5t73q6f/4.-Enter-the-Docker-(Jetson-Nano-and-Raspberry-Pi-5-users,-see-here).pdf-1-4.jpeg)


![](C:/rosmaster_pymupdf__5t73q6f/4.-Enter-the-Docker-(Jetson-Nano-and-Raspberry-Pi-5-users,-see-here).pdf-1-6.jpeg)
### 2.4 Issues Encountered After Entering the Docker Container

**on Jetson Nano Versions of M3Pro, A1, M1, and M3 Robots**


On Jetson Nano versions, attempting to run the AI Large Model Vision examples immediately

after entering the Docker container results in a "Permission Denied" error, as shown in the

figure below.


or `rqt` . After opening and then closing this window, you may proceed to run the AI Large

Model Vision examples, as illustrated in the figure below.


![](C:/rosmaster_pymupdf__5t73q6f/4.-Enter-the-Docker-(Jetson-Nano-and-Raspberry-Pi-5-users,-see-here).pdf-2-0.jpeg)

![](C:/rosmaster_pymupdf__5t73q6f/4.-Enter-the-Docker-(Jetson-Nano-and-Raspberry-Pi-5-users,-see-here).pdf-2-2.jpeg)
