# Battery voltage detection
Battery voltage detection

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Use the voltage detection function on the STM32 control board to learn how to read ADC values.

## 2. Hardware Connection
As shown in the figure below, the battery voltage detection circuit has been integrated into the

STM32 control board, and the battery needs to be plugged into the battery interface.


Please connect the type-C data cable to the computer and the USB Connect port of the STM32

control board.


![](5.Battery-voltage-detection.pdf-0-0.jpeg)
## 3. Core code analysis
The path corresponding to the program source code is:


First, initialize the battery voltage detection ADC channel. The hardware GPIO connected to the

voltage detection is PC0, and the corresponding ADC channel is ADC1_INP10.

```
 void MX_ADC1_Init(void)

 {

 /* USER CODE BEGIN ADC1_Init 0 */

 /* USER CODE END ADC1_Init 0 */

 ADC_MultiModeTypeDef multimode = {0};

 ADC_ChannelConfTypeDef sConfig = {0};

 /* USER CODE BEGIN ADC1_Init 1 */

 /* USER CODE END ADC1_Init 1 */

 /** Common config

 */

 hadc1.Instance = ADC1;

 hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;

 hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;

 hadc1.Init.LowPowerAutoWait = DISABLE;

 hadc1.Init.ContinuousConvMode = DISABLE;

```


![](5.Battery-voltage-detection.pdf-1-1.jpeg)
```
 hadc1.Init.NbrOfConversion = 1;

 hadc1.Init.DiscontinuousConvMode = DISABLE;

 hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;

 hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;

 hadc1.Init.ConversionDataManagement = ADC_CONVERSIONDATA_DR;

 hadc1.Init.Overrun = ADC_OVR_DATA_PRESERVED;

 hadc1.Init.LeftBitShift = ADC_LEFTBITSHIFT_NONE;

 hadc1.Init.OversamplingMode = DISABLE;

 hadc1.Init.Oversampling.Ratio = 1;

 if (HAL_ADC_Init(&hadc1) != HAL_OK)

 {

 Error_Handler();

 }

 hadc1.Init.ClockPrescaler = ADC_CLOCK_ASYNC_DIV6;

 hadc1.Init.Resolution = ADC_RESOLUTION_12B;

 if (HAL_ADC_Init(&hadc1) != HAL_OK)

 {

 Error_Handler();

 }

 /** Configure the ADC multi-mode

 */

 multimode.Mode = ADC_MODE_INDEPENDENT;

 if (HAL_ADCEx_MultiModeConfigChannel(&hadc1, &multimode) != HAL_OK)

 {

 Error_Handler();

 }

 /** Configure Regular Channel

 */

 sConfig.Channel = ADC_CHANNEL_10;

 sConfig.Rank = ADC_REGULAR_RANK_1;

 sConfig.SamplingTime = ADC_SAMPLETIME_1CYCLE_5;

 sConfig.SingleDiff = ADC_SINGLE_ENDED;

 sConfig.OffsetNumber = ADC_OFFSET_NONE;

 sConfig.Offset = 0;

 sConfig.OffsetSignedSaturation = DISABLE;

 if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)

 {

 Error_Handler();

 }

 /* USER CODE BEGIN ADC1_Init 2 */

 /* USER CODE END ADC1_Init 2 */

 }

```

Read the value of the current GPIO ADC channel.

```
 uint16_t Bat_Get_Adc(uint32_t ch)

 {

 ADC_ChannelConfTypeDef ADC1_ChanConf;

 ADC1_ChanConf.Channel = ch;

 ADC1_ChanConf.Rank = ADC_REGULAR_RANK_1;

 ADC1_ChanConf.SamplingTime = ADC_SAMPLETIME_1CYCLE_5;

 ADC1_ChanConf.SingleDiff = ADC_SINGLE_ENDED;

```

```
 ADC1_ChanConf.OffsetNumber = ADC_OFFSET_NONE;

 ADC1_ChanConf.Offset = 0;

 ADC1_ChanConf.OffsetSignedSaturation = DISABLE;

 HAL_ADC_ConfigChannel(&hadc1, &ADC1_ChanConf); // Channel configuration

 HAL_ADC_Start(&hadc1);

 HAL_ADC_PollForConversion(&hadc1, 10);

 return (uint16_t)HAL_ADC_GetValue(&hadc1);

 }

```

Convert the read ADC value into a GPIO voltage value.


Calculate the battery terminal voltage based on the GPIO voltage.


![](5.Battery-voltage-detection.pdf-3-0.jpeg)

![](5.Battery-voltage-detection.pdf-3-1.jpeg)

In App_Handle, print the current battery voltage value in a loop, once per second.


![](5.Battery-voltage-detection.pdf-3-2.jpeg)


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


Connect the expansion board to the computer via a Type-C data cable, open the serial port

assistant (specific parameters are shown in the figure below), and you can see the serial port

assistant print the current battery voltage.


Among them, the first value is the ADC value, the second value is the GPIO voltage value, and the

third value is the battery voltage value.


![](5.Battery-voltage-detection.pdf-4-0.jpeg)

![](5.Battery-voltage-detection.pdf-4-1.jpeg)
![](5.Battery-voltage-detection.pdf-5-0.jpeg)
