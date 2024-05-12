
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from underthesea import word_tokenize
from transformers import AutoModel, AutoTokenizer
import torch, time

import pandas as pd

CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

PhobertTokenizer = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
model_embedding = AutoModel.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")

index_name = "demo_simcse"
path_index = "test_search/config/index.json"
path_data = "test_search/data/data_title.csv"
batch_size = 128

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)


def embed_text(batch_text):
    encoded_input = PhobertTokenizer(batch_text, padding=True, truncation=True, return_tensors='pt')
    encoded_input = {k: v.to(model_embedding.device) for k, v in encoded_input.items()}
    with torch.no_grad():
        model_output = model_embedding(**encoded_input)
    
    input_mask_expanded = encoded_input['attention_mask'].unsqueeze(-1).expand(model_output.last_hidden_state.size()).float()
    sum_embeddings = torch.sum(model_output.last_hidden_state * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    mean_pooled_embeddings = sum_embeddings / sum_mask
    
    return [vector.tolist() for vector in mean_pooled_embeddings]


# def embed_text(batch_text):
#     batch_embedding = model_embedding.encode(batch_text)
#     return [vector.tolist() for vector in batch_embedding]


# def index_batch(docs):
#     requests = []
#     titles = [word_tokenize(doc["title"], format="text") for doc in docs]
#     title_vectors = embed_text(titles)
#     for i, doc in enumerate(docs):
#         request = doc
#         request["_op_type"] = "index"
#         request["_index"] = index_name
#         request["title_vector"] = title_vectors[i]
#         requests.append(request)
#     bulk(client, requests)


# print(f"Creating the {index_name} index.")
# client.indices.delete(index=index_name, ignore=[404])
# with open(path_index) as index_file:
#     source = index_file.read().strip()
#     client.indices.create(index=index_name, body=source)

# docs = []
# count = 0
# df = pd.read_csv(path_data).fillna(' ')
# for index, row in df.iterrows():
#     count += 1
#     item = {
#         'id': row['id'],
#         'title': row['title']
#     }
#     docs.append(item)
#     if count % batch_size == 0:
#         index_batch(docs)
#         docs = []
#         print("Indexed {} documents.".format(count))
# if docs:
#     index_batch(docs)
#     print("Indexed {} documents.".format(count))

# client.indices.refresh(index=index_name)
# print("Done indexing.")



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
            #   "content": {
              "title": {
                "query": query,
                "fuzziness": "AUTO"
              }
            }
        }


    response = client.search(
        index='demo_simcse',
        # index='test_tina1',
        body={
            "size": 10,
            "query": script_query,
            "_source": {
                "includes": ["id", "title"]
                # "includes": ["id", "content"]

            },
        },
        ignore=[400]
    )

    result = []
    print(response)
    for hit in response["hits"]["hits"]:
        result.append(hit["_source"]['title'])
        # result.append(hit["_source"]['id'])
    return result

print(search('tình yêu tuổi học trò', 'SimCSE'))
print(search('tình yêu tuổi học trò', ''))