# Restore the factory image system
**Restore the factory image system**

1. Format the SSD

### 1.1. Download DiskGenius

### 1.1. Use DiskGenius

#### 1.1.1, Delete partition

#### 1.1.2. Create a new partition

2. Restore the factory image

### 2.1. Install Win32DiskImager

### 2.2. Use Win32DiskImager

3. Description

## 1. Format the SSD
Before restoring the factory image, you need to format the SSD into exFAT format.

### 1.1. Download DiskGenius
Download URL: [https://www.diskgenius.com/](https://www.diskgenius.com/)


Double-click the exe file you just downloaded to install DiskGenius. Follow the prompts to install

the software on the Windows computer. After opening the software, it will be as shown below.


![](2.-Restore-the-factory-image-system.pdf-0-0.jpeg)
![](2.-Restore-the-factory-image-system.pdf-1-0.jpeg)
### 1.1. Use DiskGenius
#### 1.1.1, Delete partition
Deleting a partition will clear the disk data. Please confirm whether the drive letter is the disk that

needs to be formatted before confirming the operation: you can judge based on the disk size and

the newly added drive letter of the connected disk


![](2.-Restore-the-factory-image-system.pdf-2-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-2-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-3-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-3-1.jpeg)
#### 1.1.2. Create a new partition
Partition the SSD into NTFS format.


Select the drive letter corresponding to the SSD, and then click New Partition:


![](2.-Restore-the-factory-image-system.pdf-4-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-4-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-5-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-5-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-6-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-6-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-7-0.jpeg)
## 2. Restore the factory image
You need to download and decompress the factory image system in the data to the local

computer in advance.

### 2.1. Install Win32DiskImager
Download URL: [https://sourceforge.net/projects/win32diskimager/](https://sourceforge.net/projects/win32diskimager/)


accept the agreement:


![](2.-Restore-the-factory-image-system.pdf-7-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-8-0.jpeg)

Installation location: The default location is recommended


Installation options:


![](2.-Restore-the-factory-image-system.pdf-8-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-9-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-9-1.jpeg)

Start installation:


![](2.-Restore-the-factory-image-system.pdf-10-0.jpeg)

Complete installation:


![](2.-Restore-the-factory-image-system.pdf-10-1.jpeg)
### 2.2. Use Win32DiskImager
①: Select the factory image file (*.img) in the data


②: Select the drive letter corresponding to the solid-state drive


③: Write the factory image to the solid-state drive


Confirm writing to the system:


image-20250123105608261


Wait for the system to be written successfully:


![](2.-Restore-the-factory-image-system.pdf-11-0.jpeg)

![](2.-Restore-the-factory-image-system.pdf-11-1.jpeg)
![](2.-Restore-the-factory-image-system.pdf-12-0.jpeg)

After the system is written, you can close the program and install the SSD to the Jetson Orin

motherboard!
## 3. Description
The Jetson motherboard can start the system normally and it depends on the system Jetpack

version. Generally, only the same version can start the system!
