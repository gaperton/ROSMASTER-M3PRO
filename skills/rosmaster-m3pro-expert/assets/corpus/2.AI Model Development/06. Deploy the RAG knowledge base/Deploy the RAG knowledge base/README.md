# Deploying a Local RAG Knowledge Base

## 1. Course Content

- Master the process and methods for local deployment, debugging, and testing of the RAG knowledge base.
- Master the method for extending the RAG knowledge base based on your specific task scenarios.

### [TIP]

- The RAG knowledge base helps general AI large models provide reference knowledge in vertical domains, preventing AI large models from generating hallucinatory responses and increasing the model's ability to respond with knowledge in vertical domains.
- The RAG knowledge base can help robots quickly expand their generalization capabilities in different task scenarios.

## 2. Starting the Dify Service

Connect to the vehicle's computer via VNC or SSH, and enter the following command in the terminal:

bringup_dify

Check the vehicle's IP address (you can check it on the OLED screen, using ifconfig, or directly in the terminal). Enter the vehicle's IP address directly in the browser's address bar to access the Dify management page.

## 3. Viewing the Preset Knowledge Base

Click on the Knowledge Base page on the homepage. Dify comes pre-configured with two RAG knowledge bases, with the same content but different languages.

### [TIP]

The preset knowledge base provides training examples for some task scenarios to help the AI model quickly master relevant skills.

![Picture: page 1: picture 6](_page_1_Picture_6.jpeg)

- Open a knowledge base; it contains a preset file called Sample training for the decisionmaking level, which includes:
- Sample training for the decision-making level: Stores preset reference examples related to specific task scenarios.

![Figure: page 1: figure 9](_page_1_Figure_9.jpeg)

## 4. Expanding the RAG Knowledge Base

To expand with a new knowledge base, click "Create Knowledge".

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

- Here, we'll use importing local data as an example.
- Click "Import Existing file" -> Select File -> Next

![Picture: page 2: picture 3](_page_2_Picture_3.jpeg)

Then, you'll enter the knowledge base configuration page. Click the preview block to view the file chunking effect. Here, select "Economic" for the indexing mode.

### [!TIP]

- For beginners, it is recommended to use the economic mode for learning and testing. The difference between the two indexing modes:
  - Economic: Retrieves content from the knowledge base using **keywords**. It cannot perform extended retrieval of similar semantics, and the method of retrieving knowledge fragments is relatively rigid.
  - High-Quality Mode: Requires an embedding model to consume extra tokens and requires a rerank model, enabling more accurate retrieval of similar semantic fragments.
- The default knowledge base mode is High-Quality Mode.

### 4.1 Economic Mode Knowledge Base

After selecting the following configuration, click "Save and Process".

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

Then wait for the embedding to complete, and click to go to document.

![Figure: page 3: figure 2](_page_3_Figure_2.jpeg)

When the knowledge base is functioning normally, the status will show as available. Then click on the knowledge base file.

![Figure: page 3: figure 4](_page_3_Figure_4.jpeg)

Afterwards, you can see the segmented knowledge base fragments. The small text below each segment shows the automatically generated keywords for that segment (only available in economic mode).

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

If the keywords do not accurately describe the knowledge fragment, click "Edit" on the right side of the fragment to edit the content or keywords of that fragment. The image below shows the modified keywords, then click save.

![Figure: page 4: figure 2](_page_4_Figure_2.jpeg)

### 4.2 High-Quality Mode Knowledge Base

- If you need to use a high-quality knowledge base later, refer to this section of the tutorial.
- The knowledge base creation and file import process is the same as before.
- Here, select "High-Quality" for the indexing method, and choose any retrieval method. Here, we use hybrid retrieval as an example. Finally, save and process.

![Figure: page 5: figure 0](_page_5_Figure_0.jpeg)

### 4.3 Recall Test

- Retrieval testing tests the actual effectiveness of retrieving relevant knowledge snippets from the knowledge base based on the input, helping to optimize the AI model's response performance.
- After opening a knowledge base, click on "Retrieval Testing" on the left side.

![Figure: page 5: figure 4](_page_5_Figure_4.jpeg)

- Enter the test content in the source text (simulating user input during actual use), and then click "Test".
- The retrieved paragraphs and the knowledge base related to the input content will appear on the right. The knowledge base tested here is the economic model knowledge base, which retrieves information based on keywords.

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

If it's a high-quality mode knowledge base, the retrieved snippets will have a SCORE rating. A higher score indicates a higher relevance between the snippet and the input content. Highquality mode knowledge bases can perform associative retrieval of similar semantics, but also consume tokens.

![Figure: page 6: figure 2](_page_6_Figure_2.jpeg)
