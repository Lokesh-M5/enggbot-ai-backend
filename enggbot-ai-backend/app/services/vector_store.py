import uuid
import chromadb

from sentence_transformers import SentenceTransformer

# ==========================================================
# CHROMADB
# ==========================================================

client = chromadb.PersistentClient(path="./chroma_db")

try:

    collection = client.get_collection(
        name="enggbot_memory"
    )

except Exception:

    collection = client.create_collection(
        name="enggbot_memory"
    )

# ==========================================================
# EMBEDDING MODEL
# ==========================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

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

        embedding = embedding_model.encode(
            text
        ).tolist()

        collection.add(

            ids=[str(uuid.uuid4())],

            documents=[text],

            embeddings=[embedding]

        )

    except Exception as e:

        print(
            "Vector Store Error:",
            e
        )


# ==========================================================
# SEARCH MEMORY
# ==========================================================

def search_memory(query):

    if not query:
        return []

    try:

        query_embedding = embedding_model.encode(
            query
        ).tolist()

        results = collection.query(

            query_embeddings=[query_embedding],

            n_results=3

        )

        docs = results.get(
            "documents",
            []
        )

        if not docs:
            return []

        # flatten list

        return docs[0]

    except Exception as e:

        print(
            "Vector Search Error:",
            e
        )

        return []