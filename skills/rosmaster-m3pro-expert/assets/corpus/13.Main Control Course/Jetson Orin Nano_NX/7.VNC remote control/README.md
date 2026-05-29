# VNC remote control

#### VNC remote control

- 1. VNC Viewer
  - 1.1. VNC download
  - 1.2. VNC Installation
- 2. System Settings (Jetson)
  - 2.1. Enable desktop remote
    - 2.1.1. Sharing
    - 2.1.2. Remote Desktop
    - 2.1.3, Media Sharing
    - 2.1.4 Remote Login
  - 2.2, Fixed remote password
    - Passwords and Keys
  - 2.3, Start VNC automatically after booting

Desktop extension manager

3. VNC remote control

Frequently Asked Questions

VNC Remote Display Reconnection

Reconnection Phenomenon

Solution

VNC remote switch uppercase and lowercase

Tutorial to configure the built-in screen sharing of Ubuntu22.04 system for VNC remote control.

Windows computer needs to download and install VNC Viewer in advance and the remote device and the remote device are in the same LAN

## 1. VNC Viewer

### 1.1. VNC download

Official website download address:<https://www.realvnc.com/en/connect/download/viewer/>

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

## 1.2. VNC Installation

Run VNC-Viewer-xxx.exe as an administrator:

![Figure: page 1: figure 3](_page_1_Figure_3.jpeg)

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

![image.png] (1731245794795-9efa7e97-85ea-4c79-b598-f17a6c46ad8b.webp) RealVNC Viewer 7.12.1 Setup **Custom Setup** Select the way you want features to be installed. Click the icons in the tree below to change the way features will be installed. Installs RealVNC Viewer allowing X - Desktop Shortcut you to control other computers remotely. This feature requires 16MB on your hard drive. It has 0 of 1 subfeatures selected. The subfeatures require 0KB on your hard drive. C:\Program Files\RealVNC\VNC Viewer\ Location: Browse... Reset Disk Usage Back Next Cancel RealVNC Viewer 7.12.1 Setup Ready to install RealVNC Viewer 7.12.1 Click Install to begin the installation. Click Back to review or change any of your installation settings. Click Cancel to exit the wizard. Back Install Cancel RealVNC Viewer 7.12.1 Setup X Completed the RealVNC Viewer 7.12.1 Setup Wizard Click the Finish button to exit the Setup Wizard. ### 1.3. Use

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

## 2. System Settings (Jetson)

### 2.1. Enable desktop remote

#### 2.1.1. Sharing

Settings → Sharing

![Picture: page 5: picture 3](_page_5_Picture_3.jpeg)

#### 2.1.2. Remote Desktop

Turn on the remote desktop and enable the traditional VNC protocol (need to check the password required): the access password can be modified by yourself!

![Figure: page 5: figure 6](_page_5_Figure_6.jpeg)

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

#### 2.1.3, Media Sharing

You need to check this option every time you switch networks and turn on the switch of the new network:

![Figure: page 6: figure 3](_page_6_Figure_3.jpeg)

#### 2.1.4 Remote Login

Turn on remote login:

![Picture: page 7: picture 0](_page_7_Picture_0.jpeg)

### 2.2, Fixed remote password

You can perform VNC remote control by completing the above settings, but the access password of the Jetson motherboard will change every time it restarts. The fixed password needs to be operated as follows!

#### Passwords and Keys

Enter Passwords and Keys to set no key:

![Picture: page 7: picture 5](_page_7_Picture_5.jpeg)

Select the default key to modify the password:

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)

Enter the current password:

![Figure: page 8: figure 2](_page_8_Figure_2.jpeg)

Set an empty key: Submit without filling in any content

![Picture: page 9: picture 0](_page_9_Picture_0.jpeg)

![Picture: page 9: picture 1](_page_9_Picture_1.jpeg)

### 2.3, Start VNC automatically after booting

After completing the above operations, the Jetson motherboard cannot be remotely accessed by VNC after the screen is locked. We can follow the following operations to solve the remote problem of locked screen.

#### Desktop extension manager

Install desktop extension manager:

sudo apt install gnome-shell-extension-manager -y

Get the gnome-shell version number:

![Picture: page 10: picture 1](_page_10_Picture_1.jpeg)

Download the plug-in that allows remote access under lock screen according to the version number:

Official website: https://extensions.gnome.org/extension/4338/allow-lockedremote-desktop/

![Figure: page 10: figure 4](_page_10_Figure_4.jpeg)

Install/enable plug-in: Users need to enter the file location to install

gnome-extensions install allowlockedremotedesktopkamens.us.v9.shellextension.zip

sudo gnome-extensions enable allowlockedremotedesktop@kamens.us

![Picture: page 11: picture 1](_page_11_Picture_1.jpeg)

Restart the system: open Extension Manager to enable the corresponding function (find it in the Ubuntu system application)

![Figure: page 11: figure 3](_page_11_Figure_3.jpeg)

![Picture: page 12: picture 0](_page_12_Picture_0.jpeg)

## 3. VNC remote control

VNC Viewer input motherboard IP:

![Figure: page 12: figure 3](_page_12_Figure_3.jpeg)

Fill in the motherboard system password:

![Figure: page 13: figure 0](_page_13_Figure_0.jpeg)

![Picture: page 13: picture 1](_page_13_Picture_1.jpeg)

## Frequently Asked Questions

## VNC Remote Display Reconnection

**Reconnection Phenomenon**

![Picture: page 14: picture 0](_page_14_Picture_0.jpeg)

#### Solution

Modify the options of the corresponding remote device → Specify remote image quality

![Figure: page 14: figure 3](_page_14_Figure_3.jpeg)

![Picture: page 15: picture 0](_page_15_Picture_0.jpeg)

![Picture: page 15: picture 1](_page_15_Picture_1.jpeg)

## VNC remote switch uppercase and lowercase

Enter Settings → Compose Key → Caps Lock: Set to Caps Lock to switch uppercase and lowercase input

![Figure: page 16: figure 0](_page_16_Figure_0.jpeg)
