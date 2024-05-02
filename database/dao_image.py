import sqlite3

def createTableImage():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "IMAGE" (
        "ID"	INTEGER NOT NULL,
        "NAME"	INTEGER NOT NULL,
        "ACTIVE"	INTEGER NOT NULL,
        PRIMARY KEY("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

def addImage(id, name, active):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """ INSERT INTO IMAGE (ID, NAME, ACTIVE)
                VALUES (?, ?, ?) """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id, name, active))

    dataConnect.commit()
    dataConnect.close()

# cơ chế ở đây là active cho 012 là kiểu hiển thị
# nếu mà không hiển thị thì để 3
def updateImage(id, active):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE IMAGE SET 
            ACTIVE = ?
        WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (active, id)) 

    dataConnect.commit()
    dataConnect.close()


def deleteImage(id):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        DELETE FROM IMAGE WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (id,)) 

    dataConnect.commit()
    dataConnect.close()


def getImageAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM IMAGE
    """
    cursor = dataConnect.cursor()
    ImageList = cursor.execute(query).fetchall()
    
    return ImageList

