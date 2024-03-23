import streamlit as st
import textwrap
import anthropic
from dotenv import load_dotenv
from streamlit.components.v1 import html
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

from containers import sidebar

# from cnt import render_sidebar
from containers.htmlTemplates import css, bot_template, trading_view_template
from news import get_latest_news

# from process_images import DetectTable

from prompts import (
    balanceSheetBulletPoints,
    riskTemplate,
    summarizeChain,
    investmentThesisTemplate,
)


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
    user_question = st.session_state["user_question"]
    if st.session_state.chain:
        print("Running summarize chain on user input", user_question)
        prompt = summarizeChain()
        response = st.session_state.chain(prompt).run(user_question)
        st.markdown(
            bot_template.replace("{{MSG}}", get_response(response)),
            unsafe_allow_html=True,
        )


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


def render_page(auth):
    load_dotenv()
    queries = [investmentThesisTemplate(), riskTemplate(), balanceSheetBulletPoints()]
    results = None
    # st.session_state.detect_table = DetectTable.instance()

    # st.set_page_config(
    #     page_title="Chat with multiple PDFs", page_icon=":books:", layout="wide"
    # )
    st.write(css, unsafe_allow_html=True)

    if "chain" not in st.session_state:
        st.session_state.chain = None

    st.header("Chat with multiple PDFs :books:")
    # if st.session_state["authentication_status"]:
    with st.sidebar:
        auth.logout()
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

        st.session_state["llm"] = get_llm(selected_llm_value)

        sidebar.render_sidebar(
            st=st,
            handle_userinput=handle_userinput,
            queries=queries,
        )
    if hasattr(st.session_state, "ticker") and hasattr(st.session_state, "results"):
        ticker = st.session_state["ticker"]
        results = st.session_state["results"]

        if st.session_state["include_web_results"] and hasattr(st.session_state, "llm"):
            # fig = st.session_state.ticker_data["fig"]
            # st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            trading_view_src = trading_view_template.replace("{{ticker}}", ticker)
            st.subheader("Stock trend")
            html(
                """
                    <div style="height: 500px">"""
                + trading_view_src
                + """
                    </div>
                """,
                height=500,
            )
            if hasattr(st.session_state, "news_summary") == False:
                with st.spinner("Fetching News Summary"):
                    st.session_state["news_summary"] = get_latest_news(
                        st.session_state["llm"], ticker
                    )
            st.subheader("News summary")
            st.markdown(st.session_state["news_summary"])

        if len(results) == 3:
            st.subheader(f"Financial summary for {ticker}")
            col = st.columns((3, 3, 3), gap="medium")
            with col[0]:
                st.markdown("#### Investment Thesis")
                if results[0]:
                    st.markdown(results[0])
            with col[1]:
                st.markdown("#### Risk analysis")
                if results[1]:
                    st.markdown(results[1])
            with col[2]:
                st.markdown("#### Balance Sheet analysis")

                if results[2]:
                    st.markdown(results[2])

            # display_images()
