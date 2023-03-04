# ChatbotWithGraphDB

## Components:
### 1. A Telegram Based bot linker
### 2. A Knowledge Database using Neo4J*
### 3. Utilities to dump/query data into/from Neo4J

#### [*]In 2023, it seems that normal implementations of Chatbot are beaten by ChatGPT. However, I still think there's a way to use ChatGPT as a strong data parser and cooperate with a knowledge backend to achieve stronger human-program communication. That is why I use Neo4J. I will show a special case how we can interact with ChatGPT to do a series of tasks.

## Special Case
#### Many users have tried to ask ChatGPT some questions that needs general knowledge to reach enough precision. Unfortunately, ChatGPT is not good at answering these questions. One way to solve this problem is to use its powerful language ability to establish an information pipeline.
#### 1. Fetch the data from trusted sources.
#### 2. Transform one or two of them into structured data like json and provide the structured data and the original form to ChatGPT. ChatGPT will know how to transform the data.
#### 3. Let ChatGPT transform remaining data into json.
#### 4. Dump the data into Neo4J
#### 5. If we want to generate a robust phrase of something already in the database, we just use neo4j cipher to look for different relations and provide them to ChatGPT. ChatGPT will be able to assemble the separated information into a well organized phrase.

