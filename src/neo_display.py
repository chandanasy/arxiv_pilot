import streamlit as st
from graphviz import Digraph
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

uri = (
    "neo4j+s://c6666d76.databases.neo4j.io:7687"  # Replace with your Neo4j database URI
)
username = "neo4j"  # Replace with your Neo4j username
driver = GraphDatabase.driver(uri, auth=(username, os.environ["NEO_PASS"]))


# Streamlit app
def main():
    st.title("Graph Visualization")

    # Create a new directed graph
    graph = Digraph(format="png")

    # Execute the Cypher query and process the results
    with driver.session() as session:
        result = session.run(
            "MATCH p=()-[:CITES]->() MATCH a=()-[:AUTHORED]->() RETURN p,a limit 200"
        )
        for record in result:
            cites_path = record["p"]
            authored_path = record["a"]

            # Add nodes and edges for the CITES path
            for node in cites_path.nodes:
                graph.node(str(node.id), label=node.get("title", ""))
            for rel in cites_path.relationships:
                graph.edge(str(rel.start_node.id), str(rel.end_node.id), label="CITES")

            # Add nodes and edges for the AUTHORED path
            for node in authored_path.nodes:
                graph.node(str(node.id), label=node.get("name", ""))
            for rel in authored_path.relationships:
                graph.edge(
                    str(rel.start_node.id), str(rel.end_node.id), label="AUTHORED"
                )

    # Render the graph as an image file
    graph.render("output_graph", format="png")

    # Display the graph image in Streamlit
    st.image("output_graph.png")


if __name__ == "__main__":
    main()
