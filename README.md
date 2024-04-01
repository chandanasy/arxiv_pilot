# PaperLink

The inspiration for PaperLink came from recognizing the desire for a unified platform that caters to the needs of students, researchers, and organizations in the field of academic research. We saw the pain points faced by individuals and groups in navigating the web for scholarly works & we wanted to create a solution that simplifies this process.

PaperLink revolutionizes academic research with a user-friendly platform combining GCP's scalability, Neo4j's knowledge graphs for managing citations, and Python for robust backend operations. It simplifies the research process with efficient AI-powered search capabilities using Anthropic's Claude and RAG retrieval, providing a seamless experience for researchers tired of wading through endless links and citations.

Link to Devpost Submission - https://devpost.com/software/paperlink-ft87lw

## Features

- **Text-based search**: Enter a text query or description of your research topic to find relevant papers.
- **ArXiv data fetching**: The application connects to the ArXiv API to retrieve the latest paper metadata.
- **Relevance ranking**: Papers are ranked based on their relevance to the input text using natural language processing techniques.
- **Interactive results**: Browse through the search results, view paper details, and access links to the full papers on the ArXiv website.
- **Citation management**: Easily copy citation information for the selected papers to include in your research work.

## Installation

To run PaperLink locally, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/shashvatshah9/arxiv_pilot
   ```

2. Navigate to the project directory:

   ```
   cd arxiv_pilot
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit application:

   ```
   streamlit run src/app.py
   ```

5. Open your web browser and visit `http://localhost:8501` to access the ArXiv Paper Finder application.

## Usage

1. Enter a text query or description of your research topic in the provided text input field.
2. Click the "Search" button to initiate the search process.
3. The application will fetch relevant papers from the ArXiv API based on your input text.
4. Browse through the search results displayed on the page.
5. Click on a paper title to view more details, including the abstract and a link to the full paper on the ArXiv website.
6. Use the "Copy Citation" button to easily copy the citation information for the selected paper.
7. Refine your search by modifying the input text and clicking the "Search" button again.

## Configuration

The ArXiv Paper Finder application can be configured by adding .env file

- `OPENAI_API_KEY`: Openai api key
- `NEO_PASS`: Neo4j password


## Contributing


## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

The PaperLink application relies on the ArXiv API to fetch paper metadata. We would like to acknowledge the ArXiv team for providing access to their valuable dataset.
