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
        # print(len(query_vector))
        # print('TIME EMBEDDING ', time.time() - time_embed)
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


    with client.options(ignore_status=[400]):
        response = client.search(
            index='demo_simcse',
            body={
                "size": 10,
                "query": script_query,
                "_source": {
                    "includes": ["id", "title"]
                },
            }
        )
        
    result = []
    # print(response)
    for hit in response["hits"]["hits"]:
        result.append(hit["_source"]['title'])
    return result

# print(search('kinh tế', 'SimCSE'))
# print(search('văn hóa', ' '))
print(search('Đời sống', 'SimCSE'))

titles = ["Công nghệ", "Giáo dục", "Giải trí", "Khoa học", "Kinh tế", "Nhà đất", "Pháp luật",
          "Thế giới", "Thể thao", "Văn hóa", "Xe cộ", "Xã hội", "Đời sống"]



# Thực hiện truy vấn để lấy tất cả các tài liệu từ chỉ mục

# response = client.search(index="tina1", body={"query": {"match_all": {}}})
# response = client.search(index="tina1", id = 1000)

# # In ra ID và body của mỗi tài liệu
# for doc in response['hits']['hits']:
#     print(f"ID: {doc['_id']}")
#     print(f"Body: {doc['_source']}")
#     print("-------------")




# resp = client.get(index="tina1", id=1000)
# print(resp['_source'])





# result = client.search(index='test_tina1', body={"query": {"match_all": {}}})

# # Lặp qua kết quả trả về và in ra thông tin của từng tài liệu
# for hit in result['hits']['hits']:
#     doc = hit['_source']
#     print("ID:", doc['id'])
#     # print("Content:", doc['content'])
#     # print("Title Vector:", doc['title_vector'])
#     print()  # In một dòng trống để phân biệt giữa các tài liệu

