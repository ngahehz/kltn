from database.dao_file import *
from database.dao_label import *
from database.dao_notification import *
from database.dao_image import *
from database.dao_tag import *
from database.dao_file_tag import *
from database.PhoBERTModel import *

from PyQt6.QtCore import QThread, pyqtSignal
from controller.helper import predict_tag
from controller.elastic_client import *

from docx import Document

import os
import fitz
import string
import threading

class DocumentController(object):
    def __init__(self, file_model, notification_model, label_model, tag_model, file_tag_model):
        super().__init__()

        self._file_model = file_model
        self._notification_model = notification_model
        self._label_model = label_model
        self._tag_model = tag_model
        self._file_tag_model = file_tag_model
        self._lock = threading.Lock()

        self.status = False

        self.load()

    def load(self):
        if(len(self.get_files()) == 0):
            self._file_model.add_all_file({i[0]: list(i) for i in getFileAll()})

        if(len(self.get_labels()) == 0):
            self._label_model.add_all_label({i[0]: list(i) for i in getLabelAll()})

        if(len(self.get_notifications()) == 0):
            self._notification_model.add_all_notification({i[0]: list(i) for i in getNotificationAll()})

        if(len(self.get_tags()) == 0):
            self._tag_model.add_all_tag({i[0]: list(i) for i in getTagAll()})

        if(len(self.get_files_tags()) == 0):
            self._file_tag_model.add_all_filetag({i[0]: list(i) for i in getFileTagAll()})
    
    def get_files(self, label = None):
        if label:
            return {key: value for key, value in self._file_model.get_file().items() if value[6] == label}
        return self._file_model.get_file()
    
    def get_labels(self):
        return self._label_model.get_label()
    
    def get_tags(self):
        return self._tag_model.get_tag()
    
    def get_notifications(self):
        return self._notification_model.get_notification()
    
    def get_files_tags(self, file_id = None, file_tag_id = None):
        if file_id:
            return {key: value for key, value in self._file_tag_model.get_filetag().items() if value[1] == file_id}
        if file_tag_id:
            return {key: value for key, value in self._file_tag_model.get_filetag().items() if value[2] == file_tag_id}
        return self._file_tag_model.get_filetag()

    def add_file_to_database(self, row):
        if len(self.get_files()) == 0:
            new_id = 1000
        else:
            new_id = list(self.get_files().keys())[-1] + 1
            
        addFile(new_id, row[0], row[1], row[2], row[3], row[4])
        self.get_files()[new_id] = [new_id, row[0], row[1], row[2], row[3], row[4], None, None, None, None, 0]
        
        self.thread = AddTagThead(new_id, row[1], self.add_file_tag_to_database)
        self.thread.start()
        self.thread.finished.connect(lambda: print("Done"))

        return new_id
    
    def update_note_of_file(self, id, note):
        if id not in self.get_files():
            print("File not found")
            return
        updateFileNote(id, note)
        self.get_files()[id][7] = note

        self.pdf_thread = ElasticThread(id, note, 1)
        self.pdf_thread.start()
        self.pdf_thread.finished.connect(lambda: print("Done"))
    
    def update_reminder_of_file(self, id, date, note):
        if id not in self.get_files():
            print("File not found")
            return
        updateFileReminder(id, date, note)
        self.get_files()[id][8] = date
        self.get_files()[id][9] = note

    def update_priority_of_file(self, id, priority):
        if id not in self.get_files():
            print("File not found")
            return
        updateFilePriority(id, priority)
        self.get_files()[id][10] = priority
            
    def check_reminder_in_notification(self, file):   # 244 view
        # id_file_noti == id_file and date_noti = date_8
        for value in self.get_notifications().values():
            if value[1] == file[0] and value[5] == file[8]:
                return

        if len(self.get_notifications()) == 0:
            new_id = 100
        else:
            new_id = list(self.get_notifications().keys())[-1] + 1

        if file[9] is not None and file[9] != "":
            note = f"Bạn có một nhắc nhở ở {file[1]}: {file[9]}"
        else:
            note = f"Bạn có một nhắc nhở ở file: {file[1]}"

        addNotification(new_id, file[0], file[2], note, 0, file[8])
        self.get_notifications()[new_id] = [new_id,  file[0], file[2],  note, 0, file[8]]

    def get_url_by_file_id(self, id):
        return self.get_files()[id][2]
            
    def check_url_is_exist(self, url):
        for value in self.get_files().values():
            if value[2] == url:
                return True
        return False

    def get_label_name_by_file_id(self, id): # 191 view
        if id not in self.get_labels():
            return ""
        return self.get_labels()[id][1]
            
    def delete_file(self, id):
        deleteFile(id)
        del self.get_files()[id]
        for key in self.get_files_tags(id):
            deleteFileTag(key)
            del self.get_files_tags()[key]

    ### LABEL ###
    def check_name_label_is_exist(self, name):
        for value in self.get_labels().values():
            if value[1] == name:
                return True
        return False
    
    def add_label_to_database(self, name):
        if self.check_name_label_is_exist(name):
            return False, 0
        
        if len(self.get_labels()) == 0:
            new_id = 100
        else:
            new_id = list(self.get_labels().keys())[-1] + 1

        addLabel(new_id, name)
        self.get_labels()[new_id] = [new_id,  name]
        return True, new_id
    
    def update_label_of_file(self, file_id, label_id):
        updateFileLabel(file_id, label_id)
        self.get_files()[file_id][6] = label_id

    ### TAG ###
    def delete_tag(self, tag_name):
        id = self.get_tag_id_by_name(tag_name)
        deleteTag(id)
        del self.get_tags()[id]
        for key in self.get_files_tags(file_tag_id = id):
            deleteFileTag(key)
            del self.get_files_tags()[key]

    def get_tag_id_by_name(self, name):  # 219 view
        for value in self.get_tags().values():
            if value[1] == name:
                return value[0]
        return None
    
    def check_name_tag_is_exist(self, name):
        for value in self.get_tags().values():
            if value[1] == name:
                return True
        return False
    
    def add_tag_to_database(self, name):
        if self.check_name_tag_is_exist(name):
            return False, 0
        
        if len(self.get_tags()) == 0:
            new_id = 100
        else:
            new_id = list(self.get_tags().keys())[-1] + 1

        addTag(new_id, name)
        self.get_tags()[new_id] = [new_id,  name]
        return True, new_id
    
    ### FILE TAG ###
    def delete_file_tag(self, file_id, tag_id):
        id = self.check_file_tag_is_exist(file_id, tag_id)[1]
        deleteFileTag(id)
        del self.get_files_tags()[id]

    def check_file_tag_is_exist(self, file_id, tag_id):
        for value in self.get_files_tags().values():
            if value[1] == file_id and value[2] == tag_id:
                return True, value[0]
        return False, None
    
    def add_file_tag_to_database(self, file_id, tags_name):
        with self._lock:
            if not isinstance(tags_name, str):
                for tag_name in tags_name:
                    if len(self.get_files_tags()) == 0:
                        new_id = 1000
                    else:
                        new_id = list(self.get_files_tags().keys())[-1] + 1
                    
                    tag_id = self.get_tag_id_by_name(tag_name) # trước đó chỗ này là tag_name[0], why?

                    addFileTag(new_id, file_id, tag_id)
                    self.get_files_tags()[new_id] = [new_id, file_id, tag_id]
            else:
                tag_id = self.get_tag_id_by_name(tags_name)
                if self.check_file_tag_is_exist(file_id, tag_id)[0]:
                        return False, None
                
                if len(self.get_files_tags()) == 0:
                    new_id = 1000
                else:
                    new_id = list(self.get_files_tags().keys())[-1] + 1

                addFileTag(new_id, file_id, tag_id)
                self.get_files_tags()[new_id] = [new_id, file_id, tag_id]
                return True, new_id


class AddTagThead(QThread):
    finished = pyqtSignal()

    def __init__(self, file_id, path, add_file_tag_to_database):
        super().__init__()
        self.file_id = file_id
        self.path = path
        self.add_file_tag_to_database = add_file_tag_to_database

    def run(self):
        text = self.read_file(self.path)
        lb = predict_tag(text)
        self.add_file_tag_to_database(self.file_id, lb)
        self.finished.emit()

    # def read_pdf(self):
    #     with open(self.path, 'rb') as file:
    #         reader = PyPDF2.PdfReader(file)
            
    #         all_text = ""
    #         for page_number in range(len(reader.pages)):
    #             page = reader.pages[page_number]
    #             all_text += page.extract_text()
            
    #     print("đọc  xong")
    #     return all_text
    def extract_text_from_pdf(self, file_path):
        text = ''
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        text  = text.splitlines()
        return self.concatenate_sentences(text)


    def concatenate_sentences(self, sentence_list):
        concatenated_sentence = ""

        for i, sentence in enumerate(sentence_list):
            if sentence == '' or sentence is None:
                continue
            if i == len(sentence_list) - 1:
                concatenated_sentence += sentence
            else:
                ## sentence_list[i + 1] == '' trước để kiểm tra nó có rỗng không
                if sentence[-1] in string.punctuation or sentence_list[i + 1] == '' or sentence_list[i + 1][0] in string.punctuation:
                    concatenated_sentence += sentence
                else:
                    concatenated_sentence += sentence + " "

        return concatenated_sentence

    def read_file(self, path):
        ext = os.path.splitext(path)[1]
        if ext == '.docx':
            doc = Document(path)
            content = ''
            for para in doc.paragraphs:
                content += para.text + '\n'
        else:
            content = self.extract_text_from_pdf(path)
        return content
    

class ElasticThread(QThread):
    finished = pyqtSignal()

    def __init__(self, id, text, action):
        super().__init__()
        self._id = id
        self._text = text
        self._action = action
      
        self.PhobertTokenizer = PhoBERTModel.get_tokenizer_instance()
        self.model_embedding = PhoBERTModel.get_model_instance()

        self.client = ElasticClient()


    def run(self):
        if self._action == 1:
            self.client.index_document(self._id, self._text)
        elif self._action == 2:
            self.client.delete_document(self._id)
        self.finished.emit()