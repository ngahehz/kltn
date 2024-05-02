import sqlite3

def createTableFile():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "FILE" (
        "ID"	INTEGER NOT NULL,
        "FILE_NAME"	TEXT NOT NULL,
        "FILE_PATH"	TEXT NOT NULL,
        "UPLOAD_DATE"	TEXT NOT NULL,
        "FILE_SIZE"	REAL NOT NULL,
        "FILE_TYPE"	TEXT NOT NULL,
        "LABEL_ID"	INTEGER,
        "NOTE"	TEXT,
        "REMINDER_DATE"	TEXT,
        "REMINDER_NOTE"	TEXT,
        "PRIORITY"	INTEGER NOT NULL,
        PRIMARY KEY("ID"),
        FOREIGN KEY("LABEL_ID") REFERENCES "LABEL"("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addFile(id, name, path, date, size, type):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """ INSERT INTO FILE (ID, FILE_NAME, FILE_PATH, UPLOAD_DATE, FILE_SIZE, FILE_TYPE, LABEL_ID, NOTE, REMINDER_DATE, REMINDER_NOTE, PRIORITY)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, name, path, date, size, type, None, None, None, None, 0))

    dataConnect.commit()
    dataConnect.close()

def updateFileNote(id, note):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE FILE SET 
            NOTE = ?
        WHERE ID = ?
    """
    
    cursor = dataConnect.cursor()
    cursor.execute(query, (note, id)) 

    dataConnect.commit()
    dataConnect.close()

def updateFilePriority(id, priority):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE FILE SET 
            PRIORITY = ?
        WHERE ID = ?
    """
    
    cursor = dataConnect.cursor()
    cursor.execute(query, (priority, id)) 

    dataConnect.commit()
    dataConnect.close()

def updateFileReminder(id, date, note):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE FILE SET 
            REMINDER_DATE = ?,
            REMINDER_NOTE = ?
        WHERE ID = ?
    """
    
    cursor = dataConnect.cursor()
    cursor.execute(query, (date, note, id)) 

    dataConnect.commit()
    dataConnect.close()

def updateFileLabel(id, label_id):
    dataConnect = sqlite3.connect("dtb3003.db")
    # if LABEL_ID is None:
    #     LABEL_ID = "NULL"

    query = """
        UPDATE FILE SET 
            LABEL_ID = ?
        WHERE ID = ?
    """
    
    cursor = dataConnect.cursor()
    cursor.execute(query, (label_id, id)) 

    dataConnect.commit()
    dataConnect.close()

def deleteFile(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM FILE WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) # Có dấu ,

    dataConnect.commit()
    dataConnect.close()

def getFileAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM FILE
    """
    cursor = dataConnect.cursor()
    FileList = cursor.execute(query).fetchall()
    
    return FileList

# def getFileName(fileNAME):
#     dataConnect = sqlite3.connect("dtb3003.db")

#     query = """
#         SELECT ID, NAME, TYPE_ID, DATE, DIR FROM FILE WHERE NAME LIKE ?
#     """

#     cursor = dataConnect.cursor()
#     FileList = cursor.execute(query, ('%' + fileNAME + '%',)).fetchall()

#     return FileList