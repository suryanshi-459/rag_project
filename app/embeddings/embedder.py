from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.docstore.document import Document
import os

# Create embeddings model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Set where to store the Chroma DB
DB_DIR = "chroma_db"

def embed_and_store(chunks, doc_id: str):
    if not chunks:
        raise ValueError("No chunks to embed.")

    documents = [Document(page_content=chunk, metadata={"source": doc_id}) for chunk in chunks]

    # Load existing DB or create a new one
    if os.path.exists(DB_DIR):
        print("[INFO] Appending to existing Chroma DB...")
        db = Chroma(persist_directory=DB_DIR, embedding_function=embedding_model)
        db.add_documents(documents)
    else:
        print("[INFO] Creating new Chroma DB...")
        db = Chroma.from_documents(documents, embedding_model, persist_directory=DB_DIR)

    # No need for persist or save_local explicitly as it's handled internally
