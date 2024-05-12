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
index_name = "demo_simcse"

try:
    response = es.indices.delete(index=index_name)
    print("Index đã được xóa thành công:", index_name)
except Exception as e:
    print("Lỗi khi xóa index:", e)
