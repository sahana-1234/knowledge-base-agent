import os
from chromadb import PersistentClient

# Absolute path to /db folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db")

# Shared Chroma client (auto-persistent in ChromaDB 0.5+)
client = PersistentClient(path=DB_PATH)
