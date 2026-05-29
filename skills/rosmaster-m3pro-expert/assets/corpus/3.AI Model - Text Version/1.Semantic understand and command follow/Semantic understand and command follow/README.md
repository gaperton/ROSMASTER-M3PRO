# Semantic Understanding and Command Following

#### Semantic Understanding and Command Following

- 1. Course Content
- 2. Preparation
  - 2.1 Content Description
  - 2.2 Starting the Agent
- 3. Running Examples
  - 3.1 Starting the Program
  - 3.2 Test Cases
    - 3.2.1 Case 1
    - 3.2.2 Case 2

# 1. Course Content

Run the example program and interact with the robot only through text in the terminal, without voice input or voice response.

# 2. Preparation

#### 2.1 Content Description

This section of the course uses the Jetson Orin NX as an example. For Raspberry Pi and Jetson Nano boards, you need to open a terminal on the host machine and then enter the command to enter the Docker container. After entering the Docker container, enter the commands mentioned in this section of the course in the terminal. For instructions on entering the Docker container from the host machine, please refer to the "Entering the Robot's Docker (For Jetson Nano and Raspberry Pi 5 Users)" section in the product tutorial [0. Instructions and Installation Steps]. For Orin and NX boards, simply open the terminal and enter the commands mentioned in this section of the course.

### 2.2 Starting the Agent

**Note: If the agent is already running, you do not need to start it again.**

Enter the following command in the vehicle's terminal:

```
sh start_agent.sh
```

The terminal will print the following information, indicating a successful connection:

# 3. Running Examples

#### 3.1 Starting the Program

Open a terminal on the vehicle's system and enter the following command:

```
ros2 launch multi_brains llm_agent_control.launch.py text_chat_mode:=True
```

Start the text interaction terminal. This can be started on either the vehicle's system or the virtual machine; **choose only one** method, do not start it on both the virtual machine and the vehicle's system:

```
ros2 run text_chat text_chat
```

#### 3.2 Test Cases

Here are some example test cases. Users can create their own dialogue commands.

- Please move forward 1 meter quickly, then slowly move backward 0.5 meters like a turtle, then turn left 30 degrees, turn right 90 degrees, then translate left 0.5 meters, and then translate right 10 centimeters.
- Please perform a dance, and then tell me a joke about cats and dogs.

#### 3.2.1 Case 1

Open a terminal in the virtual machine, enter the test case in the terminal, and after the model thinks, the AI agent will reply to the user and perform the actions according to the user's instructions.

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

#### 3.2.2 Case 2

Using the same method as Case 1, enter Case 2 in the terminal. The model will reply and perform the actions according to the instructions.

![Figure: page 2: figure 3](_page_2_Figure_3.jpeg)
