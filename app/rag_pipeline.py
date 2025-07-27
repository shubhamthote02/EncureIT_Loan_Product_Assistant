from app.vector_store import load_faiss_index
from langchain_openai import ChatOpenAI
from app.prompt_template import get_prompt
from dotenv import load_dotenv

load_dotenv()

def get_rag_answer(user_question, k=3):
    """
    Handles the complete Retrieval-Augmented Generation (RAG) workflow.

    Steps:
    - Retrieves the top-k most relevant chunks from the vector store.
    - Formats the context and user question into a prompt.
    - Invokes the LLM to generate an answer.

    Args:
        user_question (str): The user's question about loan products.
        k (int, optional): Number of top chunks to retrieve. Defaults to 3.

    Returns:
        str: The generated answer or a fallback message if not enough information.
    """
    db = load_faiss_index()
    docs = db.similarity_search(user_question, k=k)
    if not docs:
        return "Sorry, I do not have enough information."
    context = "\n---\n".join([doc.page_content for doc in docs])
    prompt = get_prompt()
    final_prompt = prompt.format(context=context, question=user_question)
    llm = ChatOpenAI(temperature=0)
    answer = llm.invoke(final_prompt)
    return answer.content
