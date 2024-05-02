import sqlite3

def createTableLabel():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "LABEL" (
        "ID"	INTEGER NOT NULL,
        "NAME"	TEXT NOT NULL,
        PRIMARY KEY("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addLabel(id, name):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        INSERT INTO LABEL (ID, NAME) VALUES (?, ?)
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, name))

    dataConnect.commit()
    dataConnect.close()

def updateLabel(id, name):
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

def deleteLabel(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM LABEL WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) 

    dataConnect.commit()
    dataConnect.close()

def getLabelAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM LABEL
    """

    cursor = dataConnect.cursor()
    LabelList = cursor.execute(query).fetchall()

    return LabelList
