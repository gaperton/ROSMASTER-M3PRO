# Multi-Agent Embodied Architecture (`multi_brains`)

## 1. Course Content

This course introduces the `multi_brains` multi-agent embodied intelligence architecture used by ROSMASTER-M3 Pro.

## 2. Introduction to `multi_brains`

- `multi_brains` is an embodied intelligence framework developed by Yahboom for general-purpose AI large models. It avoids some limitations of VLA and end-to-end models, which often require dedicated hardware, strong local computing power, and long data-collection and training cycles. By connecting to general-purpose cloud AI models, the edge-side robot can gain powerful embodied intelligence capabilities.
- `multi_brains` extends training examples through a RAG knowledge base, allowing the robot to adapt quickly to different scenarios and tasks. It can run on most small main-control devices while offloading large-model inference to the cloud or to a local server.
- The core idea of `multi_brains` is to decouple different task stages through multiple AI models. It improves on the first-generation dual-model inference framework in several ways:
- A smoother recording experience, with inertial end-of-speech detection and adjustable end-of-speech duration.
- A more flexible decision-making mechanism, adding task-routing capability. The AI agent can independently choose dual-model or single-model inference based on task difficulty, giving the AI greater autonomy and improving the user experience.
- An easier-to-understand visual architecture. `multi_brains` uses Dify to build a visual AI agent, so users can observe the AI agent's operation and data flow in real time during debugging.
- A fully local RAG knowledge base, reducing concerns about sensitive data.
- Seamless integration with most global AI models. Through Dify model-provider plugins, hundreds of AI models can be integrated quickly. Local models can also be integrated if needed.
- Traceable history. By querying Dify backend access history, users can view task instructions and the robot's execution steps.
- Personalized response voices. Users can customize random response voices. The built-in speech synthesis commands are easy to configure and use.
- A comprehensive testing toolbox for quickly verifying core function modules.
- Simpler setup steps, with most operations simplified and shortcut commands provided.

## 3. Dual-Model Inference Architecture

The **dual-model inference** and **dynamic feedback inference** design provides stronger system robustness than a single-model architecture.

![Figure: page 1: figure 5](_page_1_Figure_5.jpeg)

### 3.1 Advantages of Dual-Model Inference

#### 3.1.1 Decoupling Task Decisions from Action Conversion

- The decision layer AI focuses on reasoning, planning, and decomposing task instructions.
- The execution layer AI focuses on chat responses and converting task steps into JSON text.

#### 3.1.2 Improving the Success Rate of Long Tasks

In single-model inference, one model must perform natural-language understanding, environmental perception, process decomposition, and action-function output at the same time. This can easily cause modal interference, where language ambiguity or overly long instructions lead to misinterpretation. The dual-model approach separates the process into stages, allowing the decision layer to focus on task planning and the execution layer to focus on action execution.

### 3.2 Decision Layer AI

The decision layer large language model is mainly responsible for task planning. It can understand complex human instructions and break them down into specific task steps. For example, when it receives the instruction "Can you get me a bottle of mineral water from the kitchen?", the large language model breaks it into several tasks, as shown below.

![Figure: page 1: figure 14](_page_1_Figure_14.jpeg)

### 3.3 Execution Layer AI

- The execution layer large language model is mainly responsible for chat responses and for converting task steps into JSON text. It continuously receives action feedback, such as success or failure, and images from the robot. Based on this feedback, it decides the next action.
- The execution layer large language model acts as a supervisor. It monitors the robot's progress, evaluates feedback and environmental information, and chooses the next action until the task is completed or terminated because of special circumstances.

![Figure: page 2: figure 3](_page_2_Figure_3.jpeg)

## 4. Task Cycle

- After the robot is awakened, a task cycle begins. User commands and robot feedback are included in the AI model's historical context. This acts as temporary memory, allowing the robot to "remember" what happened earlier in the task.
- When the user asks the robot to end the current task and rest, the robot resets the AI model's historical context. This causes the robot to "forget" the previous task and start fresh.

![Figure: page 2: figure 7](_page_2_Figure_7.jpeg)

## 5. Historical Context

The robot's conversation history is stored in Dify AI application variables. By default, the maximum conversation memory is 50 turns.

![Figure: page 3: figure 2](_page_3_Figure_2.jpeg)

## 6. Map Mapping

The robot uses a grid map for navigation. If the robot needs to understand real-world location areas, a mapping relationship must be established between the grid map and the real-world environment. This relationship is called **map mapping**.

Assume a robot is used in a factory environment and generates a **grid map** through SLAM mapping. In the real factory, several manually defined areas exist, as shown below.

![Picture: page 3: picture 5](_page_3_Picture_5.jpeg)

We establish a one-to-one correspondence between these real-world areas and letter symbols:

A: "Area 1", B: "Area 2", C: "Area 3", D: "Area 4", E: "Area 5", F: "Area 6", G: "Area 7", H: "Area 8", I: "Area 9"

Then we write the map coordinates for each letter symbol in a YAML file, for example:

```yaml
A:
name: 'Area 1'
position:
  x: 4.4034953117370605
  y: 0.4879316985607147
orientation:
  x: 0.0
  y: 0.0
  z: 0.701498621044694
  w: 0.7126708108744126
```

When the robot needs to go to a specific real-world area, the large language model converts the area name into the corresponding letter symbol. This allows the robot to understand the target location in the real-world environment.

## 7. Action Function Library

- The API functions in the robot action function library are the bridge that allows the large language model to control the robot and interact with the real world.
- These API functions define the minimum actions that the physical robot can perform.
- The AI large language model sends required actions to the robot as JSON text. The robot parses the JSON text and executes the corresponding actions.

![Figure: page 4: figure 6](_page_4_Figure_6.jpeg)

The minimum action functions and their meanings are shown below.

| Function name                                      | Parameters                                                                                                                       | Functionality                                                                      | Calling command                         |
|----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------|-----------------------------------------|
| `move_left(x, angular_speed)`                      | `x`: rotation angle, `angular_speed`: angular velocity                                                                           | Rotate left by `x` degrees                                                         | Rotate left by `x` degrees              |
| `move_right(x, angular_speed)`                     | `x`: rotation angle, `angular_speed`: angular velocity                                                                           | Rotate right by `x` degrees                                                        | Rotate right by `x` degrees             |
| `dance()`                                          | -                                                                                                                                | Trigger the robot's preset dance movements                                         | Dance, perform a dance, etc.            |
| `set_cmdvel(linear_x, linear_y, angular_z, duration)` | `linear_x`: x-axis linear velocity, `linear_y`: y-axis linear velocity, `angular_z`: z-axis angular velocity, `duration`: topic publishing duration | Control chassis movement by setting linear and angular velocities                  | Move forward, backward, left, or right  |
| `navigation(x)`                                    | `x`: symbol corresponding to the target point in the map mapping                                                                 | Navigate to the target point                                                       | Navigate to a location                  |
| `navigation(zero)`                                 | `zero`: recorded coordinate point                                                                                                | Navigate back to the previously recorded coordinate point                          | Return to the origin or starting point  |
| `get_current_pose()`                               | -                                                                                                                                | Record the current global-map coordinates to the `zero` parameter                  | Remember the current position           |
| `arm_up()`                                         | -                                                                                                                                | Move the robotic arm upward                                                        | Robotic arm up                          |
| `arm_down()`                                       | -                                                                                                                                | Move the robotic arm downward                                                      | Robotic arm down                        |
| `arm_nod()`                                        | -                                                                                                                                | Make the robotic arm nod                                                           | Nod                                     |
| `arm_shake()`                                      | -                                                                                                                                | Make the robotic arm shake                                                         | Shake head                              |
| `arm_applaud()`                                    | -                                                                                                                                | Make the robotic arm applaud                                                       | Applaud                                 |

| Function name                         | Parameters                                                                                                     | Functionality                                                                    | Calling command                                                  |
|---------------------------------------|----------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|------------------------------------------------------------------|
| `grasp_obj(x1, y1, x2, y2)`           | `x1`, `y1`, `x2`, `y2`: top-left and bottom-right coordinates of the target object's bounding box               | Grasp an object with the robotic arm                                             | Grasp xxx                                                        |
| `putdown()`                           | -                                                                                                              | Put down the object                                                              | Put down                                                         |
| `apriltag_sort(x)`                    | `x`: AprilTag ID                                                                                               | Sort the AprilTag with the specified ID                                          | Sort AprilTag number `x`                                         |
| `track(x1, y1, x2, y2)`               | `x1`, `y1`, `x2`, `y2`: top-left and bottom-right coordinates of the target object's bounding box               | Track the specified object in the field of view                                  | Track xx                                                         |
| `apriltag_remove_higher(x)`           | `x`: height                                                                                                    | Remove AprilTags above the specified height                                      | Remove AprilTags higher than `x` centimeters                     |
| `color_remove_higher(color, target_high)` | `color`: target color, `target_high`: target height                                                            | Remove color blocks above the specified height                                   | Remove `color` blocks higher than `target_high` centimeters      |
| `seewhat()`                           | -                                                                                                              | Capture the robot's current view and upload it to the execution layer model      | Observe the environment                                          |
| `follw_line_clear()`                  | -                                                                                                              | Follow the patrol line and clear AprilTag obstacles on the path                  | Start line clearing                                              |

| Function name       | Parameters | Functionality                                                                                  | Calling command |
|---------------------|------------|------------------------------------------------------------------------------------------------|-----------------|
| `finish_dialogue()` | -          | Reset historical context and start a new task cycle                                            | -               |
| `finish()`          | -          | Automatically called after the robot completes a task; stops feedback to the execution layer AI | -               |
