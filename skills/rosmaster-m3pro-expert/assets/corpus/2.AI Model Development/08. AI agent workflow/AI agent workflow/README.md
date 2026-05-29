# AI Agent Workflow

## 1. Course Content

Build intelligent agent workflows using multiple large AI models to implement complex logical functions.

## 2. Start the Dify Service

Connect to the car's infotainment system via VNC or SSH. Enter the following command in the terminal:

```
sh ~/bringup_dify.sh
```

Check the car's IP address. You can do this through the OLED screen, using ifconfig, or directly in the terminal. Enter the car's IP address directly into your browser's address bar to access the Dify management page.

## 3. Case Study: Categorized Question-Answering Chatbot

- In the example AI application folder of this lesson, there are reference examples that can be directly imported and used.
- In the Dify homepage studio, click "Import DSL File".

![Figure: page 1: figure 3](_page_1_Figure_3.jpeg)

Select the example AI application Complex agent.yml in the course folder for this section, and then click "Create".

![Figure: page 1: figure 5](_page_1_Figure_5.jpeg)

You can see the workflow content as shown below.

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

In the workflow, Question Classifier is a module driven by a large AI model. Its function is to categorize user questions into math questions, physics questions, and other questions. If the user's input matches a math or physics-related question, it will invoke the corresponding branch of the large AI model to answer it. The categories in Question Classifier are as follows:

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

The LLM-1 branch is used to answer math-related questions. The prompt and settings are shown below.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

The LLM-2 branch is used to answer physics-related questions. The prompt and settings are shown below.

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

## 4. Visualizing and Debugging Workflows

To debug and test the workflow, click the preview in the upper right corner, and then enter the problem in the pop-up dialog box for testing.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

Simultaneously, the workflow will display the branches through which data flows in real time, thus facilitating workflow debugging.

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

To expand your workflow, click the "+" sign on the left, which provides access to several predefined tools and modules for Dify.

![Figure: page 7: figure 2](_page_7_Figure_2.jpeg)

## 5. Accessing AI Agent Applications

After orchestrating your AI application, click "Publish Application" to save the configuration. Then, click "Copy URL" or "API Access Credentials" to access the created AI application via the web interface or backend service API.

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)
