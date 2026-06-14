# Burning STM32 firmware using serial port
Burning STM32 firmware using serial port

1. Download and install the tool

2. Hardware Connection

3. STM32CubeProgrammer burns firmware

## 1. Download and install the tool
Here we take Win 64-bit system as an example


This time we need to use the STM32CubeProgrammer burning tool. Download link:


![](4.Burning-STM32-firmware-using-serial-port.pdf-0-1.jpeg)

Serial port driver download address:


After downloading the burning tool and serial port driver, unzip them and follow the prompts to

install them.

## 2. Hardware Connection
Use a Type-C data cable to connect to the computer.


![](4.Burning-STM32-firmware-using-serial-port.pdf-1-0.jpeg)
## 3. STM32CubeProgrammer burns firmware
Open the STM32CubeProgrammer software, select the [UART] mode, select the corresponding

serial port number in [Port], and other parameters are as shown in the figure below.


![](4.Burning-STM32-firmware-using-serial-port.pdf-1-1.jpeg)
Now press and hold the BOOT button on the control board, press the RESET button again, and

then release the BOOT button. The STM32 will enter the serial port programming mode. Click the

[Connect] button to connect.


The status will change if the connection is successful.


Click the download button to enter the download page, click [Browse] to select the hex file to

download, and then click [Start Programming] to start burning the firmware.


![](4.Burning-STM32-firmware-using-serial-port.pdf-2-0.jpeg)

![](4.Burning-STM32-firmware-using-serial-port.pdf-2-1.jpeg)

![](4.Burning-STM32-firmware-using-serial-port.pdf-2-2.jpeg)
There will be a prompt after the firmware burning is completed.
