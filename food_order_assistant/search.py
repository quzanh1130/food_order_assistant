from ingest import INDEX_NAME, load_model, index

model_encoder = load_model()

def elastic_search_hybrid(query):
    field = "name_vector"
    vector = model_encoder.encode(query)
    es_client = index()
    
    knn_query = {
        "field": field,
        "query_vector": vector,
        "k": 10,
        "num_candidates": 10000,
        "boost": 0.5
    }

    keyword_query = {
        "bool": {
            "must": {
                "multi_match": {
                    "query": query,
                    "fields": ["name", "cuisine", "type", "ingredients", "serving", "price", "calories"],
                    "type": "best_fields",
                    "boost": 0.5,
                }
            }
        }
    }

    search_query = {
        "knn": knn_query,
        "query": keyword_query,
        "size": 10,
        "_source": ["name", "cuisine", "type", "ingredients", "serving", "price", "calories", "id"]
    }

    
    es_results = es_client.search(
        index=INDEX_NAME,
        body=search_query
    )
    
    result_docs = []
    
    for hit in es_results['hits']['hits']:
        result_docs.append(hit['_source'])

    return result_docs