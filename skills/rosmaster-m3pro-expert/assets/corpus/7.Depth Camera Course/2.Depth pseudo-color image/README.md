# Depth Pseudocolor Visualization

## 1. Content Description

This lesson subscribes to the depth image topic and uses OpenCV image processing to convert a grayscale depth image into a pseudocolor image.

This lesson requires terminal commands. Use the terminal that matches your mainboard. This lesson uses Raspberry Pi 5 as the example. Raspberry Pi and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker instructions, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin board users can open a terminal directly on the robot and run the commands from this lesson.

## 2. Program Startup

Start the camera:

```bash
ros2 launch orbbec_camera dabai_dcw2.launch.py
```

After the camera starts successfully, open another terminal and start the depth pseudocolor conversion program:

```bash
ros2 run yahboom_M3Pro_DepthCam GetDepthColor
```

After startup, different colors represent different depth values.

## 3. Core Code Analysis

Program code path for Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/yahboom_M3Pro_DepthCam/yahboom_M3Pro_DepthCam/GetDepth Color.py
```

Program code path for Orin boards:

```text
/home/jetson/yahboomcar_ws/yahboom_M3Pro_DepthCam/yahboom_M3Pro_DepthCam/GetD epthColor.py
```

Import the required libraries:

```python
from cv_bridge import CvBridge
import cv2
from rclpy.node import Node
import rclpy
from sensor_msgs.msg import Image
```

Define the depth image decoding formats:

```python
encoding = ['16UC1', '32FC1']
```

Create the subscriber and subscribe to the depth image topic:

```python
self.sub_depth =
self.create_subscription(Image,"/camera/depth/image_raw",self.get_DepthImgCallBa
ck,100)
```

Create `self.depth_bridge` to convert ROS image messages into an image format that OpenCV can process:

```python
self.depth_bridge = CvBridge()
```

Convert the ROS image message into an image:

```python
depth_image = self.depth_bridge.imgmsg_to_cv2(depth_frame, encoding[1])
```

Call `cv2.applyColorMap` to convert the depth map into a pseudocolor image:

```python
depth_to_color_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image,
alpha=1.0), cv2.COLORMAP_JET)
```

`cv2.convertScaleAbs` performs a linear transformation on the image data and converts it to 8-bit unsigned integer (`uint8`) format. The scaling factor controls the conversion scale.

`cv2.applyColorMap` converts a single-channel grayscale image into a pseudocolor image, making the depth information easier to visualize. The first argument is a single-channel 8-bit or floating-point image, and the second argument is the color map. Common options include:

```python
cv2.COLORMAP_AUTUMN # red -orange-yellow
cv2.COLORMAP_BONE #Black-white (grayscale with a bluish tint )
cv2.COLORMAP_HSV #HSV color space
cv2.COLORMAP_JET #Blue- cyan -yellow-red (classic heat map )
cv2.COLORMAP_WINTER # blue -green
cv2.COLORMAP_RAINBOW #Rainbow color (red-purple )
cv2.COLORMAP_OCEAN #dark blue-light blue
cv2.COLORMAP_SUMMER # green -yellow
cv2.COLORMAP_SPRING # Magenta - yellow
```

```python
cv2.COLORMAP_COOL #cyan - magenta
cv2.COLORMAP_HSV #HSV color space cycle
cv2.COLORMAP_PINK #pink tone
cv2.COLORMAP_PARULA #MATLAB Parula style
cv2.COLORMAP_VIRIDIS #Modern scientific color scale (green-purple)
cv2.COLORMAP_INFERNO # Black -Red-Yellow-White (high contrast )
cv2.COLORMAP_PLASMA # purple -red-yellow
cv2.COLORMAP_MAGMA # black -red-white
cv2.COLORMAP_TWILIGHT # blue -pink - white gradient
```
