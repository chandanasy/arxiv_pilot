from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chains import GraphCypherQAChain
from langchain_community.retrievers import ArxivRetriever
from langchain_community.vectorstores import Neo4jVector
from langchain_community.graphs import Neo4jGraph

import os


def get_vectorstore(data, from_source="documents"):
    ## load api key from os
    embedding = OpenAIEmbeddings(api_key=os.environ["OPENAI_API_KEY"])

    vectorStore = None
    if from_source == "documents":
        vectorStore = Chroma.from_documents(
            documents=data, embedding=embedding, persist_directory="./data"
        )
    elif from_source == "texts":
        vectorStore = Chroma.from_texts(
            texts=data, embedding=embedding, persist_directory="./data"
        )

    # db = FAISS.from_documents(data, embedding=embeddings)
    return vectorStore


def get_arxivretriever_res(query):
    retriever = ArxivRetriever(load_max_docs=3)
    docs = retriever.get_relevant_documents(query)
    return docs


def get_conversation_chain(llm, db):

    def get_chain(prompt):
        chain_type_kwargs = {"prompt": prompt}

        return RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(),
            chain_type_kwargs=chain_type_kwargs,
        )

    return get_chain


def get_neoj(llm, query):
    neo_user = os.environ["NEO_USER"]
    neo_pass = os.environ["NEO_PASS"]
    neo_url = os.environ["NEO_URL"]
    graph = Neo4jGraph(url=neo_url, username=neo_user, password=neo_pass)
    chain = GraphCypherQAChain.from_llm(
        llm, graph=graph, verbose=True, return_direct=True
    )
    res = chain.run(neo_url)
    return res
