# Configuring the API Key

## 1. Course Content

Use the previously registered API key to configure the robot car's API key.

[!WARNING]

**Note**: Please ensure the car is connected to the internet to use the cloud-based model services.

## 2. Starting the Dify Service

[!TIP]

ROSMASTER-M3 Pro uses Dify to build a multi-agent system, with Dify managing the calls to the cloud-based models. - Connect to the vehicle's system via VNC or SSH, and enter the following command in the terminal:

bringup_dify

View the vehicle's IP address. This can be done via the OLED screen or by using ifconfig in the terminal.

Enter the vehicle's IP address directly into your browser's address bar to access the Dify management page. If this is the first time logging in, you will need to use the account and password. You can select the language in the upper left corner.

### [!NOTE]

- Account name: yahboom@163.com
- Password: yahboom123
- All account passwords, intelligent agent applications, and RAG data are stored locally.
- After logging in, the page will look like this:

![Picture: page 1: picture 7](_page_1_Picture_7.jpeg)

## 3. Configuring the Model Service Provider API Key

Click Settings

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

Here, we'll use configuring the Alibaba Cloud Model Studio Platform account API as an example. Click Model Provider -> Setup

![Picture: page 2: picture 2](_page_2_Picture_2.jpeg)

Enter your Alibaba Cloud Model Studio Platform API key, then select whether it's an international account, and click Save.

![Picture: page 3: picture 0](_page_3_Picture_0.jpeg)

## 4. Testing the API Key

[!TIP]

- If you need to test whether your API key is valid, you can refer to this section of the tutorial. Otherwise, you can skip it.
- Click on the "TEST_API" application in the studio.

![Picture: page 3: picture 5](_page_3_Picture_5.jpeg)

Then, select any model in the model selection to test.

![Figure: page 3: figure 7](_page_3_Figure_7.jpeg)

Enter any content in the chat box. If the registered API key is valid, you will see the model's response.

![Picture: page 4: picture 1](_page_4_Picture_1.jpeg)

## 5. Configuring the multi_brains Function Package API

Generate the parameter file by running the following commands in the terminal:

```bash
cd ~/M3Pro_ws/multi_brains_file
cp .multi_brains_setting_example_en.yaml multi_brains_setting.yaml
```

If you later use Alibaba Cloud's speech synthesis service to generate a custom voice file, please apply for an API-KEY from Alibaba Cloud International and fill in ALIYUN_API_KEY. **This does not affect normal use; you can ignore this if you don't need it.**

![Figure: page 4: figure 6](_page_4_Figure_6.jpeg)

## 6. Using Local Speech Services

- By default, online speech services are used for speech recognition and speech synthesis. If you need to use local speech services, please refer to this section of the tutorial; otherwise, you can skip this section.
- Note that due to memory and performance limitations, local speech services are not currently available on Jetson Nano.

### 6.1 Local Speech Recognition

```bash
nano ~/M3Pro_ws/multi_brains_file/multi_brains_setting.yaml
```

- Find the USE_ONLINE_ASR option in the ASR function setting section and set it to False. Save and exit with Ctrl+x to enable local speech recognition.
- Other parameters are used to configure some parameters of the recording process. See the comments for details on the function of each parameter. Beginners can use the default settings.

```
####################
#ASR function setting
#Speech Recognition Function Settings
####################
USE_OLINE_ASR : False # Whether to use online
ASR
ASR_SUPPLIER : 'xunfei' #ASR Supplier (only
effective when using online ASR): Chinese mainland: aliyun International: xunfei
OLINE_ASR_MODEL : 'paraformer-realtime-v2'
ASR_THREASHOLD : 3 # ASR recognition result
threshold, unit: characters
WAKEUP_THREASHOLD : 5.0 # Wake-up time threshold, to
prevent multiple wake-ups within WAKEUP_THREASHOLD time, unit: seconds
VAD_MODE: 1 # VAD sensitivity
MAX_SILENCE_FRAMES: 90 # Tail sound duration
detection, unit: frames
```

### 6.2 Local Speech Synthesis

```bash
nano ~/M3Pro_ws/multi_brains_file/multi_brains_setting.yaml
```

Find the USE_OLINE_TTS option in the TS function setting section and set it to False. Save and exit with Ctrl+x to enable local speech synthesis.

```
####################
#TTS function setting
#Speech Synthesis Function Settings
####################
USE_OLINE_TTS : False
# Whether to use online TTS
... .
```

## 7. Modifying the Dfiy Service API

- **Note**: This section is for users with development needs only and can generally be ignored.
- If you need to modify the address that the vehicle's infotainment system uses to access the Dify application's API, or if Dify is deployed on a different server, you need to modify the access address in the configuration file:

```bash
nano ~/M3Pro_ws/multi_brains_file/multi_brains_setting.yaml
```

- Find the DIFY_API_KEY and DIFY_BASE_URL parameters, where:
- DIFY_BASE_URL is the address for accessing the Dify backend service.
- DIFY_API_KEY is the API key for the AI application in Dify.

```
####################
# dify setting
# dify configuration options
####################
DIFY_BASE_URL: "http://localhost/v1"
DIFY_API_KEY: "app-mhawRyoHteauIho7wvXhlhwR" # Dify application
API_KEY
```
