# **Set up the STM32CUBEIDE development environment**

Set up the [STM32CUBEIDE](#page-0-0) development environment

- <span id="page-0-0"></span>1. Introduction to [STM32CubeIDE](#page-0-1)
- [2. Download the](#page-0-2) installation package
- 3. Start [installation](#page-1-0)
- 4. New [construction](#page-3-0) projects
- 5. Pin [configuration](#page-6-0)
- [6. Write](#page-8-0) code
- <span id="page-0-1"></span>[7. Compile](#page-9-0) the program

## **1. Introduction to STM32CubeIDE**

STM32CubeIDE is an all-in-one, multi-OS development tool and an advanced C/C++ development platform with peripheral configuration, code generation, compilation, and debugging capabilities for STM32 microcontrollers and microprocessors. Based on the Eclipse®/CDT™ framework and the GCC toolchain for development, and GDB for debugging, it allows you to select an STM32 microprocessor, create a project, and generate initialization code. It supports graphical configuration of the STM32's clocks and pins, and supports mainstream platforms including Windows, Linux, and Mac. Its functionality is extremely powerful and practical.

## <span id="page-0-2"></span>**2. Download the installation package**

Open the following link in your computer browser:

<https://www.st.com/en/development-tools/stm32cubeide.html>

Download according to the computer system. Here we take Win10 system as an example to install the current latest version (version 1.19.0). The operations for other versions are similar.

If you have an account on my.st.com, you can log in directly and download the software. If you do not want to log in now, simply provide your name and email address in the form below to download the software.

Unzip the downloaded file, and do not use Chinese characters in the unzip path.

<span id="page-1-0"></span>

# **3. Start installation**

Double-click to open the installation package. Then follow the tutorial.

![](_page_1_Figure_4.jpeg)

The installation path can be modified according to actual needs. Be careful not to include Chinese characters.

![](_page_2_Figure_0.jpeg)

Select the driver and click Install.

![](_page_2_Figure_2.jpeg)

Then just wait for the installation to complete.

![](_page_3_Figure_0.jpeg)

#### **4. New construction projects**

\1. Double-click the shortcut on the desktop to open STM32CubeIDE. You need to select a workspace and save it in a different path (without Chinese characters).

<span id="page-3-0"></span>![](_page_3_Picture_3.jpeg)

![](_page_3_Picture_7.jpeg)

\2. Click File->New->STM32 Project.

![](_page_4_Figure_0.jpeg)

\3. Search and select the STM32H743VGT6 chip, then click Next in the lower right corner to proceed to the next step.

![](_page_4_Figure_2.jpeg)

\4. Enter the project name. Here we take LED as an example. Other parameters can be left as default.

![](_page_5_Figure_0.jpeg)

\5. Click Yes and the graphical content will be loaded.

![](_page_5_Figure_2.jpeg)

The completion is as shown below:

![](_page_6_Picture_0.jpeg)

# <span id="page-6-0"></span>**5. Pin configuration**

\1. First, you need debug information. Under Pinout & Configuration, click [Trace and Debug] -> [Debug] and select [Serial Wire].

![](_page_6_Figure_3.jpeg)

\2. Modify the system clock of STM32 and the external crystal oscillator 25M frequency.

In Pinout & Configuration, select [RCC] -> [HSE] and select [Crystal/Ceramic Resonator]. HSE is the external clock, and LSE is the internal clock. Using an external clock is more stable and efficient than the internal clock.

![](_page_6_Figure_6.jpeg)

Switch to the [Clock Configuration] interface, set the chip main frequency to 480Mhz, and press Enter to confirm.

![](_page_7_Figure_1.jpeg)

![](_page_7_Picture_3.jpeg)

\3. Add LED\_MCU pin configuration. From the pin assignment diagram, we can see that the LED is connected to the PC13 pin.

![](_page_7_Picture_5.jpeg)

Set the PC13 pin to GPIO\_Output. For convenience, change the Label to LED\_MCU.

![](_page_8_Figure_0.jpeg)

Then press Ctrl+S to save, check Remember my decision, and click Yes. This will automatically generate code every time you save.

![](_page_8_Figure_2.jpeg)

#### <span id="page-8-0"></span>**6. Write code**

\1. Since the system initialization code has been generated in the previous graphical configuration, we only need to add the functions to be implemented.

Find the main function in the main.c file and add the code below while(1) to control the LED. This will cause the LED to flash every 200 milliseconds. Press Ctrl+S to save the code.

**Note: Code content must be added between USER CODE BEGIN and USER CODE END. Otherwise, the code content will be overwritten the next time you generate code using the graphical tool. Code added between USER CODE BEGIN and USER CODE END will not be overwritten. Do not write Chinese comments in this section, as this may result in garbled characters.**

#### **7. Compile the program**

\1. Add the function of generating HEX file.

Click Project->Properties->C/C++ Build->Settings->MCU Post build outputs, and then check Convert to Intel Hex file (-O ihex), as shown in the figure below.

<span id="page-9-0"></span>![](_page_9_Picture_5.jpeg)

![](_page_10_Figure_0.jpeg)

\2. Click the hammer in the toolbar to start compiling the project.

![](_page_10_Picture_2.jpeg)

The STM32CubeIDE Console window will pop up. If you see 0 compilation errors and 0 warnings, the compilation is successful. As shown in the figure below, the file generated by the project is named LED.hex and is saved in the Debug folder of the project directory.

![](_page_10_Figure_4.jpeg)