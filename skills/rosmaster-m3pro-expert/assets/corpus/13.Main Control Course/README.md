# Main Control Course

This section provides setup and maintenance references for the ROSMASTER-M3PRO compute boards. It covers Jetson Nano B01, Jetson Orin Nano/NX, and Raspberry Pi 5 system images, startup, networking, remote access, storage expansion, backups, monitoring, and common board operations.

**Jetson Nano B01**

## [13.1.1 Jetson Nano B01 SUB Board Introduction](./Jetson%20Nano%20B01/1.%20Introduction%20to%20the%20Jetson%20Nano%20B01%20SUB%20Board/README.md)

Identify the Jetson Nano B01 SUB board interfaces, basic connections, and carrier-board layout.

## [13.1.2 Write the System Image](./Jetson%20Nano%20B01/2.%20Burn%20the%20system%20image/README.md)

Flash the eMMC boot files and prepare the USB system image used to start the Jetson Nano B01.

## [13.1.3 Re-Write an Existing Memory Card or USB Drive](./Jetson%20Nano%20B01/3.%20Re-read%20the%20memory%20card%20or%20USB%20drive%20that%20has%20been%20burned/README.md)

Recover or rewrite a previously imaged memory card or USB drive when it needs to be prepared again.

## [13.1.4 Startup System](./Jetson%20Nano%20B01/4.%20Startup%20system/README.md)

Connect the required peripherals and power up the Jetson Nano B01 system for first startup.

## [13.1.5 System and Desktop Introduction](./Jetson%20Nano%20B01/5.%20Jetson%20Nano%20B01%20System%20and%20Desktop%20Introduction/README.md)

Review the Jetson Nano B01 desktop, system environment, and basic UI layout.

## [13.1.6 Memory Card or USB Drive Expansion](./Jetson%20Nano%20B01/6.%20Memory%20card%20or%20USB%20flash%20drive%20expansion/README.md)

Expand the storage partition after writing the system image so the full capacity is available.

## [13.1.7 Network Configuration](./Jetson%20Nano%20B01/7.%20Network%20Configuration/README.md)

Configure network access for the Jetson Nano B01, including wired and wireless connection workflows.

## [13.1.8 SSH Remote Login and File Transfer](./Jetson%20Nano%20B01/8.%20SSH%20remote%20login%20%26%20file%20transfer/README.md)

Use SSH and file-transfer tools to access the Jetson Nano B01 from another computer.

## [13.1.9 VNC Remote Login](./Jetson%20Nano%20B01/9.%20VNC%20Remote%20Login/README.md)

Connect to the Jetson Nano B01 desktop remotely through VNC.

## [13.1.10 System Backup](./Jetson%20Nano%20B01/10.%20Jetson%20Nano%20B01%20system%20backup/README.md)

Back up the Jetson Nano B01 system image so it can be restored later.

## [13.1.11 Swap Space Increase](./Jetson%20Nano%20B01/11.%20Jetson%20Nano%20Swap%20space%20increased/README.md)

Increase swap space to improve stability when the Jetson Nano B01 runs memory-heavy workloads.

## [13.1.12 jtop Installation and Use](./Jetson%20Nano%20B01/12.%20Installation%20and%20use%20of%20Jtop/README.md)

Install and use `jtop` to monitor Jetson Nano B01 CPU, memory, temperature, and system load.

**Jetson Orin Nano / NX**

## [13.2.1 Jetson Orin Board Introduction](./Jetson%20Orin%20Nano_NX/1.Jetson%20Orin%20board%20introduction/README.md)

Review the Jetson Orin Nano/NX board interfaces, connectors, and supported startup layout.

## [13.2.2 Restore the Factory Image System](./Jetson%20Orin%20Nano_NX/2.%20Restore%20the%20factory%20image%20system/README.md)

Format the SSD and write the factory image system used by the Jetson Orin Nano/NX board.

## [13.2.3 Backup SSD System](./Jetson%20Orin%20Nano_NX/3.Backup%20SSD%20system/README.md)

Back up the Jetson Orin SSD system image for recovery or duplication.

## [13.2.4 SSD Expansion](./Jetson%20Orin%20Nano_NX/4.SSD%20expansion/README.md)

Expand the SSD partition after imaging so the full disk capacity is available.

## [13.2.5 Network Configuration](./Jetson%20Orin%20Nano_NX/5.Network%20configuration/README.md)

Configure network access for Jetson Orin Nano/NX, including Wi-Fi and wired connection options.

## [13.2.6 SSH Remote Login](./Jetson%20Orin%20Nano_NX/6.SSH%20remote%20login/README.md)

Access the Jetson Orin Nano/NX terminal remotely over SSH.

## [13.2.7 VNC Remote Control](./Jetson%20Orin%20Nano_NX/7.VNC%20remote%20control/README.md)

Connect to and operate the Jetson Orin Nano/NX desktop through VNC.

## [13.2.8 Remote File Transfer](./Jetson%20Orin%20Nano_NX/8.Remote%20file%20transfer/README.md)

Transfer files between the Jetson Orin Nano/NX and a host computer.

## [13.2.9 jtop Tool](./Jetson%20Orin%20Nano_NX/9.Jtop%20tool/README.md)

Use `jtop` to monitor Jetson Orin Nano/NX system status and resource usage.

## [13.2.10 Swap Space Expansion](./Jetson%20Orin%20Nano_NX/10.Exchange%20space%20expansion/README.md)

Increase swap space for workloads that need more memory headroom.

**Raspberry Pi 5**

## [13.3.1 Introduction to Raspberry Pi 5](./Raspberry%20Pi/1.Introduction%20to%20Raspberry%20PI%205/README.md)

Review the Raspberry Pi 5 hardware, interfaces, installation considerations, and supported accessories.

## [13.3.2 System Installation and Backup](./Raspberry%20Pi/2.%20Raspberry%20PI%20system%20installation%20and%20backup/README.md)

Install Raspberry Pi OS with Raspberry Pi Imager or Win32DiskImager, then back up or restore the SD card image.

## [13.3.3 Powering the Raspberry Pi 5](./Raspberry%20Pi/3.Powering%20the%20Raspberry%20PI%205/README.md)

Power the Raspberry Pi 5 correctly and understand the supported power-supply options.

## [13.3.4 Startup](./Raspberry%20Pi/4.Startup%20of%20Raspberry%20PI%205/README.md)

Start the Raspberry Pi 5 system after the OS image and peripherals are prepared.

## [13.3.5 Update and Upgrade the OS](./Raspberry%20Pi/5.Update%20and%20upgrade%20operating%20system/README.md)

Update package sources and upgrade installed software on Raspberry Pi OS.

## [13.3.6 raspi-config Tool](./Raspberry%20Pi/6.Introduction%20to%20raspi-config%20tool/README.md)

Use `raspi-config` to configure common Raspberry Pi system options.

## [13.3.7 config.txt File Description](./Raspberry%20Pi/7.config.txt%20file%20description/README.md)

Understand the key Raspberry Pi `config.txt` settings used for boot and hardware configuration.

## [13.3.8 Network Configuration](./Raspberry%20Pi/8.Network%20Configuration/README.md)

Configure Raspberry Pi 5 network access, including Wi-Fi and wired network setup.

## [13.3.9 Remote Access](./Raspberry%20Pi/9.remote%20access/README.md)

Enable and use remote access methods for Raspberry Pi 5.

## [13.3.10 Transfer Files Remotely](./Raspberry%20Pi/10.Transfer%20files%20remotely/README.md)

Move files between Raspberry Pi 5 and another computer with remote-transfer tools.

## [13.3.11 Set Display Resolution and Rotation](./Raspberry%20Pi/11.Set%20display%20resolution%20and%20rotation/README.md)

Configure Raspberry Pi 5 display resolution and screen rotation.

## [13.3.12 Set Screen to Sleep](./Raspberry%20Pi/12.Set%20screen%20to%20sleep/README.md)

Adjust screen sleep behavior for the Raspberry Pi display environment.

## [13.3.13 Play Audio and Video](./Raspberry%20Pi/13.Play%20audio%20and%20video/README.md)

Play media and verify audio/video output on Raspberry Pi 5.

## [13.3.14 Using a USB Camera](./Raspberry%20Pi/14.Using%20USB%20camera/README.md)

Connect a USB camera and verify capture on Raspberry Pi 5.

## [13.3.15 Using a MIPI Camera](./Raspberry%20Pi/15.Using%20MIPI%20camera/README.md)

Connect and test a MIPI camera on Raspberry Pi 5.

## [13.3.16 Get Real-Time Raspberry Pi Temperature](./Raspberry%20Pi/16.Get%20real-time%20temperature%20of%20Raspberry%20Pi/README.md)

Read Raspberry Pi 5 temperature data in real time for monitoring and diagnostics.
