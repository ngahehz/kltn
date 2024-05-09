import time

# model_embedding = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')

from elasticsearch import Elasticsearch
# from elasticsearch.helpers import bulk
from underthesea import word_tokenize
from transformers import AutoModel, AutoTokenizer
import torch

# from pyvi.ViTokenizer import tokenize
# import pandas as pd

CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

PhobertTokenizer = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
model_embedding = AutoModel.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

def embed_text(text):
    # text_embedding = model_embedding.encode(text)
    # return text_embedding.tolist()

    inputs = PhobertTokenizer(text, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        embeddings = model_embedding(**inputs, output_hidden_states=True, return_dict=True).pooler_output

    return embeddings.tolist()

def search(query, type_ranker):
    if type_ranker == 'SimCSE':
        time_embed = time.time()
        query_vector = embed_text([word_tokenize(query, format="text")])[0]
        print(len(query_vector))
        print('TIME EMBEDDING ', time.time() - time_embed)
        script_query = {

            "script_score": {
                "query": {
                    "match_all": {}
                }
                ,
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'title_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    else:
        script_query = {
            "match": {
              "title": {
                "query": query,
                "fuzziness": "AUTO"
              }
            }
        }


    response = client.search(
        index='demo_simcse',
        body={
            "size": 10,
            "query": script_query,
            "_source": {
                "includes": ["id", "title"]

            },
        },
        ignore=[400]
    )

    result = []
    print(response)
    for hit in response["hits"]["hits"]:
        result.append(hit["_source"]['title'])
    return result

print(search('dạy đời', 'SimCSE'))