from elasticsearch import Elasticsearch
from underthesea import word_tokenize
from transformers import AutoModel, AutoTokenizer
import torch


CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

PhobertTokenizer = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
model_embedding = AutoModel.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

def embed_text(batch_text):
    
    inputs = PhobertTokenizer(batch_text, return_tensors="pt", padding=True, truncation=True)
    
    # Forward pass through the model
    with torch.no_grad():
        outputs = model_embedding(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
        # embeddings = outputs.last_hidden_state  # Assuming model returns last hidden states
    
    # Convert embeddings to list of vectors
    # embedded_vectors = [vector.tolist() for vector in embeddings]
    # return embedded_vectors
    return embeddings.cpu().tolist()
    

def search(query, type_ranker):
    if type_ranker == 'SimCSE':
        query_vector = embed_text([word_tokenize(query, format="text")])[0]
        script_query = {

            "script_score": {
                "query": {
                    "match_all": {}
                }
                ,
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'content_vector') + 1.0",
                    "params": {"query_vector": query_vector}
                }
            }
        }
    else:
        script_query = {
            "match": {
              "content": {
                "query": query,
                "fuzziness": "AUTO"
              }
            }
        }


    with client.options(ignore_status=[400]):
        response = client.search(
            index='tina1',
            body={
                "size": 10,
                "query": script_query,
            }
        )
        
    result = []
    for hit in response["hits"]["hits"]:
        result.append(hit["_id"])
    return result

print(search('tình yêu tuổi học trò', 'SimCSE'))


# response = client.search(index="tina1", body={"query": {"match_all": {}}})

# # In ra ID và body của mỗi tài liệu
# for doc in response['hits']['hits']:
#     print(f"ID: {doc['_id']}")
#     print(f"Body: {doc['_source']}")
#     print("---")