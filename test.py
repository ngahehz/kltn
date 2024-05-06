from docx import Document
from elasticsearch import Elasticsearch
from underthesea import word_tokenize
from PyQt6.QtCore import QThread, pyqtSignal
import PyPDF2
import torch
from transformers import AutoModel, AutoTokenizer

class PDFReaderThread(QThread):
    finished = pyqtSignal()

    def __init__(self, id, file_path, ext):
        super().__init__()
        self.id = id
        self.file_path = file_path
        self.ext = ext

        self.PhobertTokenizer = AutoTokenizer.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")
        self.model_embedding = AutoModel.from_pretrained("VoVanPhuc/sup-SimCSE-VietNamese-phobert-base")

        CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
        ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

        self.index_name = "test_tina1"
        self.path_index = "test_search/config/index.json"

        self.client = Elasticsearch(
            "https://localhost:9200",
            ssl_assert_fingerprint=CERT_FINGERPRINT,
            basic_auth=("elastic", ELASTIC_PASSWORD)
)

    def run(self):
        self.add_elastic_search(self.id, self.file_path, self.ext)
        self.finished.emit()

    def add_elastic_search(self, id, path, ext):
        self.init()
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
        title_vector = self.embed_text(title)

        doc = {
            'id': id,
            'content': content,
            "title_vector" : title_vector,
        }

        response = self.client.index(index=self.index_name, document=doc)

        print(response['result'])
        self.client.indices.refresh(index=self.index_name)

    def init(self):
        print(f"Creating the {self.index_name} index.")
        if not self.client.indices.exists(index=self.index_name):
            print(f"The index {self.index_name} does not exist. Creating...")
            with open(self.path_index) as index_file:
                source = index_file.read().strip()
                
            self.client.indices.create(index=self.index_name, body=source)
        else:
            print(f"The index {self.index_name} already exists. Skipping creation.")

    def embed_text(self, text):
        # sentences = [tokenize(sentence) for sentence in sentences]
        inputs = self.PhobertTokenizer(text, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            embeddings = self.model_embedding(**inputs, output_hidden_states=True, return_dict=True).pooler_output

        return embeddings.tolist()


        



