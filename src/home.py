import streamlit as st
import textwrap
import anthropic
from dotenv import load_dotenv
from streamlit.components.v1 import html
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from containers import sidebar
from containers.htmlTemplates import css
from neo4j import GraphDatabase
import streamlit.components.v1 as components
from graphviz import Digraph
from langchain_community.retrievers import ArxivRetriever
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

import os


def get_anthropic_answer(content):
    client = anthropic.Anthropic()
    content.append(
        {
            "type": "text",
            "text": "Do financial analysis on this data",
        }
    )

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=300,
        temperature=0,
        system="You are an financial document read and data and provide analysis. \
        Focus on accuracy of the numbers. If possible write down bullet points",
        messages=[{"role": "user", "content": content}],
    )
    return message.content


def handle_userinput():
    user_text = st.session_state["textarea"]
    if st.session_state["textarea"]:
        if abs(len(st.session_state) - len(user_text)) > 10:
            retriever = ArxivRetriever(load_max_docs=3)
            docs = retriever.get_relevant_documents(query=user_text)
            # print(len(docs))
            # print([[doc.metadata['Entry ID'], doc.metadata['Title']] for doc in docs])
            print(len(docs))
            st.session_state["links"] = []
            st.session_state["links"].extend(
                [[doc.metadata["Entry ID"], doc.metadata["Title"]] for doc in docs]
            )

            uri = "neo4j+s://c6666d76.databases.neo4j.io:7687"  # Replace with your Neo4j database URI
            username = "neo4j"  # Replace with your Neo4j username
            password = os.environ["NEO_PASS"]  # Replace with your Neo4j password

            graph = Neo4jGraph(url=uri, username=username, password=password)

            chain = GraphCypherQAChain.from_llm(
                ChatOpenAI(temperature=0),
                graph=graph,
                verbose=True,
                top_k=3,
                return_intermediate_steps=False,
                return_direct=True,
            )
            query = "papers on " + user_text
            res = chain(query)
            print(len(res["result"]))
            if hasattr(res, "result") and hasattr(res["result"]["p"]):
                print(len(res["result"]))

                st.session_state["links"].extend(
                    [
                        [
                            "https://arxiv.org/abs" + str(r["p"]["arxiv_id"]),
                            r["p"]["abstract"][:50],
                        ]
                        for r in res["result"]
                    ]
                )
            elif hasattr(res, "result") and hasattr(res["result"]["p1"]):
                print(len(res["result"]))

                st.session_state["links"].extend(
                    [
                        [
                            "https://arxiv.org/abs" + str(r["p1"]["arxiv_id"]),
                            r["p1"]["abstract"][:50],
                        ]
                        for r in res["result"]
                    ]
                )

                if hasattr(res["result"]["p2"]):
                    st.session_state["links"].extend(
                        [
                            [
                                "https://arxiv.org/abs" + str(r["p2"]["arxiv_id"]),
                                r["p2"]["abstract"][:50],
                            ]
                            for r in res["result"]
                        ]
                    )

            st.write("calling!!!")
            print("calling!!!")


def get_response(response: str) -> str:
    return "\n".join(textwrap.wrap(response, width=100))


# def display_images():
#     detectTable = st.session_state.detect_table
#     if hasattr(st.session_state, "images"):
#         for image in st.session_state["images"]:
#             if detectTable.detect(image):
#                 with open(image, "rb") as fp:
#                     st.image(fp.read(), output_format="JPEG")


def get_llm(value: str):
    llm = None
    if value == "default":
        llm = ChatOpenAI(temperature=0)
    elif value.startswith("claude"):
        llm = ChatAnthropic(model_name=value, temperature=0)
    elif value == "gpt-4-turbo-preview":
        llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0)
    return llm


def handle_select_llm():
    value = st.session_state["llm_model_name"]
    st.session_state["llm"] = get_llm(value)


def render_page():
    load_dotenv()
    # uri = "neo4j+s://c6666d76.databases.neo4j.io:7687"  # Replace with your Neo4j database URI
    # username = "neo4j"  # Replace with your Neo4j username
    # driver = GraphDatabase.driver(uri, auth=(username, os.environ["NEO_PASS"]))
    # results = None
    # st.session_state.detect_table = DetectTable.instance()

    # st.set_page_config(
    #     page_title="Chat with multiple PDFs", page_icon=":books:", layout="wide"
    # )
    st.write(css, unsafe_allow_html=True)
    st.markdown(
        """
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
""",
        unsafe_allow_html=True,
    )

    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "usertext" not in st.session_state:
        st.session_state.usertext = ""
    col = st.columns((1, 1, 1), gap="medium")
    with col[0]:
        selected_llm_value = st.selectbox(
            key="llm_model_name",
            label="Select llm",
            options=[
                "default",
                "claude-3-sonnet-20240229",
                "claude-3-opus-20240229",
                "claude-3-haiku-20240307",
                "gpt-4-turbo-preview",
            ],
            index=0,
            on_change=handle_select_llm,
        )

    with col[1]:
        toggle1 = st.toggle(
            "Include indirect results",
        )
        toggle2 = st.toggle("Include similar work")

    with col[2]:
        select_joural = st.selectbox(
            key="repo_name",
            label="Select Repository",
            options=[
                "arXiv",
                "ACM",
                "ieee",
            ],
            index=0,
        )

    st.session_state["llm"] = get_llm(selected_llm_value)
    st.header("Paperlink")

    with st.sidebar:

        sidebar.render_sidebar(
            st=st,
            handle_userinput=handle_userinput,
        )

    textarea = st.text_area(
        key="textarea", label="Edit text here", height=700, on_change=handle_userinput
    )
