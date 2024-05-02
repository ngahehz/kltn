class FileTagModel:
    def __init__(self):
        self._filetag = {}

    def add_all_filetag(self, filetag):
        self._filetag = filetag

    def add_filetag(self, row):
        self._filetag[row[0]] = row

    def get_filetag(self):
        return self._filetag