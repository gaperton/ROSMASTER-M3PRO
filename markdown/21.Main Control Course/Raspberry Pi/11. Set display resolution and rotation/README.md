# Set display resolution and rotation
**Set display resolution and rotation**

1. Display display settings

### 1.1. System settings adjustment

### 1.2. Modify configuration file adjustment

2. VNC remote display

### 2.1. Graphical interface

### 2.2. Command line


This tutorial mainly introduces the relevant settings of the Raspberry Pi motherboard system

interface display:


1. Connect the resolution and rotation direction settings of the display screen


2. Resolution setting of VNC remote display when no display is connected

## 1. Display display settings
### 1.1. System settings adjustment
Adjust the resolution and rotation direction of the display: applications menu → Preferences →

Screen Configuration


Right-click the corresponding HDMI output interface to set the resolution, rotation direction, etc.


![](Set-display-resolution-and-rotation.pdf-0-1.jpeg)
![](Set-display-resolution-and-rotation.pdf-1-0.jpeg)
### 1.2. Modify configuration file adjustment
Enter the user directory of the Raspberry Pi system, display hidden files, and then enter the .config

folder to modify the wayfire.ini file


Show hidden files


![](Set-display-resolution-and-rotation.pdf-1-2.jpeg)
![](Set-display-resolution-and-rotation.pdf-2-0.jpeg)

Enter the .config folder and modify the wayfire.ini file

## 2. VNC remote display
Adjust the resolution displayed when remote.


![](Set-display-resolution-and-rotation.pdf-2-1.jpeg)

![](Set-display-resolution-and-rotation.pdf-2-2.jpeg)


### 2.1. Graphical interface
Enter Display to modify the VNC remote resolution. After modification, you need to restart the

system and reconnect to VNC!


applications menu → Preferences → Raspberry Pi Configuration → Display

### 2.2. Command line
Use the raspi-config tool to adjust the VNC resolution.


Display Options


![](Set-display-resolution-and-rotation.pdf-3-0.jpeg)

![](Set-display-resolution-and-rotation.pdf-3-1.jpeg)
![](Set-display-resolution-and-rotation.pdf-4-0.jpeg)

VNC Resolution


![](Set-display-resolution-and-rotation.pdf-4-1.jpeg)
![](Set-display-resolution-and-rotation.pdf-5-0.jpeg)
