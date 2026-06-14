# Drive the buzzer
Drive the buzzer

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Read the KEY1 button on the STM32 control board and control the active buzzer to sound.

## 2. Hardware Connection
As shown in the figure below, the KEY1 button and buzzer are onboard components, so no

external devices are required. Please connect the Type-C data cable to the computer and the USB

Connect port on the STM32 control board.


![](3.Drive-the-buzzer.pdf-0-0.jpeg)
## 3. Core code analysis
Open STM32CUBEIDE and import the project. The path corresponding to the program source

code is:


Initialize the peripheral GPIO, where BEEP_GPIO corresponds to PE5 of the hardware circuit, the

GPIO mode is output mode, KEY1 corresponds to PC15 of the hardware circuit, and the GPIO

mode is input pull-up mode.

```
 #define BEEP_Pin GPIO_PIN_5

 #define BEEP_GPIO_Port GPIOE

 #define LED_MCU_Pin GPIO_PIN_13

 #define LED_MCU_GPIO_Port GPIOC

 #define LED_ROS_Pin GPIO_PIN_14

 #define LED_ROS_GPIO_Port GPIOC

 #define KEY1_Pin GPIO_PIN_15

 #define KEY1_GPIO_Port GPIOC

 void MX_GPIO_Init(void)

 {

 GPIO_InitTypeDef GPIO_InitStruct = {0};

```


![](3.Drive-the-buzzer.pdf-1-1.jpeg)

![](3.Drive-the-buzzer.pdf-1-2.jpeg)
```
 /* GPIO Ports Clock Enable */

 __HAL_RCC_GPIOE_CLK_ENABLE();

 __HAL_RCC_GPIOC_CLK_ENABLE();

 __HAL_RCC_GPIOH_CLK_ENABLE();

 __HAL_RCC_GPIOA_CLK_ENABLE();

 /*Configure GPIO pin Output Level */

 HAL_GPIO_WritePin(BEEP_GPIO_Port, BEEP_Pin, GPIO_PIN_RESET);

 /*Configure GPIO pin Output Level */

 HAL_GPIO_WritePin(GPIOC, LED_MCU_Pin|LED_ROS_Pin, GPIO_PIN_RESET);

 /*Configure GPIO pin : PtPin */

 GPIO_InitStruct.Pin = BEEP_Pin;

 GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

 GPIO_InitStruct.Pull = GPIO_NOPULL;

 GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

 HAL_GPIO_Init(BEEP_GPIO_Port, &GPIO_InitStruct);

 /*Configure GPIO pins : PCPin PCPin */

 GPIO_InitStruct.Pin = LED_MCU_Pin|LED_ROS_Pin;

 GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;

 GPIO_InitStruct.Pull = GPIO_NOPULL;

 GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;

 HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

 /*Configure GPIO pin : PtPin */

 GPIO_InitStruct.Pin = KEY1_Pin;

 GPIO_InitStruct.Mode = GPIO_MODE_INPUT;

 GPIO_InitStruct.Pull = GPIO_PULLUP;

 HAL_GPIO_Init(KEY1_GPIO_Port, &GPIO_InitStruct);

 }

```

Turn on the buzzer


Turn off the buzzer


Set the buzzer on time. When time=0, it will be off. When time=1, it will keep ringing. When

time>=10, it will automatically turn off after a delay of xx milliseconds.

```
 void Beep_On_Time(uint16_t time)

 {

 if (time == BEEP_STATE_ON_ALWAYS)

 {

 Beep_Set_State(BEEP_STATE_ON_ALWAYS);

 Beep_Set_Time(0);

 BEEP_ON();

 }

 else if (time == BEEP_STATE_OFF)

 {

 Beep_Set_State(BEEP_STATE_OFF);

```

```
 Beep_Set_Time(0);

 BEEP_OFF();

 }

 else

 {

 if (time >= 10)

 {

 Beep_Set_State(BEEP_STATE_ON_DELAY);

 Beep_Set_Time(time / 10);

 BEEP_ON();

 }

 }

 }

```

The buzzer automatically turns off when it times out and needs to be called every 10 milliseconds.


The Beep_Handle function is called every 10 milliseconds to control the buzzer to sound

according to the status value of the KEY1 button.


![](3.Drive-the-buzzer.pdf-3-0.jpeg)

![](3.Drive-the-buzzer.pdf-3-1.jpeg)


## 4. Compile, download and burn firmware
Select the project to be compiled in the file management interface of STM32CUBEIDE and click the

compile button on the toolbar to start compiling.


![](3.Drive-the-buzzer.pdf-4-0.jpeg)

If there are no errors or warnings, the compilation is complete.


Press and hold the BOOT0 button, then press the RESET button to reset, release the BOOT0

button to enter the serial port burning mode. Then use the serial port burning tool to burn the

firmware to the board.


If you have STlink or JLink, you can also use STM32CUBEIDE to burn the firmware with one click,

which is more convenient and quick.

## 5. Experimental Results
The MCU_LED light flashes every 200 milliseconds.


When you press KEY1, the buzzer sounds once.


![](3.Drive-the-buzzer.pdf-4-1.jpeg)

![](3.Drive-the-buzzer.pdf-4-2.jpeg)
