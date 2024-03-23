import os
from langchain_openai import ChatOpenAI
import requests
from langchain.agents import AgentType, initialize_agent
from dotenv import load_dotenv

# from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

from typing import Iterable, List, Optional

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.documents import Document
from langchain_core.tools import BaseTool
from requests.exceptions import HTTPError, ReadTimeout
from urllib3.exceptions import ConnectionError

from langchain_community.document_loaders.web_base import WebBaseLoader

from langchain_core.pydantic_v1 import BaseModel, Field


class cited_answer(BaseModel):
    """Answer the user question based only on the given sources, and cite the sources used."""

    answer: str = Field(
        ...,
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: List[int] = Field(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the answer.",
    )


class YahooFinanceNewsTool(BaseTool):
    """Tool that searches financial news on Yahoo Finance."""

    name: str = "yahoo_finance_news"
    description: str = (
        "Useful for when you need to find financial news "
        "about a public company. "
        "Input should be a company ticker. "
        "For example, AAPL for Apple, MSFT for Microsoft."
    )
    top_k: int = 5
    """The number of results to return."""

    def _run(
        self,
        query: str,
        # model_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        """Use the Yahoo Finance News tool."""
        try:
            import yfinance
        except ImportError:
            raise ImportError(
                "Could not import yfinance python package. "
                "Please install it with `pip install yfinance`."
            )
        company = yfinance.Ticker(query)
        try:
            if company.isin is None:
                return f"Company ticker {query} not found."
        except (HTTPError, ReadTimeout, ConnectionError):
            return f"Company ticker {query} not found."

        links = []
        try:
            links = [n["link"] for n in company.news if n["type"] == "STORY"]
        except (HTTPError, ReadTimeout, ConnectionError):
            if not links:
                return f"No news found for company that searched with {query} ticker."
        if not links:
            return f"No news found for company that searched with {query} ticker."
        loader = WebBaseLoader(web_paths=links)
        docs = loader.load()
        # include_content = (
        #     True
        #     if model_name.startswith("claude-3-opus") or model_name.startswith("gpt-4")
        #     else False
        # )
        result = self._format_results(docs, query, links)
        if not result:
            return f"No news found for company that searched with {query} ticker."
        return result

    @staticmethod
    def _format_results(
        docs: Iterable[Document], query: str, links=[], include_content=False
    ) -> str:
        doc_strings = [
            "\n".join(
                [doc.metadata["title"], doc.metadata["description"]],
            )
            for doc in docs
            if query in doc.metadata["description"] or query in doc.metadata["title"]
        ]
        if len(links) > 0 and len(doc_strings) > 0:
            doc_strings.append(
                ",".join(f"[{i+1}]({link_str})" for i, link_str in enumerate(links))
            )

        return "\n\n".join(doc_strings)


class SerpNewsTool(BaseTool):

    name: str = "serp_news"
    description: str = "SERP"
    top_k: int = 5
    """The number of results to return."""

    def _run(
        self,
        query: str,
        # model_name: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ):
        links = []
        result = None
        try:
            api_key = os.environ["SERP_API_KEY"]
            url = f"https://serpapi.com/search.json?engine=google&q={query}&google_domain=google.com&tbm=nws&api_key={api_key}"
            resp = requests.get(url).json()
            links = [n["link"] for n in resp["news_results"]]
            print(links)
            if not links:
                return f"No news found for company that searched with {query} ticker."
            loader = WebBaseLoader(
                web_paths=links,
                requests_per_second=5,
                continue_on_failure=True,
                # requests_kwargs={"timeout": 10.0},
            )
            docs = loader.load()
            result = self._format_results(docs, query, links)

        except (HTTPError, ReadTimeout, ConnectionError):
            return f"Company ticker {query} not found."

        # include_content = (
        #     True
        #     if model_name.startswith("claude-3-opus") or model_name.startswith("gpt-4")
        #     else False
        # )
        if not result:
            return f"No news found for company that searched with {query} ticker."
        print(result)
        return result

    @staticmethod
    def _format_results(
        docs: Iterable[Document], query: str, links=[], include_content=False
    ) -> str:
        for doc in docs:
            print(doc.metadata)
        doc_strings = [
            "\n".join(
                (
                    [doc.metadata["title"], doc.metadata["description"]]
                    if hasattr(doc, "description") == True
                    else [doc.metadata["title"]]
                ),
            )
            for doc in docs
        ]
        # doc_strings = [
        #     "\n".join(
        #         ([doc.metadata["title"], doc.metadata["description"]]),
        #     )
        #     for doc in docs
        # ]
        # if len(links) > 0 and len(doc_strings) > 0:
        #     doc_strings.append(
        #         ",".join(f"[{i+1}]({link_str})" for i, link_str in enumerate(links))
        #     )

        return "\n\n".join(doc_strings)


def get_latest_news(llm, ticker, tool="Google"):
    llm.max_tokens = 2000

    tools = []

    if tool == "Google":
        tools = [
            SerpNewsTool(),
        ]
    elif tool == "Yahoo":
        tools = [
            YahooFinanceNewsTool(),
        ]

    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    # model_name = ""
    # if "model_name" in llm:
    #     model_name = llm.model_name
    # elif "model" in llm:
    #     model_name = llm.model

    result = agent_chain.run(f"Get the financial news related to ticker: {ticker}")

    return result


if __name__ == "__main__":
    load_dotenv()
    llm = ChatOpenAI(temperature=0, api_key=os.environ["OPENAI_API_KEY"])
    get_latest_news(ticker="NVDA", llm=llm)
