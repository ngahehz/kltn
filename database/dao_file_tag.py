import sqlite3

def createTableFileTag():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "FILE_TAG" (
        "ID"	INTEGER NOT NULL,
        "FILE_ID"	INTEGER NOT NULL,
        "TAG_ID"	INTEGER NOT NULL,
        PRIMARY KEY("ID"),
        FOREIGN KEY("TAG_ID") REFERENCES "TAG"("ID"),
        FOREIGN KEY("FILE_ID") REFERENCES "FILE_TAG"("FILE_ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addFileTag(id, file_id, tag_id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        INSERT INTO FILE_TAG (ID, FILE_ID, TAG_ID) VALUES (?, ?)
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, file_id, tag_id))

    dataConnect.commit()
    dataConnect.close()


def deleteFileTag(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM FILE_TAG WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) 

    dataConnect.commit()
    dataConnect.close()

def getFileTagAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM FILE_TAG
    """

    cursor = dataConnect.cursor()
    FileTagList = cursor.execute(query).fetchall()

    return FileTagList
