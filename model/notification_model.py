class NotificationModel:
    def __init__(self):
        self._notification = {}

    def add_all_notification(self, notification):
        self._notification = notification

    def add_notification(self, row):
        self._notification[row[0]] = row

    def get_notification(self):
        return self._notification