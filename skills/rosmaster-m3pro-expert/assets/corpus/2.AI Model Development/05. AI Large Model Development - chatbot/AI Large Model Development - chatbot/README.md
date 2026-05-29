# AI Application Development - Chatbot

## 1. Course Content

Master the use of Dify to quickly develop a chatbot

## 2. Starting the Dify Service

Connect to the vehicle's computer via VNC or SSH, and enter the following command in the terminal:

bringup_dify

Check the vehicle's IP address (you can view it on the OLED screen, using ifconfig, or directly in the terminal). Enter the vehicle's IP address directly in the browser's address bar to access the Dify management page.

## 3. Chatbot

On the homepage, click "Create from Blank".

![Picture: page 1: picture 1](_page_1_Picture_1.jpeg)

Click to select "Chat Assistant" in the "Beginner-friendly" Chatbot -> App Name & Icon-> Create.

![Picture: page 1: picture 3](_page_1_Picture_3.jpeg)

Then, we enter our role prompt in the "INSTRUCTIONS"

![Figure: page 1: figure 5](_page_1_Figure_5.jpeg)

Example prompt:

### Role Definition

You are a friendly, patient, and talkative general-purpose chatbot named "Yahboom". Your core goal is to engage in natural and relaxed daily conversations with users, providing them with a pleasant conversational experience.

#### Conversation Rules

- 1. Tone: Maintain a friendly and natural tone, like talking to a friend, avoiding overly formal or mechanical expressions;
- 2. Response Length: For casual conversations, keep responses to 1-3 sentences. For complex questions from the user, you may elaborate, but avoid lengthy responses;
- 3. Boundaries: If the user asks about something you don't know, honestly state that you don't know and try to offer relevant suggestions, without fabricating information; if the user makes an inappropriate request, politely decline and guide the conversation back to a normal topic;
- 4. Logic: Follow the user's conversation context, stay on topic, and adjust your response style based on the user's tone (match humor with humor, maintain seriousness when the user is serious).

#### Start Conversation

Please respond to each of the user's messages according to the settings above.

Then select the AI model; here, qwen-max is used as an example, and the parameters remain at their default settings.

#### [!TIP]

- If you need to add visual question answering functionality, you need to select a multimodal model and enable the visual switch.
- If you need to save the application modifications, you need to click Publish.

![Figure: page 2: figure 14](_page_2_Figure_14.jpeg)

Enter the test content in the chat box on the right to view the model's response.

#### [!TIP]

If you are not satisfied with the model's response, you can adjust the prompt and model parameters to fine-tune the final result.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

## 4. Accessing the Chatbot via Web

- To access the AI application we created, there are two methods: web access and backend API access. Here, we will use web access as an example.
- Click the settings button for the chatbot on the left.

![Figure: page 3: figure 4](_page_3_Figure_4.jpeg)

Click to copy the public access URL of the Web App.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

Paste the link into your browser's address bar to access the chatbot's web interface.

### [!TIP]

As long as the device is on the same network segment as the vehicle's infotainment system, you can access the page. Therefore, Dify can also be deployed on a server.

![Picture: page 5: picture 0](_page_5_Picture_0.jpeg)
