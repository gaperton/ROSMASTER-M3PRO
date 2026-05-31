# Semantic Understanding and Command Following

## 1. Course Content

Run the large language model program and interact with the robot through voice conversation. The user's voice command is converted into text by the speech recognition model. Then the text generation model and visual multimodal model understand the user's instruction, the robot performs the specified actions, and the robot responds to the user.

## 2. Preparation

### 2.1 Content Description

This lesson uses Jetson Orin NX as the example. For Raspberry Pi and Jetson Nano boards, open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For instructions, see **Entering the Robot Docker Container (for Jetson Nano and Raspberry Pi 5 users)** in **0. Configuration and Operation Guide**.

For Orin and NX boards, open a terminal directly on the robot and run the commands from this lesson.

### 2.2 Start the Agent

The Docker agent must be started before testing. If it is already running, you do not need to start it again.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

## 3. Run the Cases

### 3.1 Start the Program

Open a terminal on the robot and run:

```bash
ros2 launch multi_brains llm_agent_control.launch.py
```

Alternatively, use the shortcut command:

```bash
multi_brains
```

After initialization, the startup information is displayed.

### 3.2 Test Cases

The following are example test cases. You can also create your own voice commands.

- Please move forward quickly for 1 meter, then slowly move backward 0.5 meters like a turtle, then turn left 30 degrees, turn right 90 degrees, then translate left 0.5 meters, and then translate right 10 centimeters.
- Please perform a dance, and then tell me a joke about cats and dogs.

#### 3.2.1 Case 1

Wake the robot by saying `Hello yahboom`. The robot responds. After the recording prompt, speak your command. The robot performs dynamic sound detection. If voice activity is detected, the terminal prints `1-1-1-1`; if no voice activity is detected, it prints `---------`. After you finish speaking, end-of-speech detection runs. If silence lasts more than 1.5 seconds, recording stops.

The robot first responds to the user, then performs actions according to the instruction. The terminal prints the model response and action list.

The action list includes `finish()`.

#### 3.2.2 Case 2

As in Case 1, wake the robot and speak the command. The robot responds and performs a dance according to the instruction.

## 4. Code Analysis

This lesson uses the basic embodied AI program framework. For code analysis, see **1. AI Model Basics - 4. Embodied intelligent functions core source code**.

## 5. Common Problems

### 5.1 Microphone Recording Is Too Sensitive

If **VAD (Voice Activity Detection)** continuously displays `1-1-1-1` after you finish speaking, VAD is too sensitive. Adjust the microphone sensitivity first. Software-level sensitivity adjustment is usually not necessary.

Connect to the robot computer screen through VNC, click the options bar in the upper-right corner, and open **Settings**.

> [!NOTE]
> Raspberry Pi and Jetson Nano models use a similar method. Both adjust microphone sensitivity from the upper-right settings area, although the UI style may differ.

![Picture: page 4: picture 5](_page_4_Picture_5.jpeg)

In the left **Settings** list, open **Sound**. On the **Sound** page, find **Input** and **Input Device**. Drag the **Volume** slider to adjust sensitivity while recording.

![Figure: page 4: figure 7](_page_4_Figure_7.jpeg)

### 5.2 Microphone Recording Is Not Sensitive Enough

If the speaker is far from the robot, VAD may fail to detect voice activity and may stop recording before the speaker finishes. In this case, follow the steps in **5.1 Microphone Recording Is Too Sensitive** and increase microphone sensitivity appropriately.

> [!NOTE]
> If microphone sensitivity is too high, environmental noise may be misidentified as voice activity.

### 5.3 Adjust Speech Recognition Sensitivity in Software

The `multi_brains` configuration file path is:

```text
~/M3Pro_ws/multi_brains_file/multi_brains_setting.yaml
```

Find the `VAD_MODE` parameter. The valid range is 1-3. A higher value means higher VAD sensitivity.

```yaml
####################
# ASR function setting
####################
USE_OLINE_ASR : True # Whether to use online ASR
ASR_SUPPLIER : 'aliyun' # ASR supplier. Online ASR only. Chinese mainland: aliyun; international: xunfei
OLINE_ASR_MODEL : 'paraformer-realtime-v2'
ASR_THREASHOLD : 3 # ASR recognition result threshold, unit: characters
WAKEUP_THREASHOLD : 5.0 # Wake-up threshold, prevents repeated wake-ups within this time, unit: seconds
VAD_MODE: 1 # VAD sensitivity
MAX_SILENCE_FRAMES: 90 # End-of-speech silence duration, unit: frames
```
