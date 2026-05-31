# Enter the Robot Docker Container

## 1. Course Content

This section is for users of the **Raspberry Pi 5** mainboard and **Jetson Nano** mainboard.

> [!NOTE]
> Raspberry Pi 5 and Jetson Nano cannot install ROS 2 Humble directly because of system-version limitations. For these boards, ROS 2 Humble runs inside Docker. The host system itself does not include a ROS 2 environment.

## 2. Basic Operations

### 2.1 Start the `m3pro` Container

Before running the example programs in the tutorial, start the `m3pro` Docker container:

```bash
bringup_m3pro
```

If the terminal displays `container rosmaster-m3pro Started`, the container started successfully.

### 2.2 Enter the `m3pro` Container Terminal

Commands in later tutorials must be run inside the container. To open a terminal inside the container, run:

```bash
exec_m3pro
```

To exit the container terminal, press Ctrl+D.

### 2.3 Shut Down the `m3pro` Container

Usually, you do not need to shut down the container manually. If you do need to stop it, run:

```bash
shut_m3pro
```
