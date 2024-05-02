class SettingModel:
    def __init__(self):
        self._setting = {}

    def add_all_setting(self, setting):
        self._setting = setting

    def add_setting(self, row):
        self._setting[row[0]] = row

    def get_setting(self):
        return self._setting