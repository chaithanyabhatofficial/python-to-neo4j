from py2neo import Graph
import json
from app.config.config import *

# Connect to the Neo4j database
graph = Graph(NEO4J_URI, auth=(NEO4J_USER_NAME, NEO4J_PASSWORD))

def load_data_object(file_path : str):
    print("Function : Loading JSON file & returning nodes & links [load_data_object]")
    nodes = None
    links = None
    try:
        # Opening and Loading JSON file as dictionary
        file = open(file_path)
        json_data = json.load(file)

        if "nodes" in json_data.keys():
            nodes = json_data["nodes"]

        if "links" in json_data.keys():
            links = json_data["links"]
    except Exception as e:
        print("[load_data_object] Error while loading JSON and returning nodes and link : " + str(e))
    
    return nodes, links

def create_nodes(nodes):
    print("Function : Create query for nodes creation [create_nodes]")
    query = ''
    try:
        for node in nodes:
            # space not allowed in node name so replacing it with "" string
            node_name = str(node['id']).replace(" ", "")
            # creating label using group nad level key from JSON data provided
            node_label = "Group" + str(node['group']) + "_" + "Level" + str(node['level'])
            # creating obj text to add it to query
            node_obj_txt = "{"
            for key in node:
                node_obj_txt += str(key) + ":"
                if type(node[key]) == str:
                    node_obj_txt += "'" + node[key] + "'"
                else:
                    node_obj_txt += str(node[key])
                if list(node.keys())[-1] != key:
                    node_obj_txt += ", "
            node_obj_txt += "}"
            query += "CREATE (" + str(node_name) + ":" + str(node_label) + " " + node_obj_txt + ")"
    except Exception as e:
        print("[create_nodes] Error while creating node creation query string : " + str(e))
        query = None

    return query

def nodes_relation(links):
    print("Function : Create query for node relation [nodes_relation]")
    # one query for all the relation
    query = "CREATE\n"
    try:
        for link in links:
            # space not allowed in source and target so replacing it with "" string
            source = str(link["source"]).replace(" ", "")
            target = str(link["target"]).replace(" ", "")
            relationship_type = str(link["relationship_type"]).replace(" ", "_")

            query += "(" + source + ")-[:" + relationship_type
            # creating obj text to add it to query
            link_obj_txt = " {"
            for key in link:
                link_obj_txt += str(key) + ":"
                if type(link[key]) == str:
                    link_obj_txt += "'" + link[key] + "'"
                else:
                    link_obj_txt += str(link[key])
                if list(link.keys())[-1] != key:
                    link_obj_txt += ", "
            link_obj_txt += "}"

            query += str(link_obj_txt) + "]->(" + target + ")"
            if links[-1] != link:
                query += ",\n"
    except Exception as e:
        print("[nodes_relation] Error while creating query for node relation query string : " + str(e))
        query = None
    return query

def execute_neo4j_query(query):
    query_status = False
    print("Function : Run and commit Neo4j query [execute_neo4j_query]")
    try:
        result = graph.run(query)
        print(result)
        query_status = result != None
    except Exception as e:
        print("[execute_neo4j_query] Error while executing neo4j query : " + str(e))
    return query_status

def read_json_file_and_add_data_to_neo4j_db():
    """
    Function to load the JSON file data to Ne04j Database
    """
    print("Function : Load the JSON file data to Ne04j database [read_json_file_and_add_data_to_neo4j_db]")
    query = None
    # loading JSON file and obtaining nodes and links key from it
    nodes, links = load_data_object(FILE_PATH)
    if nodes and links:
        print("Obtained nodes and links from JSON file")
        # creating node creation query string using nodes 
        node_creation_query = create_nodes(nodes)
        if node_creation_query:
            print("Node creation query created")
            # creating nodes relation query using links
            nodes_relation_query = nodes_relation(links)
            if nodes_relation_query:
                print("Node relation query created")
                # adding both query to make single query
                query = node_creation_query + '\n' + nodes_relation_query
                # executing ne04j query
                print(query)
                query_status = execute_neo4j_query(query)
                print("Query ran successfully : " + str(query_status))