# AI Agent Workflow
**AI Agent Workflow**

1. Course Content

2. Start the Dify Service

3. Case Study: Categorized Question-Answering Chatbot

4. Visualizing and Debugging Workflows

5. Accessing AI Agent Applications

## 1. Course Content
Build intelligent agent workflows using multiple large AI models to implement complex

logical functions.
## 2. Start the Dify Service
Connect to the car's infotainment system via VNC or SSH. Enter the following command in

the terminal:


![](AI-agent-workflow.pdf-0-1.jpeg)

Check the car's IP address. You can do this through the OLED screen, using `ifconfig`, or

directly in the terminal. Enter the car's IP address directly into your browser's address bar to

access the Dify management page.


![](AI-agent-workflow.pdf-0-2.jpeg)
## 3. Case Study: Categorized Question-Answering
**Chatbot**


In the example AI application folder of this lesson, there are reference examples that can be

directly imported and used.

In the Dify homepage studio, click "Import DSL File".


and then click "Create".


You can see the workflow content as shown below.


![](AI-agent-workflow.pdf-1-0.jpeg)

![](AI-agent-workflow.pdf-1-2.jpeg)
![](AI-agent-workflow.pdf-2-0.jpeg)

In the workflow, `Question Classifier` is a module driven by a large AI model. Its function is

to categorize user questions into math questions, physics questions, and other questions. If

the user's input matches a math or physics-related question, it will invoke the corresponding


follows:


![](AI-agent-workflow.pdf-3-0.jpeg)

The LLM-1 branch is used to answer math-related questions. The prompt and settings are

shown below.


![](AI-agent-workflow.pdf-4-0.jpeg)

The LLM-2 branch is used to answer physics-related questions. The prompt and settings are

shown below.


![](AI-agent-workflow.pdf-5-0.jpeg)
## 4. Visualizing and Debugging Workflows
To debug and test the workflow, click the preview in the upper right corner, and then enter

the problem in the pop-up dialog box for testing.


![](AI-agent-workflow.pdf-6-0.jpeg)

Simultaneously, the workflow will display the branches through which data flows in real time,

thus facilitating workflow debugging.


![](AI-agent-workflow.pdf-7-0.jpeg)

To expand your workflow, click the "+" sign on the left, which provides access to several pre
defined tools and modules for Dify.

## 5. Accessing AI Agent Applications
After orchestrating your AI application, click "Publish Application" to save the configuration.

Then, click "Copy URL" or "API Access Credentials" to access the created AI application via the

web interface or backend service API.


![](AI-agent-workflow.pdf-7-1.jpeg)
![](AI-agent-workflow.pdf-8-0.jpeg)
