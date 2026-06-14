# CAN bus communication
CAN bus communication

1. Experimental Purpose

2. Hardware Connection

3. Core code analysis

4. Compile, download and burn firmware

5. Experimental Results

## 1. Experimental Purpose
Use the FDCAN function of the STM32 control board, configure the FDCAN as a traditional CAN

function, and learn how to receive and parse CAN data.

## 2. Hardware Connection
As shown in the figure below, the STM32 control board integrates the FDCAN interface. For testing

convenience, this routine uses the loopback mode and the CAN interface does not need to be

connected to other CAN devices.


Please connect the type-C data cable to the computer and the USB Connect port of the STM32

control board.


Note: In the test routine, the CAN interface can be left floating.


![](18.CAN-bus-communication.pdf-0-0.jpeg)
If you need to connect other CAN devices, please align the CAN interface silkscreen: connect CAN
H on the left and CAN-L on the right. Then change the CAN mode to standard mode, recompile

the firmware and burn it.

## 3. Core code analysis
The path corresponding to the program source code is:


![](18.CAN-bus-communication.pdf-1-0.jpeg)


According to the pin assignment, CAN_TX is connected to PD1 and CAN_RX is connected to PD0.


According to the CAN component provided by STM32CUBEIDE, configure the frame format to

traditional mode and the CAN mode to loopback mode. If you need to connect an external CAN

device, set the Mode mode to standard mode.


![](18.CAN-bus-communication.pdf-1-2.jpeg)
![](18.CAN-bus-communication.pdf-2-0.jpeg)

Set the baud rate of FDCAN to 1000kbps


Initialize CAN configuration.

```
 FDCAN_TxFrame_TypeDef TxFrame = {

 .hcan = &hfdcan1,

 .Header.IdType = FDCAN_STANDARD_ID,

 .Header.TxFrameType = FDCAN_DATA_FRAME,

 .Header.DataLength = 8,

 .Header.ErrorStateIndicator = FDCAN_ESI_ACTIVE,

 .Header.BitRateSwitch = FDCAN_BRS_OFF,

 .Header.FDFormat = FDCAN_CLASSIC_CAN,

 .Header.TxEventFifoControl = FDCAN_NO_TX_EVENTS,

 .Header.MessageMarker = 0,

 };

```


![](18.CAN-bus-communication.pdf-2-1.jpeg)
```
 void Can_Init(void)

 {

 FDCAN_FilterTypeDef FDCAN1_FilterConfig;

 FDCAN1_FilterConfig.IdType = FDCAN_STANDARD_ID;

 FDCAN1_FilterConfig.FilterIndex = 0;

 FDCAN1_FilterConfig.FilterType = FDCAN_FILTER_MASK;

 FDCAN1_FilterConfig.FilterConfig = FDCAN_FILTER_TO_RXFIFO0;

 FDCAN1_FilterConfig.FilterID1 = 0x00000000;

 FDCAN1_FilterConfig.FilterID2 = 0x00000000;

 if (HAL_FDCAN_ConfigFilter(&hfdcan1, &FDCAN1_FilterConfig) != HAL_OK)

 {

 Error_Handler();

 }

 if (HAL_FDCAN_ConfigGlobalFilter(&hfdcan1, FDCAN_REJECT, FDCAN_REJECT,

 FDCAN_FILTER_REMOTE, FDCAN_FILTER_REMOTE) != HAL_OK)

 {

 Error_Handler();

 }

 if (HAL_FDCAN_ActivateNotification(&hfdcan1, FDCAN_IT_RX_FIFO0_NEW_MESSAGE,

 0) != HAL_OK)

 {

 Error_Handler();

 }

 if (HAL_FDCAN_Start(&hfdcan1) != HAL_OK)

 {

 Error_Handler();

 }

 }

```

Receive the data sent by CAN in the interrupt.


Print out the data received by CAN. Data parsing and event processing functions can be added

here later.


![](18.CAN-bus-communication.pdf-3-0.jpeg)
![](18.CAN-bus-communication.pdf-4-0.jpeg)


The test sends a string of data via CAN and prints the data through the serial port. Each time it is

sent, the first data is automatically incremented by 1, and the other data remain unchanged.


![](18.CAN-bus-communication.pdf-4-1.jpeg)


Send test CAN data once per second.


![](18.CAN-bus-communication.pdf-4-2.jpeg)


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


Open the serial port assistant (specific parameters are shown in the figure below), and you can

see that the serial port assistant is constantly printing the data sent and received by CAN.


![](18.CAN-bus-communication.pdf-5-0.jpeg)

![](18.CAN-bus-communication.pdf-5-1.jpeg)
![](18.CAN-bus-communication.pdf-6-0.jpeg)
