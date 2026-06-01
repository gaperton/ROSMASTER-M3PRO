# Drive the Buzzer

## 1. Experimental Purpose

Read the KEY1 button on the STM32 control board and control the active buzzer to sound.

## 2. Hardware Connection

As shown in the figure below, the KEY1 button and buzzer are onboard components, so no external devices are required. Please connect the Type-C data cable to the computer and the USB Connect port on the STM32 control board.

![Picture: page 0: picture 11](_page_0_Picture_11.jpeg)

## 3. Core Code Analysis

Open STM32CubeIDE and import the project. The program source code is located at:

```
Board_Samples/STM32_Samples/Beep
```

Initialize the peripheral GPIO, where BEEP_GPIO corresponds to PE5 of the hardware circuit, the GPIO mode is output mode, KEY1 corresponds to PC15 of the hardware circuit, and the GPIO mode is input pull-up mode.

![Picture: page 1: picture 4](_page_1_Picture_4.jpeg)

![Figure: page 1: figure 5](_page_1_Figure_5.jpeg)

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

```
#define BEEP_ON() HAL_GPIO_WritePin(BEEP_GPIO_Port, BEEP_Pin, SET)
```

Turn off the buzzer

```
#define BEEP_OFF() HAL_GPIO_WritePin(BEEP_GPIO_Port, BEEP_Pin, RESET)
```

Set the buzzer on time. When time=0, it will be off. When time=1, it will keep ringing. When time>=10, it will automatically turn off after a delay of xx milliseconds.

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

```
void Beep_Handle(void)
{
    if (Beep_Get_State() == BEEP_STATE_ON_DELAY)
    {
        if (Beep_Get_Time())
        {
            beep_on_time--;
        }
        else
        {
            BEEP_OFF();
            Beep_Set_State(BEEP_STATE_OFF);
        }
    }
}
```

The Beep_Handle function is called every 10 milliseconds to control the buzzer to sound according to the status value of the KEY1 button.

```
while (1)
{
    if (Key1_State())
    {
        Beep_On_Time(100);
    }
    Beep_Handle();
    App_Led_Mcu_Handle();
    HAL_Delay(10);
}
```

## 4. Compile, Download, and Flash Firmware

In STM32CubeIDE, select the project in the file browser and click the compile button on the toolbar.

![Picture: page 4: picture 0](_page_4_Picture_0.jpeg)

Compilation is complete when no errors or warnings are reported.

Press and hold the BOOT0 button, then press the RESET button to reset, release the BOOT0 button to enter the serial port flashing mode. Then use the serial port burning tool to flash the firmware to the board.

If you have ST-LINK or JLink, you can also use STM32CubeIDE to flash the firmware with one click, which is more convenient and quick.

## 5. Experimental Results

The MCU_LED light flashes every 200 milliseconds.

When you press KEY1, the buzzer sounds once.

![Picture: page 4: picture 8](_page_4_Picture_8.jpeg)
