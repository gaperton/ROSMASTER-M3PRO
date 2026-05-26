# **Update and upgrade operating system**

#### **Update and [upgrade operating](#page-0-0) system**

[Graphical](#page-0-1) interface

Use [APT](#page-0-2)

<span id="page-0-0"></span>Update [software](#page-1-0) list

Update [software](#page-1-1) to the latest version

Search [software](#page-1-2)

View software [information](#page-1-3)

install [software](#page-1-4)

Uninstall [software](#page-2-0)

Use [rpi-update](#page-2-1)

Upgrade [firmware](#page-2-2)

<span id="page-0-1"></span>Roll back to stable [version](#page-2-3)

Keeping the Raspberry Pi up to date can improve the security of the system, but it is not recommended for developers to update randomly!

## **Graphical interface**

Generally, the Raspberry Pi system update prompt will be displayed in the upper right corner of the desktop. You can click the corresponding option to update!

![](_page_0_Picture_16.jpeg)

# **Use APT**

Tools for managing software installation, upgrades and removals.

<span id="page-0-2"></span>The software source of Raspberry Pi is saved in the sources.list file, and the path is located at /etc/apt/sources.list. Do not modify this file unless necessary.

#### **Update software list**

<span id="page-1-1"></span><span id="page-1-0"></span>sudo apt update

### **Update software to the latest version**

<span id="page-1-2"></span>sudo apt full-upgrade

### **Search software**

Command: apt-cache search <package\_name>

Function: Used to search for specific packages in the package repository.

Example: Search the package management system for packages related to "locomotive"

<span id="page-1-3"></span>apt-cache search locomotive

#### **View software information**

Command: apt-cache show <package\_name>

Function: Used to display detailed information of a specific software package.

Example: Display details for a package named "sl"

<span id="page-1-4"></span>apt-cache show sl

#### **install software**

Command: sudo apt install <package\_name>

Function: Used to install specific software packages with administrator privileges.

Example: Use administrator rights (sudo) to install software named "tree"

sudo apt install tree

Command: sudo apt install <package\_name> -y

Function: Automatically confirm the installation of specific software packages with administrator privileges.

Example: Installing a package named "tree" with automatic confirmation (-y) with administrator privileges

sudo apt install tree -y

#### <span id="page-2-0"></span>**Uninstall software**

Command: sudo apt remove <package\_name>

Function: Used to remove specific software packages with administrator privileges.

Example: Uninstalling a package named "tree" with administrator privileges.

```
sudo apt remove tree
```

Command: sudo apt purge <package\_name>

Function: Used to completely clear specific software packages, including configuration files and useless dependencies, with administrator privileges.

Example: Completely clear the package named "tree" with administrator privileges, including configuration files and useless dependencies.

<span id="page-2-1"></span>sudo apt purge tree

# **Use rpi-update**

Used to update startup files and firmware on the Raspberry Pi to provide support for new hardware, features, or fixes.

<span id="page-2-2"></span>If you need to use this method to upgrade the firmware, it is recommended to back up the current system first, because running this command may cause the system to fail to start normally.

#### **Upgrade firmware**

rpi-update needs to be run as root; you will need to reboot after the update is complete.

```
sudo rpi-update
sudo reboot
```

#### **Roll back to stable version**

If the firmware upgrade still does not work properly, you can use the following command to reinstall the stable version of the firmware.

```
sudo apt-get update
sudo apt install --reinstall raspi-firmware
```