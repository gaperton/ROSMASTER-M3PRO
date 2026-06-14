# remote access
**remote access**

1. Preliminary preparation

### 1.1. Enable SSH and VNC

Graphical interface

Command Line

### 1.2. Obtain IP

Graphical interface

2. SSH remote control

3. VNC remote login


We often use SSH and VNC tools to remotely control the Raspberry Pi system.
## 1. Preliminary preparation
Before performing SSH or VNC remote login, you need to enable SSH and VNC functions in the

Raspberry Pi system settings or use the raspi-config tool.

### 1.1. Enable SSH and VNC
**Graphical interface**


Enable SSH and VNC: applications menu → Preferences → Raspberry Pi Configuration


![](remote-access.pdf-0-0.jpeg)
![](remote-access.pdf-1-0.jpeg)

**Command Line**


Use the raspi-config tool to enable SSH and VNC functions: Interface Options → SSH/VNC: enable


![](remote-access.pdf-1-1.jpeg)

![](remote-access.pdf-1-2.jpeg)
![](remote-access.pdf-2-0.jpeg)

![](remote-access.pdf-2-1.jpeg)

![](remote-access.pdf-2-2.jpeg)


### 1.2. Obtain IP
After enabling SSH and VNC functions, you can remotely control the Raspberry Pi based on its IP!


**Graphical interface**


After the system is connected to WiFi, hover the mouse on the WiFi icon to see the corresponding

IP address.


![](remote-access.pdf-3-0.jpeg)

Use the command to view the IP address: hostname -I or ifconfig

## 2. SSH remote control
After obtaining the IP address of the Raspberry Pi motherboard, you can perform SSH remote

login on the terminal based on the user name and password of the Raspberry Pi system.


SSH remote login command: ssh username@IP address


![](remote-access.pdf-3-1.jpeg)

![](remote-access.pdf-3-2.jpeg)


![](remote-access.pdf-4-0.jpeg)
## 3. VNC remote login
After obtaining the IP address of the Raspberry Pi motherboard, you can use the RealVNC Viewer

software to log in remotely.


![](remote-access.pdf-4-2.jpeg)
![](remote-access.pdf-5-0.jpeg)

After successful remote login, the Raspberry Pi system desktop will be displayed!


![](remote-access.pdf-5-1.jpeg)
