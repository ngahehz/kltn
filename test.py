from docx import Document
from elasticsearch import Elasticsearch
from underthesea import word_tokenize
from sentence_transformers import SentenceTransformer
from PyQt6.QtCore import QThread, pyqtSignal
import PyPDF2

model_embedding = SentenceTransformer('VoVanPhuc/sup-SimCSE-VietNamese-phobert-base')

CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

index_name = "test_tina1"
path_index = "test_search/config/index.json"

client = Elasticsearch(
    "https://localhost:9200",
    ssl_assert_fingerprint=CERT_FINGERPRINT,
    basic_auth=("elastic", ELASTIC_PASSWORD)
)

def embed_text(text):
    embedding = model_embedding.encode(text)
    return embedding.tolist()

def init():
    print(f"Creating the {index_name} index.")
    if not client.indices.exists(index=index_name):
        print(f"The index {index_name} does not exist. Creating...")
        with open(path_index) as index_file:
            source = index_file.read().strip()
            
        client.indices.create(index=index_name, body=source)
    else:
        print(f"The index {index_name} already exists. Skipping creation.")


def add_elastic_search(id, path, ext):
    init()
    if ext == '.docx':
        doc = Document(path)
        content = ''
        for para in doc.paragraphs:
            content += para.text + '\n'
    else:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            content = ""
            for page_number in range(len(reader.pages)):
                page = reader.pages[page_number]
                content += page.extract_text()

    title = word_tokenize(content, format="text")
    title_vector = embed_text(title)

    doc = {
        'id': id,
        'content': content,
        "title_vector" : title_vector,
    }

    response = client.index(index=index_name, document=doc)

    print(response['result'])
    client.indices.refresh(index=index_name)



class PDFReaderThread(QThread):
    finished = pyqtSignal()

    def __init__(self, id, file_path, ext):
        super().__init__()
        self.id = id
        self.file_path = file_path
        self.ext = ext

    def run(self):
        add_elastic_search(self.id, self.file_path, self.ext)
        self.finished.emit()


        

