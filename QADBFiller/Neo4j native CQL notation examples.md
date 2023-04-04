# Neo4j CQL

Basic

```bash
# Node
(:TypeOfNode{PropertyKey:"PropertyValue"})
# Relation
[:TypeOfRelation{PropertyKey:"PropertyValue"}]
# Directed relation
()-[]->()
# Undirected relation
()-[]-()
```

## Query: Create

Create a new node

```bash
# Create a single node
CREATE (:Food{Name:"Fantasy Food"})
```

Create a relation between two nodes

```bash
MATCH (n1:Shop), (n2:Food)
WHERE n1.name = "Shop1" AND n2.name = "Food1"
CREATE (n1)-[:has]->(n2)
```

## Query: Match(Search)

Match a chain

```bash
MATCH (m:Shop)-[r:has]->(n:Food) where m.name = '富樂士林'
return m.name, r.name, n.name
# ()-[]->()
# node relation node
# m,r,n are alias, the right side of the `:` is the node's and relation's type
# alias.name can access property of entities
```

```bash
(:Person{Name:"A"})-[:Call]->(:Person{Name:"B"})
# For the (), the word between `:` and `{}` is the node's type
# Inside the {} is place for entering the node's properties
# On this relation notation's left, we can explain: the node's type is Person
# and the node's name is "A"
# In the center `[]` is the relation of Person A and Person B. The relation's
# type is Call. This type has no property but can also set properties
```

Match relation

```bash
# Match all `has` type relations and return their name
MATCH ()-[r:has]-()
return r.name

# Match all `has` type relations and return their name
MATCH (n:Shop)-[r:has]-() where n.name="富樂士林"
return n.name,r.name
```

Query-Combined match

```bash
# Search for Food type nodes and Shop type nodes simultaneously
# If Food type nodes and Shop type nodes have relations between them
# The relations will be displayed at the same time
MATCH (n:Food)
MATCH (m:Shop)
RETURN n,m
```

Query-Node(s) with multiple same type relations

```bash
# Search for Shop type nodes with has type relations that point to Food type nodes
# with the restriction that the counted relations must be more than 2
MATCH (n:Shop)-[r:has]-(m:Food)
WITH n, count(r) AS num_has
WHERE num_has >= 2
RETURN n
```

### If you want to query node with specific type of relation

This is used to support simple graph theory indicators - the input file’s structure of packages like NetworkX always have 2 columns like `v1 v2` or 3 columns like `v1 v2 v3`. Once we sorted out the table in Neo4j, it will be easy to write a script to transform the data and compute.

```bash
# The visualized graph will show all relations but the table view will
# be concise
MATCH (n:Shop)-[r:has]->(m:Food)
# The following EXISTS is an optional restriction
WHERE EXISTS(r.name)
return n.name,r.name,m.name
```

## Query: Update

Add property into existed node or update via overwrite

```bash
# If we have known the node's existed property, we can locate it via this property
MATCH (n:Person {name: "John"})
SET n.age = 30
# If the SET notation is `SET n.name = "Bob"`, the node's name will be changed
```

Change a property’s name

```bash
MATCH (n)
# Use `WHERE` and `AND` can locate precisely
WHERE EXISTS(n.old_property) and n.name="Food1"
SET n.new_property = n.old_property
REMOVE n.old_property
```

## Query: Delete

Query-Delete a node

```bash
MATCH (n:Food) where n.Name="Fantasy Food"
DELETE n
```

Query-Delete a relation

```bash
# Use undirected relation notation here can help with probability of matching
MATCH (n:Shop)-[r:has]-(m:Food)
WHERE n.name="Shop1" AND m.name="Food1"
DELETE r
```