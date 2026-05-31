# **Burning STM32 firmware using serial port**

Burning STM32 [firmware](#page-0-0) using serial port

- <span id="page-0-0"></span>[1. Download and install](#page-0-1) the tool
- [2. Hardware](#page-0-2) Connection
- <span id="page-0-1"></span>[3. STM32CubeProgrammer](#page-1-0) burns firmware

### **1. Download and install the tool**

Here we take Win 64-bit system as an example

This time we need to use the STM32CubeProgrammer burning tool. Download link:

https://www.st.com/en/development-tools/stm32cubeprog.html

![](_page_0_Picture_10.jpeg)

Serial port driver download address:

https://www.silabs.com/documents/public/software/CP210x\_Windows\_Drivers.zip

After downloading the burning tool and serial port driver, unzip them and follow the prompts to install them.

### <span id="page-0-2"></span>**2. Hardware Connection**

Use a Type-C data cable to connect to the computer.

![](_page_1_Picture_0.jpeg)

## **3. STM32CubeProgrammer burns firmware**

Open the STM32CubeProgrammer software, select the [UART] mode, select the corresponding serial port number in [Port], and other parameters are as shown in the figure below.

<span id="page-1-0"></span>![](_page_1_Picture_3.jpeg)

Now press and hold the BOOT button on the control board, press the RESET button again, and then release the BOOT button. The STM32 will enter the serial port programming mode. Click the [Connect] button to connect.

![](_page_2_Picture_1.jpeg)

The status will change if the connection is successful.

![](_page_2_Picture_3.jpeg)

Click the download button to enter the download page, click [Browse] to select the hex file to download, and then click [Start Programming] to start burning the firmware.

![](_page_2_Figure_5.jpeg)

There will be a prompt after the firmware burning is completed.