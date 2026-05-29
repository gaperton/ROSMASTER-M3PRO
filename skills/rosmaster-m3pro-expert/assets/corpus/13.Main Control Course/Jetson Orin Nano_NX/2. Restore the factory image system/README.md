# Restore the factory image system

## 1. Format the SSD

Before restoring the factory image, you need to format the SSD into exFAT format.

### 1.1. Download DiskGenius

Download URL: <https://www.diskgenius.com/>

![Figure: page 0: figure 15](_page_0_Figure_15.jpeg)

![Figure: page 0: figure 17](_page_0_Figure_17.jpeg)

Double-click the exe file you just downloaded to install DiskGenius. Follow the prompts to install the software on the Windows computer. After opening the software, it will be as shown below.

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

### 1.1. Use DiskGenius

#### 1.1.1. Delete partition

Deleting a partition will clear the disk data. Please confirm whether the drive letter is the disk that needs to be formatted before confirming the operation: you can judge based on the disk size and the newly added drive letter of the connected disk

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

#### 1.1.2. Create a new partition

Partition the SSD into NTFS format.

Select the drive letter corresponding to the SSD, and then click New Partition:

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

## 2. Restore the factory image

You need to download and decompress the factory image system in the data to the local computer in advance.

### 2.1. Install Win32DiskImager

Download URL: <https://sourceforge.net/projects/win32diskimager/>

![Figure: page 7: figure 5](_page_7_Figure_5.jpeg)

Open the win32diskimager-1.0.0-install.exe installation package as an administrator and accept the agreement:

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)

Installation location: The default location is recommended

![Figure: page 8: figure 2](_page_8_Figure_2.jpeg)

Installation options:

![Figure: page 9: figure 0](_page_9_Figure_0.jpeg)

Start installation:

![Figure: page 10: figure 0](_page_10_Figure_0.jpeg)

![Picture: page 10: picture 3](_page_10_Picture_3.jpeg)

![Figure: page 10: figure 4](_page_10_Figure_4.jpeg)

#### Complete installation:

![Figure: page 10: figure 6](_page_10_Figure_6.jpeg)

### 2.2. Use Win32DiskImager

Select the factory image file (\*.img) in the data
Select the drive letter corresponding to the solid-state drive
Write the factory image to the solid-state drive

![Picture: page 11: picture 4](_page_11_Picture_4.jpeg)

Confirm writing to the system:

image-20250123105608261

Wait for the system to be written successfully:

![Figure: page 11: figure 8](_page_11_Figure_8.jpeg)

![Picture: page 12: picture 0](_page_12_Picture_0.jpeg)

After the system is written, you can close the program and install the SSD to the Jetson Orin motherboard!

## 3. Description

The Jetson motherboard can start the system normally and it depends on the system Jetpack version. Generally, only the same version can start the system!
