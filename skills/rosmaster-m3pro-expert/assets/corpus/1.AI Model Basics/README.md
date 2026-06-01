# AI Model Basics

This section introduces the large-model concepts behind the ROSMASTER-M3PRO embodied-AI courses. It starts with the model types used in the system, explains why RAG and training examples are needed for robot decision-making, then describes Yahboom's `multi_brains` architecture and its core source-code modules.

Use this section before building or modifying AI workflows. It gives the background needed to understand later Dify, RAG, text-command, voice-command, visual-understanding, grasping, and navigation lessons.

## [1.1 Large Model Types and Core Principles](./1.AI%20large%20model%20types%20and%20principles/README.md)

Introduces AI large models as systems built from large datasets, computing power, and advanced training algorithms. It compares text-generation models, multimodal models, speech-recognition models, and speech-synthesis models, then summarizes their inputs, outputs, core technologies, and typical robot-relevant use cases.

## [1.2 RAG Retrieval and Training Examples](./2.RAG%20retrieval%20enhancement%20and%20model%20training%20samples/README.md)

Explains large-model hallucination and why it matters for embodied AI, where incorrect environment understanding or action planning can cause the robot to behave unexpectedly. It introduces RAG as a "retrieve first, generate second" workflow, then explains how knowledge bases and training examples reduce hallucinations, improve scenario generalization, reduce prompt length, and make robot capabilities easier to expand.

## [1.3 `multi_brains` Embodied AI Architecture](./3.Embodied%20intelligent%20robot%20system%20architecture/README.md)

Describes Yahboom's `multi_brains` embodied-intelligence framework for connecting the robot to general-purpose large models. It covers the dual-model inference architecture, the separation between decision-layer planning and execution-layer action conversion, task-cycle memory, Dify-backed history, map mapping between real-world areas and navigation coordinates, and the action function library that lets the model control the robot through JSON actions.

## [1.4 `multi_brains` Core Source Code Walkthrough](./4.Embodied%20intelligent%20functions%20core%20source%20code/README.md)

Walks through the main `multi_brains` package structure for users who want to understand how the AI functions are implemented. It covers configuration files, launch files, language resources, system audio, speech recognition in `asr_detect.py`, model inference in `model_service.py`, robot-action execution in `action_service.py`, and interruption handling across recording, dialogue, and action stages.
