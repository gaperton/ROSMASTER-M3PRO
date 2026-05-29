# Set display resolution and rotation

## 1. Display display settings

### 1.1. System settings adjustment

Adjust the resolution and rotation direction of the display: applications menu -> Preferences -> Screen Configuration

![Picture: page 0: picture 15](_page_0_Picture_15.jpeg)

Right-click the corresponding HDMI output interface to set the resolution, rotation direction, etc.

![Picture: page 1: picture 0](_page_1_Picture_0.jpeg)

### 1.2. Modify configuration file adjustment

Enter the user directory of the Raspberry Pi system, display hidden files, and then enter the.config folder to modify the wayfire.ini file

This method can customize the display resolution, position and rotation direction

Show hidden files

![Picture: page 1: picture 5](_page_1_Picture_5.jpeg)

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

Enter the.config folder and modify the wayfire.ini file

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

## 2. VNC remote display

Adjust the resolution displayed when remote.

When connecting to a monitor, adjusting the resolution of the VNC remote will not affect it. The displayed resolution will still be based on the resolution set by the monitor!

### 2.1. Graphical interface

Enter Display to modify the VNC remote resolution. After modification, you need to restart the system and reconnect to VNC!

applications menu -> Preferences -> Raspberry Pi Configuration -> Display

![Picture: page 3: picture 3](_page_3_Picture_3.jpeg)

### 2.2. Command line

Use the raspi-config tool to adjust the VNC resolution.

Display Options

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

VNC Resolution

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

| | R | aspberry | Pi Software | Configuration | Tool | (raspi-config) | |
|---|---|----------|-------------------|---------------|-------------------------------------------|----------------|--|

| | | | | 640x480 | | | |
| | | | | 720x480 | | | |
| | | | | 800x600 | | | |
| | | | | 1024x768 | | | |
| | | | | 1280x720 | | | |
| | | | | 1280x1024 | | | |
| | | | | 1600x1200 | | | |
| | | | | 1920x1080 | | | |


|   |   |          |                   |               |                                           |                |  |
e<> | Back>          |  |
| 1 |   |          |                   |               |                                           |                |  |
| L |   |          |                   |               |                                           |                |  |
