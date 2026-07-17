import uuid
import chromadb

# ==========================================================
# CHROMADB
# ==========================================================

client = chromadb.PersistentClient(path="./chroma_db")

try:
    collection = client.get_collection("enggbot_memory")
except Exception:
    collection = client.create_collection("enggbot_memory")

# ==========================================================
# EMBEDDING MODEL (Lazy Load)
# ==========================================================

embedding_model = None

def get_embedding_model():
    global embedding_model

    if embedding_model is None:
        from sentence_transformers import SentenceTransformer
        embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return embedding_model

# ==========================================================
# STORE MEMORY
# ==========================================================

def store_memory(text):

    if not text:
        return

    text = text.strip()

    if not text:
        return

    try:
        model = get_embedding_model()

        embedding = model.encode(text).tolist()

        collection.add(
            ids=[str(uuid.uuid4())],
            documents=[text],
            embeddings=[embedding],
        )

    except Exception as e:
        print("Vector Store Error:", e)

# ==========================================================
# SEARCH MEMORY
# ==========================================================

def search_memory(query):

    if not query:
        return []

    try:
        model = get_embedding_model()

        query_embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
        )

        docs = results.get("documents", [])

        if not docs:
            return []

        return docs[0]

    except Exception as e:
        print("Vector Search Error:", e)
        return []
