# Restore the Factory Image System

## 1. Format the SSD

Before restoring the factory image, format the SSD as `exFAT`.

### 1.1 Download DiskGenius

Download URL: <https://www.diskgenius.com/>

![Figure: page 0: figure 15](_page_0_Figure_15.jpeg)

![Figure: page 0: figure 17](_page_0_Figure_17.jpeg)

Double-click the `.exe` file you just downloaded to install DiskGenius. Follow the prompts to install the software on the Windows computer. After opening the software, it will be as shown below.

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

### 1.2 Use DiskGenius

#### 1.2.1 Delete the Existing Partition

Deleting a partition clears the disk data. Before confirming the operation, verify that the selected drive is the SSD you want to format. Use the disk capacity and the newly added drive letter to identify it.

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

#### 1.2.2 Create a New Partition

Create an `NTFS` partition on the SSD.

Select the drive letter corresponding to the SSD, and then click New Partition:

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

## 2. Restore the Factory Image

Download the factory image from the provided materials and extract it to the local computer before starting.

### 2.1. Install Win32DiskImager

Download URL: <https://sourceforge.net/projects/Win32DiskImager/>

![Figure: page 7: figure 5](_page_7_Figure_5.jpeg)

Open `win32diskimager-1.0.0-install.exe` as an administrator and accept the agreement:

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)

Installation location: the default location is recommended.

![Figure: page 8: figure 2](_page_8_Figure_2.jpeg)

Installation options:

![Figure: page 9: figure 0](_page_9_Figure_0.jpeg)

Start installation:

![Figure: page 10: figure 0](_page_10_Figure_0.jpeg)

![Picture: page 10: picture 3](_page_10_Picture_3.jpeg)

![Figure: page 10: figure 4](_page_10_Figure_4.jpeg)

#### Complete Installation

![Figure: page 10: figure 6](_page_10_Figure_6.jpeg)

### 2.2. Use Win32DiskImager

Select the factory image file (`*.img`) from the materials, select the drive letter that corresponds to the SSD, then write the factory image to the SSD.

![Picture: page 11: picture 4](_page_11_Picture_4.jpeg)

Confirm that you want to write the system image.

Wait for the system image to finish writing.

![Figure: page 11: figure 8](_page_11_Figure_8.jpeg)

![Picture: page 12: picture 0](_page_12_Picture_0.jpeg)

After the system image is written, close the program and install the SSD on the Jetson Orin mainboard.

## 3. Description

Whether the Jetson mainboard starts normally depends on the JetPack version of the system. In general, the board should boot from a system image with the matching JetPack version.
