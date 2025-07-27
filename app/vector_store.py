import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
FAISS_INDEX_PATH = os.path.join(PROJECT_ROOT, "data", "faiss_index")

def build_faiss_index():
    """
    Loads all processed data chunks, generates embeddings, and builds a FAISS vector store.

    Side Effects:
        Saves the FAISS vector index to disk.
    """
    docs, metadatas = [], []
    for fname in os.listdir(PROC_DIR):
        with open(os.path.join(PROC_DIR, fname), encoding="utf-8") as f:
            text = f.read()
            docs.append(text)
            metadatas.append({"source": fname})
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_texts(docs, embeddings, metadatas=metadatas)
    db.save_local(FAISS_INDEX_PATH)

def load_faiss_index():
    """
    Loads the FAISS vector store from disk using the OpenAI embedding model.

    Returns:
        FAISS: Loaded FAISS vector database instance.
    """
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)

if __name__ == "__main__":
    build_faiss_index()
