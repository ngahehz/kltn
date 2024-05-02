class ImageModel:
    def __init__(self):
        self._image = {}

    def add_all_image(self, image):
        self._image = image

    def add_image(self, row):
        self._image[row[0]] = row

    def get_image(self):
        return self._image