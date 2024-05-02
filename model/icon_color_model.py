class IconModel:
    def __init__(self):
        self._icon = {}

    def add_all_icon(self, icon):
        self._icon = icon

    def add_icon(self, row):
        self._icon[row[0]] = row

    def get_icon(self):
        return self._icon