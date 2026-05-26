# **Enter the Vehicle Docker**

#### **[Enter the Vehicle Docker](#page-0-0)**

- <span id="page-0-0"></span>[1. Course](#page-0-1) Content
- [2. Basic Operations](#page-0-2)
  - 2.1 Start the m3pro [container](#page-0-3)
  - 2.2 Enter the m3pro [container](#page-1-0) terminal
  - 2.3 Shut down the m3pro [container](#page-1-1)

## **1. Course Content**

This section of the course is only for reference by users of **Raspberry Pi 5** mainboard and **Jetson-Nano** mainboard

[!NOTE]

<span id="page-0-3"></span><span id="page-0-2"></span><span id="page-0-1"></span>Raspberry Pi 5 and Jetson Nano cannot directly install the ros2 humble environment due to system version limitations, so the ros2 humble environment is placed in Docker . The host machine does not have a ros2 environment.

## **2. Basic Operations**

### **2.1 Start the m3pro container**

If you need to run the example programs in the tutorial, you must first start the m3pro Docker container

```
bringup_m3pro
```

Display container rosmaster-m3pro Started indicates successful startup

#### **2.2 Enter the m3pro container terminal**

<span id="page-1-0"></span>The commands in subsequent tutorials need to be operated within the container. Open the container terminal command:

```
exec_m3pro
```

If you need to exit the container terminal, press ctrl+D

## **2.3 Shut down the m3pro container**

<span id="page-1-1"></span>When you really need to manually shut down the m3pro container (generally no need to shut down):

```
shut_m3pro
```