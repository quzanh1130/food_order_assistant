import os
import pandas as pd
from tqdm.auto import tqdm
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch


MODEL_NAME = 'multi-qa-MiniLM-L6-cos-v1'
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://elasticsearch:9200")
ELASTIC_URL_LOCAL = os.getenv("ELASTIC_URL", "http://localhost:9200")
DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")
INDEX_NAME = "food-list"

def fetch_documents():
    print("Fetching documents...")
    df = pd.read_csv(DATA_PATH)
    df['price'] = df['price'].astype(str)
    df['calories'] = df['calories'].astype(str)
    documents = df.to_dict(orient="records")
    print(f"Fetched {len(documents)} documents")
    return documents

def load_model():
    print(f"Loading model: {MODEL_NAME}")
    return SentenceTransformer(MODEL_NAME)


def setup_elasticsearch():
    print("Setting up Elasticsearch...")
    es_client = Elasticsearch(ELASTIC_URL_LOCAL)

    index_settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "name": {"type": "text"},
                "cuisine": {"type": "text"},
                "type": {"type": "text"},
                "ingredients": {"type": "text"},
                "serving": {"type": "text"},
                "price": {"type": "text"},
                "calories": {"type": "text"},
                "name_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
                "cuisine_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
                "type_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
                "ingredients_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
                "text_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
            }
        }
    }

    es_client.indices.delete(index=INDEX_NAME, ignore_unavailable=True)
    es_client.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"Elasticsearch index '{INDEX_NAME}' created")
    return es_client


def index():
    index_elastic = Elasticsearch(ELASTIC_URL)
    return index_elastic


def index_documents(es_client, documents, model):
    print("Indexing documents...")
    for doc in tqdm(documents):
        name = doc["name"]
        cuisine = doc["cuisine"]
        types = doc["type"]
        ingredients = doc["ingredients"]
        serving = doc["serving"]
        price = doc["price"]
        calories = doc["calories"]
        doc['name_vector'] = model.encode(name)
        doc['cuisine_vector'] = model.encode(cuisine)
        doc['type_vector'] = model.encode(types)
        doc['ingredients_vector'] = model.encode(ingredients)
        doc["text_vector"] = model.encode(name + " " + cuisine + " " + types \
                                          + " " + ingredients + " " + serving + " " + price + " " + calories \
                                         ).tolist()
        es_client.index(index=INDEX_NAME, document=doc)
    print(f"Indexed {len(documents)} documents")


def ingest_data():
    # you may consider to comment <start>
    # if you just want to init the db or didn't want to re-index
    print("Starting the indexing process...")

    documents = fetch_documents()
    model = load_model()
    es_client = setup_elasticsearch()
    index_documents(es_client, documents, model)
    
    print("Indexing completed")
