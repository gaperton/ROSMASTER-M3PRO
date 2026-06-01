# AI Model Development

This section shows how to prepare and develop the ROSMASTER-M3PRO large-model application stack. It covers model-provider accounts, API-key configuration, Dify basics, chatbot creation, local RAG knowledge bases, RAG-backed applications, AI agent workflows, wake-up response audio, and core module tests.

Use this section after the AI model basics when you need to connect model services, configure the robot's AI backend, build Dify applications, expand the robot's private knowledge base, or diagnose speech and Dify connectivity issues.

## [2.1 Model Provider Accounts and API Keys](./01.Register%20a%20model%20service%20provider%20account/1.Register%20a%20model%20service%20account/README.md)

Explains how to register with model service providers and create API keys so the robot can access cloud-based models. It covers Alibaba Cloud Model Studio account registration, free quota notes, and OpenRouter account and key creation for users who need alternate model services.

## [2.2 Configure Model API Access](./02.%20Configuring%20API-KEY/2.Configuring%20API-KEY/README.md)

Shows how to start the robot's Dify service, log in to the local Dify management page, configure a model-provider API key, test whether the key works, generate the `multi_brains` settings file, switch between online and local speech services, and modify Dify backend access settings for development needs.

## [2.3 Dify Platform Overview](./03.%20Introduction%20to%20Dify/3.%20Introduction%20to%20Dify/README.md)

Introduces Dify as the visual AI application platform used by the robot. It summarizes Dify's drag-and-drop application building, model-provider integration, multi-source data and vector indexing support, local RAG knowledge bases, and plugin ecosystem.

## [2.4 Dify Operations and Model Switching](./04.%20Basic%20Dify%20Features/Basic%20Dify%20Features/README.md)

Covers routine Dify operations on the robot, including starting the service, logging in, changing the interface language, installing model-provider plugins, configuring provider access, switching the models used by the `multi_brains` task-routing, decision, and execution layers, adjusting model parameters, publishing updates, and managing local account settings.

## [2.5 Build a Chatbot in Dify](./05.%20AI%20Large%20Model%20Development%20-%20chatbot/AI%20Large%20Model%20Development%20-%20chatbot/README.md)

Walks through creating a basic Dify chatbot from a blank app. It covers choosing the chat assistant template, writing a role prompt, selecting a model, testing responses, optionally enabling multimodal visual question answering, publishing the app, and accessing the chatbot through a web URL on the same network.

## [2.6 Deploy a Local RAG Knowledge Base](./06.%20Deploy%20the%20RAG%20knowledge%20base/Deploy%20the%20RAG%20knowledge%20base/README.md)

Explains how to inspect the robot's preset RAG knowledge bases and create new local knowledge bases in Dify. It covers importing files, selecting Economic or High-Quality indexing modes, reviewing chunking results, editing keywords or fragments, and using retrieval testing to check whether the knowledge base recalls the right content.

## [2.7 Connect RAG to a Chatbot](./07.%20RAG%20knowledge%20base%20%2B%20chatbot/RAG%20knowledge%20base%20%2B%20chatbot/README.md)

Builds on the chatbot and RAG lessons by combining a Dify chat application with a knowledge base. It includes a task-planning example that simulates the robot decision layer and a document-management example showing how private knowledge lets a model answer based on domain-specific materials instead of general training alone.

## [2.8 Build an AI Agent Workflow](./08.%20AI%20agent%20workflow/AI%20agent%20workflow/README.md)

Shows how to build and debug multi-model AI agent workflows in Dify. The lesson imports a sample DSL workflow, uses a question classifier to route math and physics questions to different model branches, previews branch execution in real time, expands the workflow with additional modules, and publishes the application for web or API access.

## [2.9 Customize Wake-Up Responses](./09.%20Custom%20wake-up%20response/Custom%20wake-up%20response/README.md)

Explains how to customize the audio response played after the robot wakes up. It covers preparing or generating voice files with `generate_voice`, configuring the required speech-synthesis API key, choosing voices and languages, and placing audio files into the `multi_brains` system voice directories for Chinese or English responses.

## [2.10 Test Core AI Modules](./10.%20Core%20module%20testing%20tools/Core%20Module%20Testing%20Tools/README.md)

Lists the minimal `multi_brains` test programs used to isolate AI module problems. It covers local speech synthesis, local speech recognition, Dify connectivity, domestic online voice services such as Bailian and Baidu, and international online voice services such as iFlytek speech recognition and synthesis.
