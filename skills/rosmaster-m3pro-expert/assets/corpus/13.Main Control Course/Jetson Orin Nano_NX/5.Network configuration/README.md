# Network configuration

Wi-Fi and hotspot modes require the use of a wireless network card. Before making the following settings, check whether the wireless network card and antenna are installed!

It is recommended to switch networks by connecting to the display screen. Once the network is switched to a new network, the system needs to re-enable network sharing for the new network before VNC remote

## 1. Wi-Fi mode

### 1.1. Connect to Wi-Fi

Select the menu option in the upper right corner of the system desktop -> Wi-Fi options -> Wi-Fi Settings:

![Picture: page 0: picture 13](_page_0_Picture_13.jpeg)

Select the Wi-Fi you want to connect to: If the Wi-Fi signal is very weak, check whether the antenna is not installed or the signal in the environment is poor

![Figure: page 1: figure 0](_page_1_Figure_0.jpeg)

After entering the password, click Connect:

![Figure: page 2: figure 1](_page_2_Figure_1.jpeg)

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

### 1.2. Check Wi-Fi information

Click the settings icon of the connected Wi-Fi:

![Figure: page 3: figure 3](_page_3_Figure_3.jpeg)

The terminal can use the following command to view the IP addresses of all networks: enP8p1s0 is the IP connected by the network cable, and wlP1p1s0 is the IP connected by Wi-Fi

```bash
ifconfig
```

![Figure: page 3: figure 6](_page_3_Figure_6.jpeg)

### 1.3. Set static IP

Click the setting icon of the connected Wi-Fi to modify the IPv4 option:

Address: Fill in the required fixed IP address, which needs to be in the assignable IP address range

Netmask: Fill in 255.255.255.0

Gateway: Fill in the Wi-Fi default gateway address

![Figure: page 4: figure 5](_page_4_Figure_5.jpeg)

After completion, reconnect Wi-Fi to take effect:

![Picture: page 4: picture 7](_page_4_Picture_7.jpeg)

## 2. Hotspot mode

The wireless network card needs to support hotspot to enable hotspot mode.

Configure the hotspot mode on the desktop system. The hotspot will be automatically turned off after the system restarts. Users who need it can find the tutorial on how to start the hotspot on Ubuntu 22.04

### 2.1. Create a hotspot

Enter Wi-Fi settings and select Turn On Wi-Fi Hotspot...

![Picture: page 5: picture 3](_page_5_Picture_3.jpeg)

### 2.2. Hotspot information

Hotspot name: Jetson_Orin_Hot (customizable)

Hotspot password: 12345678 (customizable)

Hotspot mode default IP: 10.42.0.1

![Picture: page 5: picture 8](_page_5_Picture_8.jpeg)

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)
