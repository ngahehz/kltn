class FileModel:
    def __init__(self):
        self._file = {}

    def add_all_file(self, file):
        self._file = file

    def add_file(self, row):
        self._file[row[0]] = row

    def get_file(self):
        return self._file