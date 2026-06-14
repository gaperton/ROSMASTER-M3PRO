# AI Application Development - Chatbot
**AI Application Development - Chatbot**

1. Course Content

2. Starting the Dify Service

3. Chatbot

4. Accessing the Chatbot via Web

## 1. Course Content
Master the use of Dify to quickly develop a chatbot
## 2. Starting the Dify Service
Connect to the vehicle's computer via VNC or SSH, and enter the following command in the

terminal:


![](AI-Large-Model-Development---chatbot.pdf-0-1.jpeg)

Check the vehicle's IP address (you can view it on the OLED screen, using `ifconfig`, or

directly in the terminal). Enter the vehicle's IP address directly in the browser's address bar

to access the Dify management page.

## 3. Chatbot
![](AI-Large-Model-Development---chatbot.pdf-0-2.jpeg)
On the homepage, click "Create from Blank".


Click to select "Chat Assistant" in the "Beginner-friendly" Chatbot -> App Name & Icon->

Create.


Then, we enter our role prompt in the "INSTRUCTIONS"


![](AI-Large-Model-Development---chatbot.pdf-1-0.jpeg)

![](AI-Large-Model-Development---chatbot.pdf-1-1.jpeg)

![](AI-Large-Model-Development---chatbot.pdf-1-2.jpeg)
Example prompt:


![](AI-Large-Model-Development---chatbot.pdf-2-0.jpeg)


Then select the AI model; here, `qwen`  - `max` is used as an example, and the parameters remain

at their default settings.


[!TIP]


If you need to add visual question answering functionality, you need to select a

multimodal model and enable the visual switch.

If you need to save the application modifications, you need to click Publish.


Enter the test content in the chat box on the right to view the model's response.


[!TIP]


If you are not satisfied with the model's response, you can adjust the prompt and

model parameters to fine-tune the final result.


![](AI-Large-Model-Development---chatbot.pdf-2-1.jpeg)
![](AI-Large-Model-Development---chatbot.pdf-3-0.jpeg)
## 4. Accessing the Chatbot via Web
To access the AI application we created, there are two methods: web access and backend API

access. Here, we will use web access as an example.

Click the settings button for the chatbot on the left.


![](AI-Large-Model-Development---chatbot.pdf-3-1.jpeg)
![](AI-Large-Model-Development---chatbot.pdf-4-0.jpeg)

Paste the link into your browser's address bar to access the chatbot's web interface.


[!TIP]


As long as the device is on the same network segment as the vehicle's infotainment

system, you can access the page. Therefore, Dify can also be deployed on a server.


![](AI-Large-Model-Development---chatbot.pdf-5-0.jpeg)
