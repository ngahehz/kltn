import sqlite3

def createTableTag():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "TAG" (
        "ID"	INTEGER NOT NULL,
        "NAME"	TEXT NOT NULL,
        PRIMARY KEY("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addTag(id, name):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        INSERT INTO TAG (ID, NAME) VALUES (?, ?)
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, name))

    dataConnect.commit()
    dataConnect.close()

def updateTag(id, name):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE TYPE SET 
            NAME = ?, 
        WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (name, id))

    dataConnect.commit()
    dataConnect.close()

def deleteTag(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM TAG WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) 

    dataConnect.commit()
    dataConnect.close()

def getTagAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM TAG
    """

    cursor = dataConnect.cursor()
    TagList = cursor.execute(query).fetchall()

    return TagList
