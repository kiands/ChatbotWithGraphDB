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

### Q: I will provide you a sentence and a json for reference and I want you to transform the information inside the data into json that in same format.
### A(From ChatGPT): Sure, I'd be happy to help! Please provide the sentence and the JSON data you would like me to transform.
### Q: sentence: There is a restaurant called 5Spice(Vietnamese) and it mainly provide Pho dishes. its reputation is good and many people rate it 5/5 stars. Some relative store names are Pho888, Pho66.
json:{"id":1,"name":"5Spice","desc":"A Vietnamese restaurant provides delicious Pho","reput":"very good","foods":["Pho"],"relatives":["Pho","Pho66"]}
attention: the "desc" key in json means description, the "reput" key in json means reputation, the value of "foods" key need to be written as string list in pytho format and the value of "relatives" key need to be written as string list in pytho format, too. you need to extract data from the sentence and fill them into the best fit place of json.
### A(From ChatGPT): Here is the JSON data in the same format as the provided example:

json
{
  "id": 1,
  "name": "5Spice",
  "desc": "A Vietnamese restaurant provides delicious Pho dishes.",
  "reput": "good",
  "foods": ["Pho"],
  "relatives": ["Pho888", "Pho66"]
}
### Q: then help me transform the next sentence into a json. That is: Nusr-Et is a steakhouse and it mainly provide beef steak with fancy services. Some people like its funny services and memes while some people think it is not worthy. There are many relative stores like Keens, Club A.
### A(From ChatGPT): Sure, here's the JSON data for the given sentence:
{
  "id": 1,
  "name": "Nusr-Et",
  "desc": "A steakhouse that provides beef steak with fancy services.",
  "reput": {
    "good": 60,
    "average": 20,
    "bad": 20
  },
  "foods": ["Beef Steak"],
  "relatives": ["Keens", "Club A"]
}
### Q: correction: can you give a conclusion of the reputation with a single sentence and revise the json?
### A: Sure! Here's the revised JSON data with a single sentence summary for the reputation:
{
  "id": 1,
  "name": "Nusr-Et",
  "desc": "A steakhouse that provides beef steak with fancy services.",
  "reput": "Mixed reputation with some customers loving the funny services and memes, while others feel it is not worth the price.",
  "foods": ["Beef Steak"],
  "relatives": ["Keens", "Club A"]
}
