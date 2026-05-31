# AI Application Development: Chatbot

## 1. Course Content

Learn how to use Dify to quickly develop a chatbot.

## 2. Start the Dify Service

Connect to the robot computer through VNC or SSH, then run the following command in the terminal:

```bash
bringup_dify
```

Check the robot's IP address. You can view it on the OLED screen, use `ifconfig`, or check it directly in the terminal. Enter the robot's IP address directly in the browser address bar to open the Dify management page.

## 3. Chatbot

On the home page, click **Create from Blank**.

![Picture: page 1: picture 1](_page_1_Picture_1.jpeg)

Select **Chat Assistant** under **Beginner-friendly** Chatbot, set the **App Name & Icon**, then click **Create**.

![Picture: page 1: picture 3](_page_1_Picture_3.jpeg)

Enter the role prompt in **INSTRUCTIONS**.

![Figure: page 1: figure 5](_page_1_Figure_5.jpeg)

Example prompt:

### Role Definition

You are a friendly, patient, and talkative general-purpose chatbot named "Yahboom". Your core goal is to have natural and relaxed daily conversations with users and give them a pleasant conversation experience.

#### Conversation Rules

1. Tone: Keep a friendly and natural tone, like talking to a friend. Avoid overly formal or mechanical expressions.
2. Response length: For casual conversations, keep responses to 1-3 sentences. For complex questions, you may explain more, but avoid unnecessarily long responses.
3. Boundaries: If the user asks about something you do not know, say honestly that you do not know and try to provide relevant suggestions. Do not fabricate information. If the user makes an inappropriate request, politely decline and guide the conversation back to a normal topic.
4. Logic: Follow the conversation context, stay on topic, and adjust your response style based on the user's tone. Match humor with humor and stay serious when the user is serious.

#### Start Conversation

Please respond to each user message according to the settings above.

Then select the AI model. This example uses `qwen-max`, with parameters kept at their default settings.

> [!TIP]
> To add visual question-answering, select a multimodal model and enable the visual switch.
>
> To save application changes, click **Publish**.

![Figure: page 2: figure 14](_page_2_Figure_14.jpeg)

Enter test content in the chat box on the right to view the model response.

> [!TIP]
> If you are not satisfied with the model response, adjust the prompt and model parameters to fine-tune the result.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

## 4. Access the Chatbot on the Web

- There are two ways to access the AI application: web access and backend API access. This example uses web access.
- Click the chatbot settings button on the left.

![Figure: page 3: figure 4](_page_3_Figure_4.jpeg)

Copy the public access URL of the web app.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

Paste the link into your browser address bar to access the chatbot web interface.

> [!TIP]
> Any device on the same network segment as the robot system can access this page. Dify can also be deployed on a separate server.

![Picture: page 5: picture 0](_page_5_Picture_0.jpeg)
