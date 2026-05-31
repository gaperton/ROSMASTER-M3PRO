# AI Agent Workflow

## 1. Course Content

Build AI agent workflows that use multiple large models to implement complex logical functions.

## 2. Start the Dify Service

Connect to the robot system through VNC or SSH, then run the following command in the terminal:

```bash
sh ~/bringup_dify.sh
```

Check the robot's IP address. You can view it on the OLED screen, use `ifconfig`, or check it directly in the terminal. Enter the robot's IP address directly in the browser address bar to open the Dify management page.

## 3. Case Study: Categorized Question-Answering Chatbot

- The example AI application folder for this lesson includes reference examples that can be imported and used directly.
- On the Dify home page, click **Import DSL File**.

![Figure: page 1: figure 3](_page_1_Figure_3.jpeg)

Select the example AI application file `Complex agent.yml` in this lesson's folder, then click **Create**.

![Figure: page 1: figure 5](_page_1_Figure_5.jpeg)

The workflow content appears as shown below.

![Figure: page 2: figure 0](_page_2_Figure_0.jpeg)

In the workflow, **Question Classifier** is driven by a large model. It classifies user questions into math questions, physics questions, and other questions. If the user's input matches a math- or physics-related question, the corresponding large-model branch is invoked to answer it. The categories in **Question Classifier** are shown below.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

The **LLM-1** branch answers math-related questions. Its prompt and settings are shown below.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

The **LLM-2** branch answers physics-related questions. Its prompt and settings are shown below.

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

## 4. Visualize and Debug Workflows

To debug and test the workflow, click the preview button in the upper-right corner, then enter a problem in the pop-up dialog box.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

At the same time, the workflow displays the branches through which data flows in real time, making debugging easier.

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

To expand the workflow, click the **+** sign on the left. This opens Dify's predefined tools and modules.

![Figure: page 7: figure 2](_page_7_Figure_2.jpeg)

## 5. Access AI Agent Applications

After arranging the AI application, click **Publish Application** to save the configuration. Then click **Copy URL** or **API Access Credentials** to access the application through the web interface or backend service API.

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)
