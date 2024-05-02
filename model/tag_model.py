class TagModel:
    def __init__(self):
        self._tag = {}

    def add_all_tag(self, tag):
        self._tag = tag

    def add_tag(self, row):
        self._tag[row[0]] = row

    def get_tag(self):
        return self._tag