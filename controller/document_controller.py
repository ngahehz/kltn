from database.dao_file import *
from database.dao_label import *
from database.dao_notification import *
from database.dao_image import *
from database.dao_tag import *
from database.dao_file_tag import *
from test import PDFReaderThread

class DocumentController(object):
    def __init__(self, file_model, notification_model, label_model, tag_model, file_tag_model):
        super().__init__()

        self._file_model = file_model
        self._notification_model = notification_model
        self._label_model = label_model
        self._tag_model = tag_model
        self._file_tag_model = file_tag_model

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
    
    def get_files_tags(self, file_id = None):
        if file_id:
            return {key: value for key, value in self._file_tag_model.get_filetag().items() if value[1] == file_id}
        return self._file_tag_model.get_filetag()

    def add_file_to_database(self, row):
        if len(self.get_files()) == 0:
            new_id = 1000
        else:
            new_id = list(self.get_files().keys())[-1] + 1
            
        addFile(new_id, row[0], row[1], row[2], row[3], row[4])
        self.get_files()[new_id] = [new_id, row[0], row[1], row[2], row[3], row[4], None, None, None, None, 0]
        
        self.thread = PDFReaderThread(new_id, row[1], row[4])
        self.thread.start()
        self.thread.finished.connect(lambda: print("Done"))
        # add_elastic_search(new_id, row[1], row[4])
        return new_id
    
    def update_note_of_file(self, id, note):
        if id not in self.get_files():
            print("File not found")
            return
        updateFileNote(id, note)
        self.get_files()[id][7] = note

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
            
    def check_reminder_in_notification(self, file):
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

    def get_url_by_id_file(self, id):
        return self.get_files()[id][2]
            
    def check_url_is_exist(self, url):
        for value in self.get_files().values():
            if value[2] == url:
                return True
        return False

    def get_label_name_by_id_file(self, id):
        if id not in self.get_labels():
            return ""
        return self.get_labels()[id][1]
            
    def delete_file(self, id):
        deleteFile(id)
        del self.get_files()[id]

    def check_name_label_is_exist(self, name):
        for value in self.get_labels().values():
            if value[1] == name:
                return True
        return False
    
    ### LABEL ###
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
