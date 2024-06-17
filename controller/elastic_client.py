from elasticsearch import Elasticsearch
from underthesea import word_tokenize

from database.PhoBERTModel import PhoBERTModel

import torch
import regex as re

class ElasticClient:
    CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
    ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

    def __init__(self):
        self._init_client()
        self.PhobertTokenizer = PhoBERTModel.get_tokenizer_instance()
        self.model_embedding = PhoBERTModel.get_model_instance()

    def _init_client(self):
        self.client = Elasticsearch(
            "https://localhost:9200",
            ssl_assert_fingerprint=self.CERT_FINGERPRINT,
            basic_auth=("elastic", self.ELASTIC_PASSWORD)
        )

    def _ensure_client(self):
        if not self.client.ping():
            self._init_client()

    def create_index_if_not_exists(self, index_name="tina1", path_index="json-styles/elastic.json"):
        if not self.client.indices.exists(index=index_name):
            with open(path_index) as index_file:
                source = index_file.read().strip()
            self.client.indices.create(index=index_name, body=source)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")

    def index_document(self, id, text, index_name="tina1"):
        self._ensure_client()
        self.create_index_if_not_exists(index_name)
        # print("text", text)
        # print("fff", word_tokenize(text, format="text"))
        # print("embed", self.embed_text([word_tokenize(text, format="text")])[0])
        
        text = text.lower()
        # text = re.sub(r'https?://\S+', '', text) 
        text = re.sub(r'\[\d+(?:,\s?\d+)*\]', '', text) 

        document = {
            "content": text,
            "content_vector": self.embed_text([word_tokenize(text, format="text")])[0]
        }

        try:
            self.client.get(index=index_name, id=id)
            self.client.update(index=index_name, id=id, doc=document)
            print(f"Updated document {id}")
        except Exception as e:
            self.client.index(index=index_name, id=id, document=document)
            print(f"Created document {id}")
        
        self.client.indices.refresh(index=index_name)


    def delete_document(self, id, index_name="tina1"):
        self._ensure_client()
        try:
            response = self.client.delete(index=index_name, id=id)
            print("Xóa tài liệu thành công:", response)
        except Exception as e:
            print("Lỗi khi xóa tài liệu:", e)

    def search(self, query, type_ranker, index_name="tina1"):
        self._ensure_client()
        if type_ranker == 'SimCSE':
            query_vector = self.embed_text([word_tokenize(query, format="text")])[0]
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


        with self.client.options(ignore_status=[400]):
            response = self.client.search(
                index = index_name,
                body = { 
                    # "size": 2,
                    "query": script_query,
                    # "_source": {
                    #     "includes": ["content", "content_vector"]
                    # },
                }
            )

        # response = self.client.search(
        #     index=index_name,
        #     body = {
        #         "query": script_query,
        #         "_source": {
        #             "includes": [ "content"]
        #         },
        #     },
        #     ignore=[400]
        # )
            
        result = []

        for hit in response["hits"]["hits"]:
            result.append([hit["_score"], hit["_id"], hit["_source"]['content']])
            # print(hit)
        return result
    
    # def embed_text(self, batch_text):
    #     inputs = self.PhobertTokenizer(batch_text, return_tensors="pt", padding=True, truncation=True)
    #     with torch.no_grad():
    #         outputs = self.model_embedding(**inputs)
    #         embeddings = outputs.last_hidden_state[:, 0, :]
    #     return embeddings.cpu().tolist()

    
    # def embed_text(self, text):
    #     inputs = self.PhobertTokenizer(text, padding=True, truncation=True, return_tensors="pt")
    #     with torch.no_grad():
    #         embeddings = self.model_embedding(**inputs, output_hidden_states=True, return_dict=True).pooler_output
    #     return embeddings.tolist()

    def embed_text(self, texts):
        inputs = self.PhobertTokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model_embedding(**inputs, output_hidden_states=True, return_dict=True).pooler_output
        return embeddings.tolist()


