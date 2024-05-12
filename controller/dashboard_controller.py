from database.dao_file import *
from database.dao_label import *
from database.dao_notification import *
from database.dao_setting import *

class MainController(object):
    def __init__(self, file_model, notification_model, label_model, setting_model):
        super().__init__()

        self._file_model = file_model
        self._notification_model = notification_model
        self._label_model = label_model
        self._setting_model = setting_model

        self.load()
        

    def load(self):
        if(len(self.get_files()) == 0):
            self._file_model.add_all_file({i[0]: list(i) for i in getFileAll()})

        if(len(self.get_labels()) == 0):
            self._label_model.add_all_label({i[0]: list(i) for i in getLabelAll()})

        if(len(self.get_notifications()) == 0):
            self._notification_model.add_all_notification({i[0]: list(i) for i in getNotificationAll()})

        if(len(self.get_settings()) == 0):
            self._setting_model.add_all_setting({i[0]: list(i) for i in getSettingAll()})

    def get_files(self, label = None):
        if label:
            return {key: value for key, value in self._file_model.get_file().items() if value[6] == label}
        return self._file_model.get_file()
    
    def get_labels(self):
        return self._label_model.get_label()
    
    def get_notifications(self):
        return self._notification_model.get_notification()
    
    def get_settings(self):
        return self._setting_model.get_setting()
    
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

    def check_read_status(self):
        count = 0
        for row in self.get_notifications().values():
            if row[4] == 0:
                count += 1
        return count
    
    def check_name_label_is_exist(self, name):
        for value in self.get_labels().values():
            if value[1] == name:
                return True
        return False
    
    def update_read_status_of_notification(self, id):
        updateNotification(id, 1)
        self.get_notifications()[id][4] = 1

    def get_url_by_id_file(self, id):
        # int(id)
        if id not in self.get_files():
            print("File id not found")
            return False
        return self.get_files()[id][2]
            

    def remove_label_from_file(self, id):
        for value in self.get_files().values():
            if value[6] == id:
                updateFileLabel(value[0], None)
                value[6] = None
                
    def delete_label(self, id):
        id = int(id)
        self.remove_label_from_file(id)
        # if id not in self.get_labels(): # đống này chi v ta
        #     print("Label not found")
        #     return
        deleteLabel(id)
        del self.get_labels()[id]
