import asyncio
from pdf import get_pdf_images, get_pdf_pages
from vec_store import get_conversation_chain, get_vectorstore
from typing import List
from containers.htmlTemplates import item_template


def render_sidebar(
    st,
    handle_userinput,
):
    st.subheader("Recommended")
    import streamlit as st

    # Assume you have a list of items, where each item is a dictionary

    if hasattr(st.session_state, "links"):
        # Render the template for each item in the list
        for item in st.session_state["links"]:

            item_html = item_template.replace("{{URL}}", item[0]).replace(
                "{{LINE1}}", item[1]
            )
            st.markdown(item_html, unsafe_allow_html=True)
    # if textarea:
    #     if st.button("Process"):
    #         with st.spinner("Processing"):

    # content = make_claude_messages(pdf_docs)
    # st.text(get_anthropic_answer(content))
    # vectorstore_db = get_vectorstore(pages)
    # st.session_state.chain = get_conversation_chain(
    #     st.session_state["llm"], vectorstore_db
    # )
    # st.text("Done")

    # # Define an async function to process a single query
    # async def process_query(prompt, query):
    #     result = await st.session_state.chain(prompt).acall(query)
    #     return result["result"]

    # # Use asyncio to run all queries in parallel
    # async def process_all_queries():
    #     tasks = [process_query(prompt, query) for prompt, query in queries]
    #     results = await asyncio.gather(*tasks)
    #     return results

    # st.session_state["results"] = asyncio.run(process_all_queries())
    # st.session_state["results"] = ["1", "2", "3"]

    # if st.session_state["results"]:
    #     user_question = st.text_input(
    #         key="user_question",
    #         label="Ask a question about your documents:",
    #         on_change=handle_userinput,
    #     )
