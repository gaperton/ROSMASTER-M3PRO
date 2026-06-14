# Light up the LED light
Light up the LED light

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Control the LED indicator on the STM32 control board to flash.

## 2. Hardware Connection
As shown in the figure below, the LED indicator is an onboard component, so no external devices

are required. Please connect the Type-C data cable between the computer and the USB Connect

port on the STM32 control board.


![](1.Turn-on-the-LED-light.pdf-0-0.jpeg)
## 3. Core code analysis
Open STM32CUBEIDE and import the project. The path corresponding to the program source

code is:


Initialize the LED peripheral, where LED_GPIO corresponds to PC13 of the hardware circuit and

the GPIO mode is output mode.

```
 #define LED_MCU_Pin GPIO_PIN_13

 #define LED_MCU_GPIO_Port GPIOC

 void MX_GPIO_Init(void)

 {

```


![](1.Turn-on-the-LED-light.pdf-1-1.jpeg)

![](1.Turn-on-the-LED-light.pdf-1-2.jpeg)
```
 GPIO_InitTypeDef GPIO_InitStruct = {0};

 /* GPIO Ports Clock Enable */

 __HAL_RCC_GPIOC_CLK_ENABLE();

 __HAL_RCC_GPIOH_CLK_ENABLE();

 __HAL_RCC_GPIOA_CLK_ENABLE();

 /*Configure GPIO pin Output Level */

 HAL_GPIO_WritePin(LED_MCU_GPIO_Port, LED_MCU_Pin, GPIO_PIN_RESET);

 /*Configure GPIO pin : PtPin */

 GPIO_InitStruct.Pin = LED_MCU_Pin;

 GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

 GPIO_InitStruct.Pull = GPIO_NOPULL;

 GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

 HAL_GPIO_Init(LED_MCU_GPIO_Port, &GPIO_InitStruct);

 }

```

Turn on the LED light


Turn off LED lights


Control the LED light status flip


The LED blinking function flips the LED state every time it is called 20 times.


![](1.Turn-on-the-LED-light.pdf-2-3.jpeg)


Call the App_Led_Mcu_Handle function every 10 milliseconds to make the LED blink.


![](1.Turn-on-the-LED-light.pdf-2-4.jpeg)


## 4. Compile, download and burn firmware
Select the project to be compiled in the file management interface of STM32CUBEIDE and click the

compile button on the toolbar to start compiling.


If there are no errors or warnings, the compilation is complete.


Press and hold the BOOT0 button, then press the RESET button to reset, release the BOOT0

button to enter the serial port burning mode. Then use the serial port burning tool to burn the

firmware to the board.


If you have STlink or JLink, you can also use STM32CUBEIDE to burn the firmware with one click,

which is more convenient and quick.

## 5. Experimental Results
The MCU_LED light flashes every 200 milliseconds.


![](1.Turn-on-the-LED-light.pdf-3-0.jpeg)

![](1.Turn-on-the-LED-light.pdf-3-1.jpeg)

![](1.Turn-on-the-LED-light.pdf-3-2.jpeg)
