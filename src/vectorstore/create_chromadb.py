import chromadb

client = chromadb.PersistentClient(
    path="data/vector_db"
)
