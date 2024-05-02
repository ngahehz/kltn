import sqlite3

def createTableNotification():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "NOTIFICATION" (
        "ID"	INTEGER NOT NULL,
        "FILE_ID"	INTEGER NOT NULL,
	    "FILE_PATH"	TEXT NOT NULL,
        "NOTE"	TEXT,
        "READ_STATUS"	INTEGER NOT NULL,
        "TIME_STAMP"	TEXT NOT NULL,
        PRIMARY KEY("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addNotification(id, file_id, file_path, note, read_status, time_stamp):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """ INSERT INTO NOTIFICATION (ID, FILE_ID, FILE_PATH, NOTE, READ_STATUS, TIME_STAMP)
                VALUES (?, ?, ?, ?, ?, ?) """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, file_id, file_path, note, read_status, time_stamp))

    dataConnect.commit()
    dataConnect.close()

def updateNotification(id, read_status):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE NOTIFICATION SET 
            READ_STATUS = ?
        WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (read_status, id)) 

    dataConnect.commit()
    dataConnect.close()


def deleteNotification(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM NOTIFICATION WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) 

    dataConnect.commit()
    dataConnect.close()


def getNotificationAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM NOTIFICATION
    """
    cursor = dataConnect.cursor()
    NotificationList = cursor.execute(query).fetchall()
    
    return NotificationList
