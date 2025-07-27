# Bank of Maharashtra Loan Product Assistant

A Retrieval-Augmented Generation (RAG) assistant that answers questions about Bank of Maharashtra loan products. Built using FastAPI, LangChain, OpenAI, FAISS, and a modular Python codebase.

---

## Table of Contents

- [Project Setup](#project-setup)
- [How to Run the Pipeline](#how-to-run-the-pipeline)
- [Test the API](#test-the-api)
- [Architectural Decisions](#architectural-decisions)
- [Data Strategy](#data-strategy)
- [Model Selection](#model-selection)
- [AI Tools Used](#ai-tools-used)
- [Challenges Faced](#challenges-faced)
- [Potential Improvements](#potential-improvements)
- [Demo](#demo)
- [Contact](#contact)

---

## Project Setup

**Clear instructions to set up and run the project:**

### Prerequisites

- Python 3.13+
- [OpenAI API key](https://platform.openai.com/account/api-keys)

### 1. Create and activate a virtual environment

On Linux/Mac:
python -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
venv\Scripts\activate


### 2. Install dependencies
pip install -r requirements.txt


### 3. Set your OpenAI API Key
Create a .env file in the project root:  
OPENAI_API_KEY=sk-<your-key>


## How to Run the Pipeline
Step 1: Scrape Data  
python app/webscraper.py

Step 2: Clean & Chunk Data  
python app/data_cleaner.py

Step 3: Build FAISS Vector Store  
python app/vector_store.py

Step 4: Start FastAPI Server  
uvicorn app/main:app --reload


## Test the API
You can use Postman, curl, swagger or any HTTP client to send a POST request:  
curl -X POST "[http://127.0.0.1:8000/ask](http://127.0.0.1:8000/ask)" \  
-H "Content-Type: application/json" \  
-d "{\"question\": \"What are the interest rates for a home loan?\"}"  


## Architectural Decisions
Explain the reasoning behind your choices for each step:

- Libraries
httpx: Chosen for fast, reliable HTTP requests to fetch webpages for scraping.

- BeautifulSoup: Selected for its powerful HTML parsing and cleaning capabilities, making it easy to extract only the required loan information.

- langchain: Used for text chunking, embedding, prompt handling, and orchestrating the RAG pipeline. It simplifies building modular, scalable systems.

- faiss-cpu: Provides efficient, in-memory vector search. It supports fast retrieval of relevant text chunks and is suitable for lightweight local deployments.

- langchain_openai: Used to access OpenAI’s latest APIs for both embedding generation and LLM querying, and is fully compatible with LangChain.

- FastAPI: Offers a modern, easy-to-use REST API with strong Python support and fast development speed.

## Data Strategy  
How did you approach chunking your text data for the vector search? Why that strategy?

- Focus: Scrape only official Bank of Maharashtra loan product pages. Irrelevant pages are ignored.

- Chunking: Used RecursiveCharacterTextSplitter (from LangChain) with chunk size 500 and overlap 50 to balance token/context window size and model retrieval accuracy. This strategy helps retain important context in each chunk, improving answer quality while respecting model limits.

- Storage: Each cleaned chunk is stored as a .txt file for transparency, easier inspection, and possible reprocessing.

## Model Selection  
- Embedding Model: Used OpenAI’s text-embedding-ada-002 (via LangChain). Chosen for its high semantic accuracy, robustness, and industry-wide acceptance for vector search.

- LLM: Used OpenAI’s GPT (via ChatOpenAI) for answer synthesis because it gives high-quality, context-aware, instruction-following outputs.

## AI Tools Used  
- LangChain: The backbone for pipeline construction, providing easy integration of all RAG components.

- OpenAI API: For best-in-class embedding and generative language model capabilities.

- FAISS: For local, fast, scalable vector retrieval, with no external DB dependency.

- FastAPI: For exposing the assistant as a production-ready REST API endpoint.

## Challenges Faced  
- Dynamic/Messy HTML: Some loan pages had inconsistent or deeply nested structures, requiring careful extraction and cleaning.

- Solution: Used BeautifulSoup to remove unnecessary tags and focused on extracting the main content.

- Link Discovery: Product links were scattered across navigation and internal menus.

- Solution: Automated extraction and filtering of sublinks containing "loan" in the URL to capture all relevant pages.

- Pickle Safety (FAISS): Recent FAISS versions require explicit permission for loading pickle files.

- Solution: Used allow_dangerous_deserialization=True only with locally created, trusted indexes.

## Potential Improvements
- Deeper Recursive Crawling: Recursively crawl internal links for even more complete data coverage.

- Automated Data Refresh: Schedule periodic scraping to keep knowledge base up to date.

- UI Frontend: Add a web or chat interface for easier access.

- Multi-Bank or Multi-Source Support: Extend to more banks or data sources.

- Advanced RAG: Add question classification, better prompt engineering, or smarter context selection.

## Demo  
Add your Loom, YouTube, or Google Drive video walkthrough link here.

## Contact
For questions or suggestions, please contact:  
Shubham Thote – [shubhamthote2197@gmail.com]
