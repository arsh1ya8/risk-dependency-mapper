from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.Client()
collection = client.get_or_create_collection(name="risk_docs")


def add_documents(docs):
    for i, doc in enumerate(docs):
        embedding = model.encode(doc).tolist()
        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[str(i)]
        )


def query_docs(query):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"]