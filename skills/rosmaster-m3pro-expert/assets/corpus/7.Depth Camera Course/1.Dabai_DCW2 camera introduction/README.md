# Orbbec Dabai DCW2 Camera Overview

## 1. Content Description

This lesson introduces the Dabai DCW2, an Orbbec depth camera used with this product. It shows how the camera node publishes color images, depth images, infrared images, and point clouds.

This lesson requires terminal commands. Use the terminal that matches your mainboard. This lesson uses Raspberry Pi 5 as the example. Raspberry Pi and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker instructions, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin board users can open a terminal directly on the robot and run the commands from this lesson.

## 2. Camera Introduction

The Dabai DCW2/DW2 depth camera uses binocular structured-light 3D imaging to obtain object depth images. It also uses an RGB camera to capture color images. The camera is suitable for smart products that perform 3D object scanning at a distance of `0.2 m` to `5 m`.

![Picture: page 0: picture 9](_page_0_Picture_9.jpeg)

- IR: Infrared camera
- LDP: Laser Dot Projector
- LDM: Laser Driver Module
- RGB: Color camera

Features of the Dabai DCW2:

- Low-reflectivity object detection: Can identify objects with reflectivity as low as 5%.
- Anti-interference design: Improves electromagnetic compatibility and electrostatic-discharge resistance.
- Balanced field of view: H-FOV: 91 degrees; V-FOV: 62 degrees.
- Energy level switching: Provides two energy modes for different use cases.
- Depth image: Supports up to `640*400` depth resolution.
- Working distance: `0.15 m` to `5 m`.

Depth accuracy: `<1% @ 1 m`

Interface: USB 2.0 Type-C

## 3. ROS Camera Driver

The ROS SDK for the Dabai DCW2 has already been compiled for this product. Start the camera with:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, the camera image appears as shown below.

If the camera does not start, check whether the cable between the camera and the mainboard or hub expansion board is loose.

Use the ROS 2 node tool to view the topics published by the camera node and the services it provides:

```bash
ros2 node info /camera/camera
```

The published topics are shown in the figure below.

The provided services are shown in the figure below.

## 4. Subscribe to Image Topics

### 4.1 Subscribe to Color Images

The camera node publishes the following color image topics:

- `/camera/color/image_raw`: Raw color image topic.
- `/camera/color/image_raw/compressed`: Compressed color image topic.
- `/camera/color/image_raw/compressedDepth`: Depth-compressed color image topic.
- `/camera/color/image_raw/theora`: Color image topic compressed with the Theora encoder.

After the camera starts, run `rqt_image_view` and select the required image topic.

![Figure: page 2: figure 7](_page_2_Figure_7.jpeg)

In the red box shown above, `/camera/color/image_raw` is selected.

### 4.2 Subscribe to Depth Images

The camera node publishes the following depth image topics:

- `/camera/depth/image_raw`: Raw depth image topic.
- `/camera/depth/image_raw/compressed`: Compressed depth image topic.
- `/camera/depth/image_raw/compressedDepth`: Depth-compressed depth image topic.
- `/camera/depth/image_raw/theora`: Depth image topic compressed with the Theora encoder.

Similarly, run `ros2 run rqt_image_view rqt_image_view`, then select the depth image topic to display the depth image.

![Picture: page 3: picture 5](_page_3_Picture_5.jpeg)

The figure above shows the depth image from `/camera/depth/image_raw`.

### 4.3 Subscribe to Infrared Images

The camera node publishes the following infrared image topics:

- `/camera/ir/image_raw`: Raw infrared image topic.
- `/camera/ir/image_raw/compressed`: Compressed infrared image topic.
- `/camera/ir/image_raw/compressedDepth`: Depth-compressed infrared image topic.
- `/camera/ir/image_raw/theora`: Infrared image topic compressed with the Theora encoder.

`rqt_image_view` cannot display infrared images, so use RViz instead. Use the virtual machine to communicate with the robot through distributed ROS 2 communication, then start RViz on the virtual machine and select the plugin for displaying the infrared image. Before doing this, configure distributed communication between the virtual machine and the robot. For details, see **Configuration and Operation Guide - Car Virtual Machine Distributed Communication Settings**.

Open a terminal in the virtual machine and start RViz.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

Follow the arrows in the figure above and click **OK** to complete the selection. The infrared image is displayed as shown below.

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

## 5. Subscribe to Point Cloud Topics

The camera node publishes the following point cloud topics:

- `/camera/depth/points`: 3D depth point cloud.
- `/camera/depth_registered/points`: Registered 3D point cloud topic. The depth data has been aligned with the RGB image, so each depth point corresponds to the correct color point.

Use RViz to display point cloud information. As above, configure distributed communication between the virtual machine and the robot first. Start RViz from the virtual machine terminal, then follow these steps:

![Figure: page 5: figure 1](_page_5_Figure_1.jpeg)

After selecting the display, set the coordinate frame to `camera_link`, as shown below.

![Figure: page 5: figure 3](_page_5_Figure_3.jpeg)

The figure below shows the point cloud from `/camera/depth/points`.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

You can also modify the point cloud display settings.

![Figure: page 6: figure 2](_page_6_Figure_2.jpeg)

Under **Topic**, select `/camera/depth_registered/points` to display the point cloud after aligning the depth and color images. Under **Color Transformer**, select `RGB8` to display the RGB point cloud, as shown below.

![Figure: page 6: figure 4](_page_6_Figure_4.jpeg)
