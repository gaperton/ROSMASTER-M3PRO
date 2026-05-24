# **Get real-time temperature of Raspberry Pi**

#### **Get [real-time temperature of](#page-0-0) Raspberry Pi**

<span id="page-0-0"></span>[environment](#page-0-1) [Ideas](#page-0-2) Get [temperature](#page-0-3) parameters [actual](#page-1-0) effect

Enter the command through the terminal to check the current CPU temperature of the Raspberry Pi.

## **environment**

System: Raspberry Pi OS

<span id="page-0-1"></span>Raspbian is the old name of Raspberry Pi's official Debian-based operating system, and Raspberry Pi OS is its new name after its name change in 2020.

### **Ideas**

The CPU temperature information of the Raspberry Pi is located in the file /sys/class/thermal/thermal\_zone0/temp, which is a read-only file; we can read the value and convert it to the actual temperature.

### **Get temperature parameters**

Open the terminal and run the following two commands to obtain the temperature parameters:

cd /sys/class/thermal/thermal\_zone0 cat temp

<span id="page-0-3"></span><span id="page-0-2"></span>
$$T_{actual temperature} = \frac{temperature parameter}{1000}$$

# <span id="page-1-0"></span>**actual effect**

![](_page_1_Figure_1.jpeg)