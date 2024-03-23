import asyncio
from pdf import get_pdf_images, get_pdf_pages
from vec_store import get_conversation_chain, get_vectorstore
from typing import List


def render_sidebar(
    st,
    queries: List,
    handle_userinput,
):
    st.subheader("Analyse your documents")
    ticker = st.text_input(
        key="ticker",
        label="Enter ticker for the stock your are analysing",
        placeholder="Enter ticker like AAPL",
    )

    pdf_docs = st.file_uploader(
        "Upload your PDFs here and click on 'Process'",
        accept_multiple_files=True,
        type=["pdf"],
    )

    on = st.toggle("Include Web results")
    if on:
        st.session_state["include_web_results"] = True
    else:
        st.session_state["include_web_results"] = False

    file_paths = []
    for i, pdf in enumerate(pdf_docs):
        path = f"./pdfs/{i}.pdf"
        file_paths.append(path)
        with open(path, "wb") as f:
            f.write(pdf.getvalue())

    if pdf_docs and ticker and len(ticker) > 0:
        if st.button("Process"):
            with st.spinner("Processing"):

                pages = get_pdf_pages(file_paths)
                images = get_pdf_images(file_paths)
                st.session_state["images"] = images
                # content = make_claude_messages(pdf_docs)
                # st.text(get_anthropic_answer(content))
                vectorstore_db = get_vectorstore(pages)
                st.session_state.chain = get_conversation_chain(
                    st.session_state["llm"], vectorstore_db
                )
                st.text("Done")

                # Define an async function to process a single query
                async def process_query(prompt, query):
                    result = await st.session_state.chain(prompt).acall(query)
                    return result["result"]

                # Use asyncio to run all queries in parallel
                async def process_all_queries():
                    tasks = [process_query(prompt, query) for prompt, query in queries]
                    results = await asyncio.gather(*tasks)
                    return results

                st.session_state["results"] = asyncio.run(process_all_queries())
                # st.session_state["results"] = ["1", "2", "3"]

            # if st.session_state["results"]:
            #     user_question = st.text_input(
            #         key="user_question",
            #         label="Ask a question about your documents:",
            #         on_change=handle_userinput,
            #     )
