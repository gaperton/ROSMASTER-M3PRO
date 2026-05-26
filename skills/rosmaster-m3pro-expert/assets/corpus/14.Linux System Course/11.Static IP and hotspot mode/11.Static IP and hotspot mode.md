## **11.Static IP and hotspot mode**

## **1. Static IP**

Click the WiFi icon in the upper right corner of the system interface, and a frame as shown below will appear.

Click [Edit Connections...] at the bottom.

![](_page_0_Picture_4.jpeg)

Double-click the connected Wi-Fi, here is [Yahboom].

![](_page_0_Figure_6.jpeg)

In the [Wi-Fi] directory, select [Mode]-->[Client].

![](_page_1_Figure_0.jpeg)

In the [IPv4 Settings] directory, click the [Add] icon, enter the IP as shown below, and finally click [save] to save.

![](_page_2_Figure_0.jpeg)

Input following command to modify the .bashrc file,

```
sudo vim ~/.bashrc
```

Set ROS\_IP to the IP modified in the previous step, as shown in the figure below.

Note: If you do not connect to this Wi-Fi, be sure to comment out the modified line (just add # in front).

When we newly open the terminal, 【binary operator expected】 appears.

Don't pay attention to it. It does not affect use.

## **2. Hotspot mode**

Click the WiFi icon in the upper right corner of the system interface, and a frame as shown below will appear.

Click [Edit Connections...] at the bottom.

![](_page_3_Picture_4.jpeg)

The frame as shown below will pop up, click [+] to select [Wi-Fi] mode, and click [Create...].

![](_page_3_Picture_6.jpeg)

In the [Wi-Fi] directory, add [yah] in the [SSID] column and select [Hotspot] in the [Mode] column.

![](_page_4_Picture_0.jpeg)

In the [Wi-Fi Security] directory, select [WPA & WPA2 Personal] in the [Security] column, and enter the password in the [Password] column.

![](_page_4_Figure_2.jpeg)

In the [IPv4 Settings] directory, click the [Add] icon and enter the IP as shown in the figure below.

![](_page_5_Figure_1.jpeg)

In the [IPv4 Settings] directory, select [Ignore] in the [Method] column, and finally click [Save] to save.

![](_page_6_Figure_0.jpeg)

In [Wi-Fi] mode, our newly created WIFI appears.

![](_page_6_Figure_2.jpeg)

At this point, the new WIFI has been successfully created. Next, connect to the new WIFI. Follow the steps below.

![](_page_7_Figure_0.jpeg)

Select the newly created WIFI [Wi-Fi connections 1] in the [Connections] column of the pop-up dialog box, and click [Connect].

![](_page_7_Figure_2.jpeg)