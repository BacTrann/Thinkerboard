from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_ollama import OllamaEmbeddings
from db.db import connect_db_client
from pymongo import MongoClient

# initialize MongoDB python client
client = connect_db_client()
embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

# DB_NAME = "langchain_test_db"
# COLLECTION_NAME = "langchain_test_vectorstores"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"

MONGODB_COLLECTION = client


def get_vectorstore() -> MongoDBAtlasVectorSearch:
    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=embeddings,
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )
    return vector_store


def get_embedding(query: str):
    return embeddings.embed_query(query)
