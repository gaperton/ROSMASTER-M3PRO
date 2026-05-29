# Transfer files remotely

## 1. WinSCP software

Install the WinSCP software by yourself. Here we mainly introduce how to connect to the Raspberry Pi system based on IP, username and password information.

My current login user name is pi, the password is yahboom, and the IP address is 192.168.2.93

![Picture: page 0: picture 11](_page_0_Picture_11.jpeg)

![Picture: page 1: picture 1](_page_1_Picture_1.jpeg)


### Ed25519

```bash
ssh-ed25519 255
```

SHA-256: AmyCUFkAYb3rKjKuYS9Jli0b39Pj03CmqWQpxokTOEk

MD5: ba:7e:d9:3a:dd:22:6c:51:ec:04:a2:37:3f:5b:68:83


### (C)

![Figure: page 1: figure 11](_page_1_Figure_11.jpeg)

#### Connection success interface:

![Figure: page 1: figure 13](_page_1_Figure_13.jpeg)

## Transfer files

You can directly drag local files to the other party's area, so that the files can be copied; the following demonstration is to transfer the Text.txt file to the Raspberry Pi system.

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

You can directly select a folder on your computer and move it to the other party's area. It does not necessarily need to be done within the software!

## 2. SCP command

Use the scp command to send files to the Raspberry Pi system through ssh. This operation does not require the use of software, just use the terminal!

My current login user name is pi, the password is yahboom, and the IP address is 192.168.2.93

### 1.1. Copy the file to the Raspberry Pi motherboard

#### Single file copy command: scp file name username@IP address:path

Copy the file to the user directory: scp Test.txt pi@192.168.2.93:

![Picture: page 2: picture 8](_page_2_Picture_8.jpeg)

Copy the file to the desktop: scp Test.txt pi@192.168.2.93:Desktop/

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

### 1.2. Copy files from the Raspberry Pi motherboard to the current computer

### Single file copy command: scp username@IP address: file name

Copy the files in the Raspberry Pi system to the current directory of the computer: scp pi@192.168.2.93:Test.txt.

Note: The copied file should be in the user directory of the Raspberry Pi system (the copied Test.txt file should be in the pi user directory of the Raspberry Pi)

![Figure: page 3: figure 5](_page_3_Figure_5.jpeg)
