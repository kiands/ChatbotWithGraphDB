# Thinking about the methods to dump data

## 1. The method in this prototype

Simply speaking, the method in this prototype in build_graph.py is just a fixed solution. It has designated node types and relation types, the poperties are also fixed. Though it uses the key-value feature of json type data source, it is apparently not flexible.

## 2. Think about the usage of py2neo

### 2.1 Create nodes

```python
from py2neo import Node, Relationship
a = Node("Person", name="Alice")
b = Node("Person", name="Bob")
ab = Relationship(a, "KNOWS", b)
>>> ab
>>> (alice)-[:KNOWS]->(bob)
```

We just created 2 nodes with type = `Person` and property `name`. We also created a relation between node a and node b and assigned it to variable ab. The type of the relation is `KNOWS`. We can also read data from other resources and simply create objects included in py2neo using same methods.

### 2.1 Assign or update property to nodes and relations

```python
# assign
a['age'] = 20
b['age'] = 21
r['time'] = '2017/08/31'
print(a, b, r)
>>> (alice:Person {age:20,name:"Alice"}) (bob:Person {age:21,name:"Bob"}) (alice)-[:KNOWS {time:"2017/08/31"}]->(bob)
```

```python
# update
data = {
    'name': 'Amy',
    'age': 21
}
a.update(data)
print(a)
```

### 2.3 Functions implemented in py2neo

(OOP) properties of class Node:

- hash(node): returns node’s ID’s hash value, ID is unique
- node[key]: returns node’s property, if no such property, it will return None
- node[key] = value: sets the node’s property
- del node[key]: deletes the designated property, if this property does not exist, it will return KeyError
- len(node): returns the quantity of a node’s properties
- dict(node): returns all properties of a node
- walk(node): returns a generator(?) and only contains one node
- labels(): returns a set of a node’s labels
- has_label(label): whether a node has the designated label
- add_label(label): adds a label to a node
- remove_label(label): removes a node’s label
- clear_labels(): clears all labels of a node
- update_labels(labels): adds multiple labels, remember labels can be iterative

(OOP) properties of class Relation:

- hash(relationship): returns the relation’s ID’s hash value, ID is unique
- relationship[key]: returns the relation’s property, if no such property, it will return None
- relationship[key]: = value: sets the relation’s property
- del relationship[key]: deletes the designated property of the relation
- len(relationship): returns the relation’s quantity of properties
- dict(relationship): returns all properties of the relation using dict
- walk(relationship): returns a generator(?) that includes the starting node, the relation itself and the ending node
- type(): returns the type of the relation

Once we have understood the ways to CRUD, it is easy for us to use loops to dump data into the database.

### 2.4 Manipulating the database

```python
# connect
test_graph = Graph(
    "http://localhost:7474", 
    username="neo4j", 
    password="xxxx"
)
```

```python
# use subgraph to add data
from py2neo import Node, Relationship, Graph

a = Node('Person', name='Alice')
b = Node('Person', name='Bob')
r = Relationship(a, 'KNOWS', b)
s = a | b | r
graph = Graph(password='123456')
graph.create(s)
```

```python
# separately add objects
from py2neo import Graph, Node, Relationship

graph = Graph(password='123456')
a = Node('Person', name='Alice')
graph.create(a)
b = Node('Person', name='Bob')
ab = Relationship(a, 'KNOWS', b)
graph.create(ab)
```

## 3. Future work

I will try to rewrite the code or partly rewrite the code and introduce a simplified structure of entities.json. Due to the feature of Neo4j, it is not a big problem to execute duplicate CQL. This allows me to use simple notations in multiple lines, this also allows us to use non-fixed definitions of nodes and relations which makes it possible to let the program become extensive.
