import PyPDF2
from datetime import datetime

from elasticsearch import Elasticsearch 

# Kết nối tới Elasticsearch trên localhost với port mặc định là 9200
# es = Elasticsearch(['https://localhost:9200'], basic_auth=('elastic', 'wHf*2*Go0DX52qFzSIpa'))

CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

# text = ["Bình Nhưỡng 'đổ dầu' vào chảo lửa Triều - Hàn",
#         "32 năm tù cho những kẻ phạm tội bắt cóc tống tiền",
#         "Trung Quốc phát hiện 1,5 tỷ USD tham nhũng",
#         "Những cổ động viên 'chất' nhất của đội tuyển U23 Việt Nam",
#         "Thủ tướng tiếp Đại sứ Thụy Sỹ Jean Hubert Lebet"]

# # Định nghĩa tài liệu để index
# for i in range(5):
#     doc = {
#         'author': 'unknown',
#         'content': text[i],
#         'timestamp': datetime.now(),
#     }

#     # Index tài liệu
#     response = client.index(index="my-index", document=doc)
#     print(response['result'])



# print(client.info())

index_name = 'my-index'



# Sử dụng API count để đếm số lượng tài liệu trong index
count_response = client.count(index=index_name)

# Số lượng tài liệu trong index
document_count = count_response['count']
print("Số lượng tài liệu trong index '{}' là: {}".format(index_name, document_count))




query = {
    "query": {
        "match": {
            "content": "Nhưỡng"
        }
    }
}

# Thực hiện truy vấn
search_result = client.search(index="my-index", body=query)

# Xử lý kết quả
print("Took:", search_result["took"])
print("Hits:", search_result["hits"]["total"]["value"])
print("Max Score:", search_result["hits"]["max_score"])

# Lặp qua danh sách các tài liệu và in ra thông tin của mỗi tài liệu
for hit in search_result['hits']['hits']:
    print("\nIndex:", hit['_index'])
    print("ID:", hit['_id'])
    print("Score:", hit['_score'])
    print("Source:")
    for key, value in hit['_source'].items():
        print(f"  {key}: {value}")

# indices_info = client.cat.indices(v=True)

# # In ra thông tin
# print(indices_info)

analyzer_info = client.indices.get_field_mapping(index="my-index", fields='*', include_defaults=True)

# In ra thông tin chi tiết về Standard Analyzer
print("Standard Analyzer Configuration:")
print(analyzer_info["my-index"]['mappings']['properties']['content']['analyzer'])