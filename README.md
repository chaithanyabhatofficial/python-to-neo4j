# python-to-neo4j
A simple Python code to push a JSON structure onto NEo4j

- Load the JSON File using json module.
- Creat two list out of the JSON file data called nodes and links.
- Create query to create nodes using nodes list of dict.
- Create query to map the relation between nodes using links list of dict.
- Merge two query into one query
- Run the query using py2neo module