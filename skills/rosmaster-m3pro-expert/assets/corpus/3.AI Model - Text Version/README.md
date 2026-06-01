# AI Model - Text Version

This section demonstrates the ROSMASTER-M3PRO embodied-AI functions using terminal-based text interaction. It covers text command following, multimodal visual understanding, robotic-arm grasping, SLAM navigation, object-transfer tasks, and personalized intent understanding.

Use this section when you want to test the `multi_brains` AI agent without speech recognition or speech synthesis. The workflows are the same style as the voice version, but user commands are entered through the `text_chat` terminal.

## [3.1 Text Command Understanding and Action Execution](./1.Semantic%20understand%20and%20command%20follow/Semantic%20understand%20and%20command%20follow/README.md)

Shows how to run the text-mode AI agent and send natural-language commands from a terminal. The lesson covers starting the agent, launching `llm_agent_control` with `text_chat_mode:=True`, starting the `text_chat` node, and testing chained robot actions such as movement, rotation, translation, dancing, and conversational replies.

## [3.2 Text-Based Visual Understanding](./2.Multimodal%20visual%20understand/Multimodal%20visual%20understand/README.md)

Runs the text-input visual understanding example so the robot can observe the environment, answer questions about visible objects, and choose simple actions based on what it sees. It also explains the `seewhat` visual observation function and how image feedback is passed from `action_service.py` to the `multi_brains` model service.

## [3.3 Text-Guided Visual Grasping](./3.%20Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/README.md)

Combines text commands, multimodal visual understanding, and robotic-arm grasping. The lesson includes examples for finding and grasping a red cube, moving a block relative to another block, removing AprilTag blocks above a target height, and tracking AprilTags, then explains the related action functions such as `grasp_obj`, `set_cmdvel`, `putdown`, and `apriltag_remove_higher`.

## [3.4 Text-Guided Visual Navigation](./4.Multimodal%20visual%20understand%2BSLAM%20navigation/Multimodal%20visual%20understand%2BSLAM%20navigation/README.md)

Shows how to combine text interaction, visual understanding, and Nav2 SLAM navigation. It covers the prerequisite grid map, configuring named locations in `map_mapping.yaml`, updating the corresponding Dify session variables, launching the navigation stack and RViz, initializing the robot pose, and running a test where the robot remembers its start point, visits named locations, observes objects, and returns.

## [3.5 Text-Guided Navigation and Object Transfer](./5.Robotic%20arm%20gripping%2BMultimodal%20visual%20understand%2BSLAM%20navigation/README.md)

Runs a complex text-command task that combines navigation, visual understanding, and robotic-arm object handling. The example asks the robot to move one colored block from its starting area to the master bedroom, then find another block there and transfer it to the kitchen, demonstrating decision-layer planning and execution-layer action control across multiple locations.

## [3.6 Text-Based Personal Intent Understanding](./6.Intention%20estimation/Intention%20estimation/README.md)

Explains how to customize fuzzy user-intent understanding with a RAG knowledge base. It covers editing an intent mapping file, uploading it to Dify, using High-Quality retrieval for semantically similar user cues, launching the text-mode AI agent with navigation, and testing an example where a personal statement such as being thirsty is mapped to a multi-step robot task.
