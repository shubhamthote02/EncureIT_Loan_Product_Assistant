from langchain.prompts import PromptTemplate

DEFAULT_PROMPT = """
You are an expert assistant for the Bank of Maharashtra. Use ONLY the context provided below to answer the user's loan product question as accurately as possible.

Context:
{context}

User Question:
{question}

If you do not know the answer from the provided context, reply "Sorry, I do not have enough information."
"""

def get_prompt():
    """
    Returns a formatted prompt template for Bank of Maharashtra loan QA.

    Returns:
        PromptTemplate: LangChain prompt template instance.
    """
    return PromptTemplate.from_template(DEFAULT_PROMPT)
