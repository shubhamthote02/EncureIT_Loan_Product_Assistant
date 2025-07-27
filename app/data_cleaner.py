import os
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Compute root path dynamically, so the script works from anywhere
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROC_DIR = os.path.join(PROJECT_ROOT, "data", "processed")

def clean_and_chunk_all(chunk_size=500, chunk_overlap=50):
    """
    Reads all raw text files, cleans and splits them into overlapping chunks for vector storage.

    Args:
        chunk_size (int, optional): The max character size for each chunk. Defaults to 500.
        chunk_overlap (int, optional): Number of overlapping characters between chunks. Defaults to 50.

    Side Effects:
        Writes chunked text files to the processed data folder.
    """
    os.makedirs(PROC_DIR, exist_ok=True)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.txt')]

    chunk_count = 0
    for fname in raw_files:
        with open(os.path.join(RAW_DIR, fname), encoding="utf-8") as f:
            text = f.read().strip()
            if len(text) < 100:
                continue
            chunks = splitter.split_text(text)
            base = fname.replace('.txt', '')
            for idx, chunk in enumerate(chunks):
                chunk_fname = f"{base}_chunk{idx}.txt"
                with open(os.path.join(PROC_DIR, chunk_fname), "w", encoding="utf-8") as out:
                    out.write(chunk.strip())
                chunk_count += 1
    print(f"Created {chunk_count} chunks in '{PROC_DIR}'.")

if __name__ == "__main__":
    clean_and_chunk_all()
