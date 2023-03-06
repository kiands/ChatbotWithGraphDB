# ChatbotWithGraphDB

## Components:
### 1. A Telegram Based bot linker
### 2. A Knowledge Database using Neo4J*
### 3. Utilities to dump/query data into/from Neo4J
#### [*]In 2023, it seems that normal implementations of Chatbot are beaten by ChatGPT. However, I still think there's a way to use ChatGPT as a strong data parser and cooperate with a knowledge backend to achieve stronger human-program communication. That is why I use Neo4J. I will show an example case about how we can interact with ChatGPT to do a series of tasks.

## Directory Explanation
### /
The files (exclude folders) are mostly components of the Telegram ChatBot.
### /GraphTools
This folder stores python scripts to interact with Neo4J (generates Neo4J cipher according to the question received by ChatBot front end).
### /QADBFiller
This folder contains python scripts to dump data into Neo4J.

## Advantage of using Neo4J instead of MySQL to store knowledge
In my opinion, if we want to explain some knowledge, we cannot bypass one thing: organizing and introducing the relation. If we use the concept of object oriented design, the relations between different objects should be an object, too.

For example, If we want to use MySQL to describe the features of one object, the features are stored in a table and different features are stored in different columns. But what if we use Neo4J? Then we can see that the object we want to describe and its features can be stored like this:
#### object -relation-> feature1.
### And even like this:
#### &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-relation->
#### object&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;feature1
#### &ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;<-relation-
In many cases, a specific object has a feature and a feature also influences this object. There exists a two-way description and it has a more complex implementation in traditional RDBMS, however, this is very simple in graph concept.

#### Another important advantage of using Neo4J instead of traditional RDBMS is: if we use traditional RDBMS, we will need to modify the whole table if we want to add new feature column(s), but Neo4J can allow us to add feature(s) on one specific object to achieve higher efficiency and will not have huge table problem.

## Example Case
#### Many users have tried to ask ChatGPT some questions that needs general knowledge to reach enough precision. Unfortunately, ChatGPT is not good at answering these questions. One way to solve this problem is to use its powerful language ability to establish an information pipeline.
1. Fetch the data from trusted sources.
2. Transform one or two of them into structured data like json and provide the structured data and the original form to ChatGPT. ChatGPT will know how to transform the data.
3. Let ChatGPT transform remaining data into json.
4. Dump the data into Neo4J
5. If we want to generate a robust phrase of something already in the database, we just use neo4j cipher to look for different relations and provide them to ChatGPT. ChatGPT will be able to assemble the separated information into a well organized phrase.

### [1]Q: I will provide you a sentence and a json for reference and I want you to transform the information inside the data into json that in same format.
### [2]A(From ChatGPT): Sure, I'd be happy to help! Please provide the sentence and the JSON data you would like me to transform.
### [3]Q: sentence: There is a restaurant called 5Spice(Vietnamese) and it mainly provide Pho dishes. its reputation is good and many people rate it 5/5 stars. Some relative store names are Pho888, Pho66.
```
json
{"id":1,"name":"5Spice","desc":"A Vietnamese restaurant provides delicious Pho","reput":"very good","foods":["Pho"],"relatives":["Pho","Pho66"]}
attention: the "desc" key in json means description, the "reput" key in json means reputation, the value of "foods" key need to be written as string list in pytho format and the value of "relatives" key need to be written as string list in python format, too. you need to extract data from the sentence and fill them into the best fit place of json.
```
### [4]A(From ChatGPT): Here is the JSON data in the same format as the provided example:
```
json
{
  "id": 1,
  "name": "5Spice",
  "desc": "A Vietnamese restaurant provides delicious Pho dishes.",
  "reput": "good",
  "foods": ["Pho"],
  "relatives": ["Pho888", "Pho66"]
}
```
### [5]Q: then help me transform the next sentence into a json. That is: Nusr-Et is a steakhouse and it mainly provide beef steak with fancy services. Some people like its funny services and memes while some people think it is not worthy. There are many relative stores like Keens, Club A.
### [6]A(From ChatGPT): Sure, here's the JSON data for the given sentence:
```
json
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
```
### [7]Q: correction: can you give a conclusion of the reputation with a single sentence and revise the json?
### [8]A: Sure! Here's the revised JSON data with a single sentence summary for the reputation:
```
json
{
  "id": 1,
  "name": "Nusr-Et",
  "desc": "A steakhouse that provides beef steak with fancy services.",
  "reput": "Mixed reputation with some customers loving the funny services and memes, while others feel it is not worth the price.",
  "foods": ["Beef Steak"],
  "relatives": ["Keens", "Club A"]
}
```
#### The result json will be stored in /QADBFiller/data/entities.json and the keys and values will be processed and automatically filled into Neo4J ciphers to generate data records for future queries.
#### When we provide the following relations to ChatGPT:
Nusr-Et -description-> A steakhouse that provides beef steak with fancy services.

&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-reputation-> Mixed reputation with some customers loving the funny services and memes, while others feel it is not worth the price.

&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-foods> ["Beef Steak"],

&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;-relatives-> ["Keens", "Club A"]
#### ChatGPT will smoothly assemble the query results into a good answer. We can also use this to generate appropriate prompts which are important in interacting with ChatGPT to let it generate high quality outputs.
