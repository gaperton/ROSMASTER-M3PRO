# AI Model - Voice Version

This section demonstrates the ROSMASTER-M3PRO embodied-AI functions through voice interaction. It covers spoken command following, multimodal visual understanding, robotic-arm grasping, SLAM navigation, object-transfer tasks, and personalized intent understanding with speech recognition and speech synthesis in the loop.

Use this section when you want to run the full `multi_brains` voice workflow. Compared with the text version, these lessons add wake-up interaction, microphone and VAD behavior, ASR/TTS configuration effects, spoken prompts, and voice-specific troubleshooting.

## [4.1 Voice Command Understanding and Action Execution](./1.Semantic%20understand%20and%20command%20follow/Semantic%20understand%20and%20command%20follow/README.md)

Shows how to run the voice-mode AI agent so spoken user commands are converted to text, interpreted by the model system, executed by the robot, and answered with voice output. It covers starting the agent, launching `llm_agent_control` or the `multi_brains` shortcut, waking the robot with `Hello yahboom`, testing chained motion and conversation tasks, and adjusting microphone or VAD sensitivity when recording is too sensitive or not sensitive enough.

## [4.2 Voice-Based Visual Understanding](./2.Multimodal%20visual%20understand/Multimodal%20visual%20understand/README.md)

Runs the voice-input visual understanding example so the robot can observe the environment and respond to spoken questions or instructions. The lesson demonstrates wake-up, dynamic sound detection, short-term task memory, object-description prompts, visual condition checks, and the same `seewhat` image-feedback path used by the text version, with speech recognition and speech synthesis wrapped around the interaction.

## [4.3 Voice-Guided Visual Grasping](./3.%20Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/Multimodal%20Large%20Model%2Brobotic%20arm%20gripping/README.md)

Combines spoken commands, multimodal visual understanding, and robotic-arm grasping. It includes voice-command cases for finding and picking up a red cube, moving a cube relative to another cube, and removing AprilTag blocks above a target height, then explains the related grasping flow through `seewhat`, `grasp_obj`, target bounding-box coordinates, and the arm-tracking subprocesses.

## [4.4 Voice-Guided Visual Navigation](./4.Multimodal%20visual%20understand%2BSLAM%20navigation/Multimodal%20visual%20understand%2BSLAM%20navigation/README.md)

Shows how to combine voice interaction, visual understanding, and Nav2 SLAM navigation. It covers the required grid map, configuring named locations in `map_mapping.yaml`, updating the Dify `map_mapping` session variable, launching navigation and RViz, initializing the robot pose, and speaking a task that asks the robot to remember its start point, visit named locations, observe objects, and return.

## [4.5 Voice-Guided Navigation and Object Transfer](./5.Robotic%20arm%20gripping%2BMultimodal%20visual%20understand%2BSLAM%20navigation/README.md)

Runs a complex spoken task that combines Nav2 navigation, visual understanding, robotic-arm grasping, and object placement. The example asks the robot to bring a red cube to the master bedroom, showing how the decision layer plans the steps, the execution layer observes and grasps the object, navigation moves to the target, and `putdown` releases the object before the robot waits for the next voice instruction.

## [4.6 Voice-Based Personal Intent Understanding](./6.Intention%20estimation/Intention%20estimation/README.md)

Explains how to customize fuzzy personal-intent understanding for spoken interaction using a RAG knowledge base. It covers editing an intent mapping file, uploading it to Dify, using High-Quality retrieval for semantically similar cues, running the voice agent with navigation, testing a spoken personal statement such as being thirsty, and debugging intent classification, workflow data flow, and knowledge-base recall in Dify.
