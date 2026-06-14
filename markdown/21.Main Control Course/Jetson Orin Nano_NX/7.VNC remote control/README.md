# VNC remote control
**VNC remote control**

1. VNC Viewer

### 1.1. VNC download

### 1.2. VNC Installation

2. System Settings (Jetson)

### 2.1. Enable desktop remote

#### 2.1.1. Sharing

#### 2.1.2. Remote Desktop

#### 2.1.3, Media Sharing

#### 2.1.4 Remote Login

### 2.2, Fixed remote password

Passwords and Keys

### 2.3, Start VNC automatically after booting

Desktop extension manager

3. VNC remote control

Frequently Asked Questions

VNC Remote Display Reconnection

Reconnection Phenomenon

Solution

VNC remote switch uppercase and lowercase


Tutorial to configure the built-in screen sharing of Ubuntu22.04 system for VNC remote control.

## 1. VNC Viewer
### 1.1. VNC download
Official website download address: [https://www.realvnc.com/en/connect/download/viewer/](https://www.realvnc.com/en/connect/download/viewer/)


![](VNC-remote-control.pdf-1-0.jpeg)
### 1.2. VNC Installation
Run VNC-Viewer-xxx.exe as an administrator:


![](VNC-remote-control.pdf-1-1.jpeg)

![](VNC-remote-control.pdf-1-2.jpeg)
![](VNC-remote-control.pdf-2-0.jpeg)
![image.png] (1731245794795-9efa7e97-85ea-4c79-b598-f17a6c46ad8b.webp)


### 1.3. Use


![](VNC-remote-control.pdf-3-0.jpeg)

![](VNC-remote-control.pdf-3-1.jpeg)

![](VNC-remote-control.pdf-3-2.jpeg)
![](VNC-remote-control.pdf-4-0.jpeg)

VNC

## 2. System Settings (Jetson)
![](VNC-remote-control.pdf-4-1.jpeg)

![](VNC-remote-control.pdf-4-2.jpeg)
### 2.1. Enable desktop remote
#### 2.1.1. Sharing
Settings → Sharing

#### 2.1.2. Remote Desktop
Turn on the remote desktop and enable the traditional VNC protocol (need to check the password

required): the access password can be modified by yourself!


![](VNC-remote-control.pdf-5-0.jpeg)

![](VNC-remote-control.pdf-5-1.jpeg)
![](VNC-remote-control.pdf-6-0.jpeg)
#### 2.1.3, Media Sharing
You need to check this option every time you switch networks and turn on the switch of the new

network:

#### 2.1.4 Remote Login
Turn on remote login:


![](VNC-remote-control.pdf-6-1.jpeg)
![](VNC-remote-control.pdf-7-0.jpeg)
### 2.2, Fixed remote password
You can perform VNC remote control by completing the above settings, but the access password

of the Jetson motherboard will change every time it restarts. The fixed password needs to be

operated as follows!


**Passwords and Keys**


Enter Passwords and Keys to set no key:


Select the default key to modify the password:


![](VNC-remote-control.pdf-7-1.jpeg)
![](VNC-remote-control.pdf-8-0.jpeg)

Enter the current password:


Set an empty key: Submit without filling in any content


![](VNC-remote-control.pdf-8-1.jpeg)
![](VNC-remote-control.pdf-9-0.jpeg)

![](VNC-remote-control.pdf-9-1.jpeg)
### 2.3, Start VNC automatically after booting
After completing the above operations, the Jetson motherboard cannot be remotely accessed by

VNC after the screen is locked. We can follow the following operations to solve the remote

problem of locked screen.


**Desktop extension manager**


Install desktop extension manager:


Get the gnome-shell version number:


![](VNC-remote-control.pdf-10-1.jpeg)

Download the plug-in that allows remote access under lock screen according to the version

number:


Install/enable plug-in: Users need to enter the file location to install


![](VNC-remote-control.pdf-10-3.jpeg)


![](VNC-remote-control.pdf-11-1.jpeg)

Restart the system: open Extension Manager to enable the corresponding function (find it in the

Ubuntu system application)


![](VNC-remote-control.pdf-11-2.jpeg)
![](VNC-remote-control.pdf-12-0.jpeg)
## 3. VNC remote control
VNC Viewer input motherboard IP:


Fill in the motherboard system password:


![](VNC-remote-control.pdf-12-1.jpeg)
![](VNC-remote-control.pdf-13-0.jpeg)

![](VNC-remote-control.pdf-13-1.jpeg)

**Frequently Asked Questions**

**VNC Remote Display Reconnection**


**Reconnection Phenomenon**


![](VNC-remote-control.pdf-14-0.jpeg)

**Solution**


Modify the options of the corresponding remote device → Specify remote image quality


![](VNC-remote-control.pdf-14-1.jpeg)
![](VNC-remote-control.pdf-15-0.jpeg)

![](VNC-remote-control.pdf-15-1.jpeg)

**VNC remote switch uppercase and lowercase**


Enter Settings → Compose Key → Caps Lock: Set to Caps Lock to switch uppercase and lowercase

input


![](VNC-remote-control.pdf-16-0.jpeg)
