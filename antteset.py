# import PyPDF2
# from datetime import datetime

# from elasticsearch import Elasticsearch 

# # Kết nối tới Elasticsearch trên localhost với port mặc định là 9200
# # es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'wHf*2*Go0DX52qFzSIpa'))

# CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
# ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

# client = Elasticsearch(
#     "https://localhost:9200",
#     ssl_assert_fingerprint=CERT_FINGERPRINT,
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )

# # text = ["Bình Nhưỡng 'đổ dầu' vào chảo lửa Triều - Hàn",
# #         "32 năm tù cho những kẻ phạm tội bắt cóc tống tiền",
# #         "Trung Quốc phát hiện 1,5 tỷ USD tham nhũng",
# #         "Những cổ động viên 'chất' nhất của đội tuyển U23 Việt Nam",
# #         "Thủ tướng tiếp Đại sứ Thụy Sỹ Jean Hubert Lebet"]

# # # Định nghĩa tài liệu để index
# # for i in range(5):
# #     doc = {
# #         'author': 'unknown',
# #         'content': text[i],
# #         'timestamp': datetime.now(),
# #     }

# #     # Index tài liệu
# #     response = client.index(index="my-index", document=doc)
# #     print(response['result'])



# # print(client.info())

# index_name = 'my-index'



# # Sử dụng API count để đếm số lượng tài liệu trong index
# count_response = client.count(index=index_name)

# # Số lượng tài liệu trong index
# document_count = count_response['count']
# print("Số lượng tài liệu trong index '{}' là: {}".format(index_name, document_count))




# query = {
#     "query": {
#         "match": {
#             "content": "Nhưỡng"
#         }
#     }
# }

# # Thực hiện truy vấn
# search_result = client.search(index="my-index", body=query)

# # Xử lý kết quả
# print("Took:", search_result["took"])
# print("Hits:", search_result["hits"]["total"]["value"])
# print("Max Score:", search_result["hits"]["max_score"])

# # Lặp qua danh sách các tài liệu và in ra thông tin của mỗi tài liệu
# for hit in search_result['hits']['hits']:
#     print("\nIndex:", hit['_index'])
#     print("ID:", hit['_id'])
#     print("Score:", hit['_score'])
#     print("Source:")
#     for key, value in hit['_source'].items():
#         print(f"  {key}: {value}")

# # indices_info = client.cat.indices(v=True)

# # # In ra thông tin
# # print(indices_info)

# analyzer_info = client.indices.get_field_mapping(index="my-index", fields='*', include_defaults=True)

# # In ra thông tin chi tiết về Standard Analyzer
# print("Standard Analyzer Configuration:")
# print(analyzer_info["my-index"]['mappings']['properties']['content']['analyzer'])



# ------------------------------------------------




# from elasticsearch import Elasticsearch

# CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
# ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

# client = Elasticsearch(
#     "https://localhost:9200",
#     ssl_assert_fingerprint=CERT_FINGERPRINT,
#     basic_auth=("elastic", ELASTIC_PASSWORD)
# )

# result = client.search(index='test_tina1', body={"query": {"match_all": {}}})

# # Lặp qua kết quả trả về và in ra thông tin của từng tài liệu
# for hit in result['hits']['hits']:
#     doc = hit['_source']
#     print("ID:", doc['id'])
#     # print("Content:", doc['content'])
#     # print("Title Vector:", doc['title_vector'])
#     print()  # In một dòng trống để phân biệt giữa các tài liệu


from elasticsearch import Elasticsearch


CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

es = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# Xóa toàn bộ index
index_name = "tina1"

try:
    response = es.indices.delete(index=index_name)
    print("Index đã được xóa thành công:", index_name)
except Exception as e:
    print("Lỗi khi xóa index:", e)


    # def embed_text(self, batch_text):
    ##     if isinstance(batch_text, str):
    ##        batch_text = [batch_text]

    #     encoded_input = self.PhobertTokenizer(batch_text, padding=True, truncation=True, return_tensors='pt')
    #     encoded_input = {k: v.to(self.model_embedding.device) for k, v in encoded_input.items()}
    #     with torch.no_grad():
    #         model_output = self.model_embedding(**encoded_input)
        
    #     input_mask_expanded = encoded_input['attention_mask'].unsqueeze(-1).expand(model_output.last_hidden_state.size()).float()
    #     sum_embeddings = torch.sum(model_output.last_hidden_state * input_mask_expanded, 1)
    #     sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    #     mean_pooled_embeddings = sum_embeddings / sum_mask
        
    #     return [vector.tolist() for vector in mean_pooled_embeddings]
    

        

