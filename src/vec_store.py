from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
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
