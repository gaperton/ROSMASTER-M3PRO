# Intent Understanding

## 1. Course Content

Learn how to customize user intent understanding through the RAG knowledge base.

> [!IMPORTANT]
> Intent understanding is designed to improve rapport between the robot and the user so the robot can better understand the user's needs. Do not use this function for unusual or unsafe tasks.

## 2. Start the Agent

If the agent is already running, you do not need to start it again.

Run the following command in the robot terminal:

```bash
sh start_agent.sh
```

The terminal prints connection information when the agent connects successfully.

### 2.1 Configure the Intent Mapping File

This file stores fuzzy personal intents and the corresponding tasks the robot should perform.

Open the example file in this lesson's folder. You can add multiple custom intents by following the reference format. A simple example is shown below.

| Query                | Answer                                                                                                                                                                    |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| I'm a little thirsty | 1. Navigate to the kitchen. 2. Check for bottled water or drinks. 3. If available, use the robotic arm to pick up the drink. 4. Navigate back to the starting position. |

### 2.2 Configure the Knowledge Base

Next, upload the edited intent mapping file to the Dify RAG knowledge base.

> [!NOTE]
> For detailed RAG knowledge base instructions, see **2. AI Model Development - 06 - Deploy the RAG knowledge base**.
>
> Dify includes a sample **Intent mapping** knowledge base to demonstrate the intent understanding feature.

![Picture: page 1: picture 4](_page_1_Picture_4.jpeg)

You can modify the `Intent mapping.xlsx` template, or delete it and add your own file.

![Picture: page 1: picture 6](_page_1_Picture_6.jpeg)

> [!TIP]
> For best intent understanding results, set the **Intent mapping** knowledge base to High-Quality mode. Intent understanding often requires retrieving relevant snippets from semantically similar cues.

## 3. Run the Example

### 3.1 Start the Program

On the robot computer, open a terminal and start the AI agent in text mode:

```bash
ros2 launch multi_brains llm_agent_control.launch.py text_chat_mode:=True
```

On the robot computer, open two more terminals and start the navigation nodes:

```bash
ros2 launch M3Pro_navigation base_bringup.launch.py
```

```bash
ros2 launch M3Pro_navigation navigation2.launch.py
```

Start RViz on the robot:

```bash
ros2 launch M3Pro_navigation nav_rviz.launch.py
```

Initialize navigation in RViz by clicking **2D Pose Estimate** and roughly marking the robot's position and orientation on the map. After initialization, preparation is complete.

![Picture: page 3: picture 3](_page_3_Picture_3.jpeg)

Start the text interaction node:

```bash
ros2 run text_chat text_chat
```

### 3.2 Test Case

The following is a reference test case. You can also create your own dialogue commands.

```text
I'm in the master bedroom, and I'm a little thirsty.
```

Enter the test case in the text interaction terminal. The decision-layer model plans the task steps, and the execution-layer model executes them in sequence.

When the robotic arm grasps an object, a visualization window is displayed. Note: the factory preset gripper size is for a 3 cm cube. Gripping bottled water here is only a demonstration. To grasp objects of other sizes, modify the gripper opening angle.

![Picture: page 4: picture 3](_page_4_Picture_3.jpeg)

After arriving at the **master bedroom**, the robot uses the robotic arm to put down the red cube and reports that the task is complete.
