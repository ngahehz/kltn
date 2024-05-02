class LabelModel:
    def __init__(self):
        self._label = {}

    def add_all_label(self, label):
        self._label = label

    def add_label(self, row):
        self._label[row[0]] = row

    def get_label(self):
        return self._label