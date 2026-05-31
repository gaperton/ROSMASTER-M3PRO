# Robotic Arm Grasping + Multimodal Visual Understanding + SLAM Navigation

## 1. Course Content

- Run the example program and combine Nav2 navigation, robotic arm grasping, and large-model visual understanding to perform complex tasks.
- **This chapter requires the map mapping file to be configured first.**

> [!NOTE]
> The text version differs from the voice version only in the instruction input method. The text version does not require speech recognition or speech synthesis.

## 2. Start the Agent

The Docker agent must be started before testing. If it is already running, you do not need to start it again.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

## 3. Run the Case

### 3.1 Start the Program

Open a terminal on the robot and run:

```bash
ros2 launch multi_brains llm_agent_control.launch.py text_chat_mode:=True
```

Start the text interaction node:

```bash
ros2 run text_chat text_chat
```

### 3.2 Test Case

The following is a reference test case. You can also create your own instructions.

```text
Please help me move the red block in front of you to the master bedroom, and then move the green block from the master bedroom to the kitchen.
```

Wooden blocks used: 30 x 30 x 30 mm blocks.

Enter the test case in the text interaction terminal.

The decision-layer large language model plans the task steps, and the execution-layer large language model executes those steps.

The robot first grasps the red block in front of it.

![Figure: page 2: figure 2](_page_2_Figure_2.jpeg)

Then it navigates to the **bedroom** and uses the robotic arm to put down the red block.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

After observing, finding, and grasping the green block in the **master bedroom**, it moves to the **kitchen**.

![Figure: page 3: figure 2](_page_3_Figure_2.jpeg)

After putting down the green block in the **kitchen**, the robot reports that the task is complete and enters a waiting state. Enter `End current task` in the interaction terminal to end the task.
