# **SSD expansion**

#### **SSD [expansion](#page-0-0)**

- <span id="page-0-0"></span>[1. Install](#page-0-1) GParted
- 2. Use [GParted](#page-0-2)
- 3. Adjust [partitions](#page-1-0)

The factory image system will perform disk compression, so the capacity displayed in the system will be inconsistent with the actual capacity. Users can follow the tutorial to expand the SSD.

<span id="page-0-1"></span>The tutorial is located in the Jetson Orin motherboard system

### **1. Install GParted**

```
sudo apt update
sudo apt install gparted -y
```

![](_page_0_Figure_9.jpeg)

## **2. Use GParted**

Find the GParted application icon in the system application menu bar to open it or enter the following command in the terminal to start it:

<span id="page-0-2"></span>gparted

![](_page_1_Figure_0.jpeg)

### <span id="page-1-0"></span>**3. Adjust partitions**

Right-click the disk partition that needs to be expanded: generally select the largest partition in the disk

![](_page_1_Figure_3.jpeg)

You can adjust the partition size through the slider: you can maximize the space and slide to the far right

![](_page_2_Figure_0.jpeg)

Confirm the partition adjustment operation:

image-20250110204116310

![](_page_2_Figure_3.jpeg)

![](_page_3_Figure_0.jpeg)

After partitioning is completed, close the GParted software by yourself!