# jtop Tool

## 1. Install jtop

```bash
sudo apt update
sudo apt install python3-pip -y
sudo pip3 install -U jetson-stats
```

![Figure: page 0: figure 10](_page_0_Figure_10.jpeg)

## 2. Best performance mode

### 2.1. Enable MAXN mode

Enable MAXN power mode so all CPU and GPU cores are available:

```
sudo nvpmodel -m 2
```

### 2.2. Enable Jetson Clocks

Enable Jetson Clocks so the CPU and GPU cores run at maximum frequency:

```
sudo jetson_clocks
```

## 3. Use jtop

After restarting the system, run `jtop` in a terminal to start the monitoring tool:

```
jtop
```

Note: Set the mainboard power mode to MAXN to display the highest performance parameters.

![Figure: page 1: figure 7](_page_1_Figure_7.jpeg)

![Figure: page 1: figure 8](_page_1_Figure_8.jpeg)

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)
