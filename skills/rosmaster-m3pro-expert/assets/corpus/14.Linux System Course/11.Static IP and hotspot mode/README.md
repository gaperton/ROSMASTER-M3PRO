## 11.Static IP and hotspot mode

## 1. Static IP

Click the Wi-Fi icon in the upper right corner of the system interface, and a frame as shown below will appear.

Click [Edit Connections...] at the bottom.

![Picture: page 0: picture 4](_page_0_Picture_4.jpeg)

Double-click the connected Wi-Fi, here is [Yahboom].

![Figure: page 0: figure 6](_page_0_Figure_6.jpeg)

In the [Wi-Fi] directory, select [Mode]-->[Client].

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

In the [IPv4 Settings] directory, click the [Add] icon, enter the IP as shown below, and finally click [save] to save.

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

Input following command to modify the.bashrc file,

```
sudo vim ~/.bashrc
```

Set ROS_IP to the IP modified in the previous step, as shown in the figure below.

Note: If you do not connect to this Wi-Fi, be sure to comment out the modified line (just add # in front).

When we newly open the terminal, 【binary operator expected】 appears.

Don't pay attention to it. It does not affect use.

## 2. Hotspot mode

Click the Wi-Fi icon in the upper right corner of the system interface, and a frame as shown below will appear.

Click [Edit Connections...] at the bottom.

![Picture: page 3: picture 4](_page_3_Picture_4.jpeg)

The frame as shown below will pop up, click [+] to select [Wi-Fi] mode, and click [Create...].

![Picture: page 3: picture 6](_page_3_Picture_6.jpeg)

In the [Wi-Fi] directory, add [yah] in the [SSID] column and select [Hotspot] in the [Mode] column.

![Picture: page 4: picture 0](_page_4_Picture_0.jpeg)

In the [Wi-Fi Security] directory, select [WPA & WPA2 Personal] in the [Security] column, and enter the password in the [Password] column.

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

In the [IPv4 Settings] directory, click the [Add] icon and enter the IP as shown in the figure below.

![Figure: page 5: figure 1](_page_5_Figure_1.jpeg)

In the [IPv4 Settings] directory, select [Ignore] in the [Method] column, and finally click [Save] to save.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

In [Wi-Fi] mode, our newly created Wi-Fi appears.

![Figure: page 6: figure 2](_page_6_Figure_2.jpeg)

At this point, the new Wi-Fi has been successfully created. Next, connect to the new Wi-Fi. Follow the steps below.

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

Select the newly created Wi-Fi [Wi-Fi connections 1] in the [Connections] column of the pop-up dialog box, and click [Connect].

![Figure: page 7: figure 2](_page_7_Figure_2.jpeg)
