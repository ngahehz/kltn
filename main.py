import sys

from view.dashboard_view import *

from controller.document_controller import DocumentController
from controller.setting_controller import SettingController
from controller.dashboard_controller import MainController

from model.file_model import FileModel
from model.image_model import ImageModel
from model.notification_model import NotificationModel
from model.label_model import LabelModel
from model.setting_model import SettingModel
from model.icon_color_model import IconModel
from model.tag_model import TagModel
from model.file_tag_model import FileTagModel

from PyQt6.QtWidgets import QApplication

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self._file_model = FileModel()
        self._image_model = ImageModel()
        self._notification_model = NotificationModel()
        self._label_model = LabelModel()
        self._setting_model = SettingModel()
        self._icon_model = IconModel()
        self._tag_model = TagModel()
        self._file_tag_model = FileTagModel()

        self._document_controller = DocumentController(self._file_model, self._notification_model, self._label_model, self._tag_model, self._file_tag_model)
        self._setting_controller = SettingController(self._image_model, self._setting_model, self._icon_model )
        self._dashboard_controller = MainController(self._file_model, self._notification_model, self._label_model, self._setting_model)

        self.ui = MyWindow(self._dashboard_controller, self._document_controller, self._setting_controller)
        self.ui.show()
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
    
    # from elasticsearch import Elasticsearch

    # CERT_FINGERPRINT = "a621638c3d236dffb6be182fe2dac0dbd97d0ea27e823c6269beb3d3d69f93d4"
    # ELASTIC_PASSWORD = "xtX3XzQB1JJS=9MeADZK"

    # client = Elasticsearch(
    #     "https://localhost:9200",
    #     ssl_assert_fingerprint=CERT_FINGERPRINT,
    #     basic_auth=("elastic", ELASTIC_PASSWORD)
    # )

    # result = client.search(index='test_tina1', body={"query": {"match_all": {}}})

    # # Lặp qua kết quả trả về và in ra thông tin của từng tài liệu
    # for hit in result['hits']['hits']:
    #     doc = hit['_source']
    #     print("ID:", doc['id'])
    #     # print("Content:", doc['content'])
    #     # print("Title Vector:", doc['title_vector'])
    #     print()  # In một dòng trống để phân biệt giữa các tài liệu
