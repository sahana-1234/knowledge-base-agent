import os
from chroma_client import client
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embedding model
EMBED_MODEL = "nomic-embed-text"
embeddings = OllamaEmbeddings(model=EMBED_MODEL)

# Shared vector DB (same one used by app.py)
vector_db = Chroma(
    client=client,
    collection_name="kb_agent",
    embedding_function=embeddings
)

def ingest_pdf(path):
    loader = PyPDFLoader(path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    vector_db.add_documents(chunks)  # <-- Auto-persist handled by Chroma 0.5+
    print(f"Ingested {len(chunks)} chunks from {os.path.basename(path)}")

if __name__ == "__main__":
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

    for file in os.listdir(DATA_DIR):
        if file.endswith(".pdf"):
            ingest_pdf(os.path.join(DATA_DIR, file))

    print("Background ingestion complete.")
