# **VNC remote control**

#### **[VNC remote control](#page-0-0)**

- <span id="page-0-0"></span>1. VNC [Viewer](#page-0-1)
  - 1.1. VNC [download](#page-0-2)
  - 1.2. VNC [Installation](#page-1-0)
- [2. System Settings](#page-4-0) (Jetson)
  - 2.1. Enable [desktop remote](#page-5-0)
    - [2.1.1. Sharing](#page-5-1)
    - [2.1.2. Remote](#page-5-2) Desktop
    - 2.1.3, Media [Sharing](#page-6-0)
    - 2.1.4 [Remote](#page-6-1) Login
  - 2.2, [Fixed remote](#page-7-0) password
    - [Passwords](#page-7-1) and Keys
  - 2.3, Start VNC [automatically](#page-9-0) after booting

[Desktop extension](#page-9-1) manager

3. VNC [remote](#page-12-0) control

Frequently [Asked Questions](#page-13-0)

VNC Remote Display [Reconnection](#page-13-1)

[Reconnection](#page-13-2) Phenomenon

<span id="page-0-2"></span><span id="page-0-1"></span>[Solution](#page-14-0)

VNC remote switch uppercase [and lowercase](#page-15-0)

Tutorial to configure the built-in screen sharing of Ubuntu22.04 system for VNC remote control.

Windows computer needs to download and install VNC Viewer in advance and the remote device and the remote device are in the same LAN

## **1. VNC Viewer**

### **1.1. VNC download**

Official website download address:<https://www.realvnc.com/en/connect/download/viewer/>

![](_page_1_Figure_0.jpeg)

## <span id="page-1-0"></span>**1.2. VNC Installation**

Run VNC-Viewer-xxx.exe as an administrator:

![](_page_1_Figure_3.jpeg)

![](_page_2_Figure_0.jpeg)

![image.png] (1731245794795-9efa7e97-85ea-4c79-b598-f17a6c46ad8b.webp) RealVNC Viewer 7.12.1 Setup **Custom Setup** Select the way you want features to be installed. Click the icons in the tree below to change the way features will be installed. Installs RealVNC Viewer allowing X - Desktop Shortcut you to control other computers remotely. This feature requires 16MB on your hard drive. It has 0 of 1 subfeatures selected. The subfeatures require 0KB on your hard drive. C:\Program Files\RealVNC\VNC Viewer\ Location: Browse... Reset Disk Usage Back Next Cancel RealVNC Viewer 7.12.1 Setup Ready to install RealVNC Viewer 7.12.1 Click Install to begin the installation. Click Back to review or change any of your installation settings. Click Cancel to exit the wizard. Back Install Cancel RealVNC Viewer 7.12.1 Setup X Completed the RealVNC Viewer 7.12.1 Setup Wizard Click the Finish button to exit the Setup Wizard. ### 1.3. Use

![](_page_4_Figure_0.jpeg)

## <span id="page-4-0"></span>**2. System Settings (Jetson)**

### <span id="page-5-0"></span>**2.1. Enable desktop remote**

#### <span id="page-5-1"></span>**2.1.1. Sharing**

Settings → Sharing

![](_page_5_Picture_3.jpeg)

#### <span id="page-5-2"></span>**2.1.2. Remote Desktop**

Turn on the remote desktop and enable the traditional VNC protocol (need to check the password required): the access password can be modified by yourself!

![](_page_5_Figure_6.jpeg)

![](_page_6_Figure_0.jpeg)

#### <span id="page-6-0"></span>**2.1.3, Media Sharing**

You need to check this option every time you switch networks and turn on the switch of the new network:

![](_page_6_Figure_3.jpeg)

#### <span id="page-6-1"></span>**2.1.4 Remote Login**

Turn on remote login:

![](_page_7_Picture_0.jpeg)

### <span id="page-7-0"></span>**2.2, Fixed remote password**

You can perform VNC remote control by completing the above settings, but the access password of the Jetson motherboard will change every time it restarts. The fixed password needs to be operated as follows!

#### <span id="page-7-1"></span>**Passwords and Keys**

Enter Passwords and Keys to set no key:

![](_page_7_Picture_5.jpeg)

Select the default key to modify the password:

![](_page_8_Figure_0.jpeg)

Enter the current password:

![](_page_8_Figure_2.jpeg)

Set an empty key: Submit without filling in any content

![](_page_9_Picture_0.jpeg)

![](_page_9_Picture_1.jpeg)

### <span id="page-9-0"></span>**2.3, Start VNC automatically after booting**

After completing the above operations, the Jetson motherboard cannot be remotely accessed by VNC after the screen is locked. We can follow the following operations to solve the remote problem of locked screen.

#### **Desktop extension manager**

Install desktop extension manager:

<span id="page-9-1"></span>sudo apt install gnome-shell-extension-manager -y

Get the gnome-shell version number:

![](_page_10_Picture_1.jpeg)

Download the plug-in that allows remote access under lock screen according to the version number:

Official website: https://extensions.gnome.org/extension/4338/allow-lockedremote-desktop/

![](_page_10_Figure_4.jpeg)

Install/enable plug-in: Users need to enter the file location to install

gnome-extensions install allowlockedremotedesktopkamens.us.v9.shellextension.zip

sudo gnome-extensions enable allowlockedremotedesktop@kamens.us

![](_page_11_Picture_1.jpeg)

Restart the system: open Extension Manager to enable the corresponding function (find it in the Ubuntu system application)

![](_page_11_Figure_3.jpeg)

![](_page_12_Picture_0.jpeg)

## <span id="page-12-0"></span>**3. VNC remote control**

VNC Viewer input motherboard IP:

![](_page_12_Figure_3.jpeg)

Fill in the motherboard system password:

![](_page_13_Figure_0.jpeg)

![](_page_13_Picture_1.jpeg)

## <span id="page-13-0"></span>**Frequently Asked Questions**

## <span id="page-13-1"></span>**VNC Remote Display Reconnection**

<span id="page-13-2"></span>**Reconnection Phenomenon**

![](_page_14_Picture_0.jpeg)

#### <span id="page-14-0"></span>**Solution**

Modify the options of the corresponding remote device → Specify remote image quality

![](_page_14_Figure_3.jpeg)

![](_page_15_Picture_0.jpeg)

![](_page_15_Picture_1.jpeg)

## <span id="page-15-0"></span>**VNC remote switch uppercase and lowercase**

Enter Settings → Compose Key → Caps Lock: Set to Caps Lock to switch uppercase and lowercase input

![](_page_16_Figure_0.jpeg)