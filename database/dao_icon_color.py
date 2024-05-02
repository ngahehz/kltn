import sqlite3

def createIconColor():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "ICON_COLOR" (
        "ID"	INTEGER NOT NULL,
        "COLOR"	TEXT,
        "NAME"	TEXT,
        PRIMARY KEY("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addIconColor(id, color, name):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """ INSERT INTO ICON_COLOR (ID, COLOR, NAME)
                VALUES (?, ?, ?) """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, color, name))

    dataConnect.commit()
    dataConnect.close()

def updateIconColor(id, color, name):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE ICON_COLOR SET 
            COLOR = ?,
            NAME = ?
        WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (color, name, id)) 

    dataConnect.commit()
    dataConnect.close()


def deleteIconColor(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM ICON_COLOR WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) 

    dataConnect.commit()
    dataConnect.close()


def getIconColorAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM ICON_COLOR
    """
    cursor = dataConnect.cursor()
    ImageList = cursor.execute(query).fetchall()
    
    return ImageList

