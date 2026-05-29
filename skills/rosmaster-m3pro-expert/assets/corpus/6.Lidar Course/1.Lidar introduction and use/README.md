# Radar Introduction and Usage

Radar Introduction and Usage

- 1. Radar Introduction
  - 1.1. T-mini Plus Radar
  - 1.2 Radar Characteristics
  - 1.3 Performance Parameters
- 2. Using the Radar

### 1. Radar Introduction

#### 1.1. T-mini Plus Radar

This product uses the T-mini Plus, a 360° 2D lidar. Based on the pulsed Time of Flight (ToF) ranging principle and equipped with relevant optical, electrical, and algorithmic designs, the Tmini Plus achieves high-frequency, high-precision distance measurement. Simultaneously, its mechanical structure rotates 360 degrees, continuously acquiring angle information, enabling 360-degree scanning and ranging, and outputting point cloud data of the scanned environment.

#### 1.2 Radar Characteristics

- 360-degree omnidirectional scanning, adjustable scanning frequency of 6-12 Hz
- High-speed ranging, ranging frequency of 4000 Hz
- Small ranging error, excellent ranging stability
- Strong immunity to ambient light interference
- Class I eye-safe standard

#### 1.3 Performance Parameters

| Item               | Value    | Unit    |
|--------------------|----------|---------|
| Ranging Frequency  | 4000     | Hz      |
| Scanning Frequency | 6 (6-12) | Hz      |
| Ranging Range      | 0.05-12  | m       |
| Scanning Angle     | 0-360    | Degrees |
| Ranging Accuracy   | 20       | mm      |
| Angular Resolution | 0.54     | Degrees |
| Pitch Angle        | 0-1.5    | Degrees |

## 2. Using the Radar

In this product, a ROS expansion board is used to drive two radars. After the car starts the agent, it starts the underlying control node, which publishes to the two radar topics, /scan0 and /scan1. The radar on the left rear of the car is /scan0, and the radar on the right front is /scan1. After the car starts the agent, enter the following command in the terminal to view the radar data, using /scan1 as an example:

A frame of data is shown in the figure above.

- frame_id: indicates the radar's coordinate system name.
- angle_min and angle_max: indicate the minimum and maximum arc angles of the radar scan, which translate to angles from 0 to 360 degrees.
- angle_increment: Indicates the angle increment.
- range_min and range_max: Indicate the minimum and maximum ranges of the radar scan, in meters. Here, the minimum distance is 0.05 meters and the maximum is 12.0 meters.
- ranges: Indicates the range scanned at each angle within the radar scan range, in meters.

You can also use RViz to visualize radar point cloud data. For example, let's view the point cloud data for /scan1 in a virtual machine. First, the virtual machine and the car must be on the same local area network and have the same ROS_DOMAIN_ID. Then, enter the following command in the virtual machine to start RViz:

rviz2

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

After starting RViz, add the /scan1 topic, as shown above, and then modify the [Global Options]- [Fixed] Change the value of [Frame] to laser1_frame. Then, in RViz, you will see the point cloud data for /scan1, as shown below.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

The white portion is the point cloud data for the right front radar.
