# **Restore the factory image system**

#### **[Restore the factory image system](#page-0-0)**

- <span id="page-0-0"></span>[1. Format](#page-0-1) the SSD
  - [1.1. Download DiskGenius](#page-0-2)
  - 1.1. Use [DiskGenius](#page-1-0)
    - 1.1.1, Delete [partition](#page-1-1)
    - [1.1.2. Create](#page-3-0) a new partition
- [2. Restore](#page-7-0) the factory image
  - 2.1. Install [Win32DiskImager](#page-7-1)
  - 2.2. Use [Win32DiskImager](#page-11-0)
- <span id="page-0-2"></span><span id="page-0-1"></span>[3. Description](#page-12-0)

# **1. Format the SSD**

Before restoring the factory image, you need to format the SSD into exFAT format.

## **1.1. Download DiskGenius**

Download URL: <https://www.diskgenius.com/>

![](_page_0_Figure_15.jpeg)

![](_page_0_Figure_17.jpeg)

Double-click the exe file you just downloaded to install DiskGenius. Follow the prompts to install the software on the Windows computer. After opening the software, it will be as shown below.

![](_page_1_Figure_0.jpeg)

## <span id="page-1-0"></span>**1.1. Use DiskGenius**

#### <span id="page-1-1"></span>**1.1.1, Delete partition**

Deleting a partition will clear the disk data. Please confirm whether the drive letter is the disk that needs to be formatted before confirming the operation: you can judge based on the disk size and the newly added drive letter of the connected disk

![](_page_2_Figure_0.jpeg)

![](_page_3_Figure_0.jpeg)

#### <span id="page-3-0"></span>**1.1.2. Create a new partition**

Partition the SSD into NTFS format.

Select the drive letter corresponding to the SSD, and then click New Partition:

![](_page_4_Figure_0.jpeg)

![](_page_5_Figure_0.jpeg)

![](_page_6_Figure_0.jpeg)

![](_page_7_Figure_0.jpeg)

# <span id="page-7-0"></span>**2. Restore the factory image**

You need to download and decompress the factory image system in the data to the local computer in advance.

## <span id="page-7-1"></span>**2.1. Install Win32DiskImager**

Download URL: <https://sourceforge.net/projects/win32diskimager/>

![](_page_7_Figure_5.jpeg)

Open the win32diskimager-1.0.0-install.exe installation package as an administrator and accept the agreement:

![](_page_8_Figure_0.jpeg)

Installation location: The default location is recommended

![](_page_8_Figure_2.jpeg)

Installation options:

![](_page_9_Figure_0.jpeg)

Start installation:

![](_page_10_Figure_0.jpeg)

![](_page_10_Picture_3.jpeg)

![](_page_10_Figure_4.jpeg)

#### Complete installation:

![](_page_10_Figure_6.jpeg)

### **2.2. Use Win32DiskImager**

- ①: Select the factory image file (\*.img) in the data
- ②: Select the drive letter corresponding to the solid-state drive
- ③: Write the factory image to the solid-state drive

<span id="page-11-0"></span>![](_page_11_Picture_4.jpeg)

Confirm writing to the system:

image-20250123105608261

Wait for the system to be written successfully:

![](_page_11_Figure_8.jpeg)

![](_page_12_Picture_0.jpeg)

After the system is written, you can close the program and install the SSD to the Jetson Orin motherboard!

## <span id="page-12-0"></span>**3. Description**

The Jetson motherboard can start the system normally and it depends on the system Jetpack version. Generally, only the same version can start the system!