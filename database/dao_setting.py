import sqlite3

def createTableSetting():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """CREATE TABLE IF NOT EXITS "SETTING" (
        "ID"	INTEGER,
        "BG_IMG"	TEXT,
        "LG_IMG"	TEXT,
        "DASHBOARD_IMG"	TEXT,
        "ACCENT_COLOR"	TEXT,
        "WIDGET_COLOR"	TEXT,
	    "ID_ICON_COLOR"	TEXT,
        "STATUS"	INTEGER NOT NULL,
        PRIMARY KEY("ID")
    )"""

    cursor = dataConnect.cursor()
    cursor.execute(query)

    dataConnect.close()

# def addSetting(id, bg_img, lg_img, dashboard_img, accent_color, wigets_color, status):
#     dataConnect = sqlite3.connect("dtb3003.db")

#     query = """ INSERT INTO IMAGE (ID, NAME, ACTIVE)
#                 VALUES (?, ?, ?) """

#     cursor = dataConnect.cursor()
#     cursor.execute(query, (id, bg_img, lg_img, dashboard_img, accent_color, wigets_color, 1))
#     #cho này là 1 thì chỉnh mấy cái còn lại là 0

#     dataConnect.commit()
#     dataConnect.close()

def updateSetting(bg_img, accent_color, widget_color, icon_color):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE SETTING SET 
            BG_IMG = ?,
            ACCENT_COLOR = ?,
            WIDGET_COLOR = ?,
            ID_ICON_COLOR = ?,
            STATUS = 1
        WHERE ID = 2
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (bg_img, accent_color, widget_color, icon_color)) 

    dataConnect.commit()
    dataConnect.close()

def updateStatus(id, status):
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        UPDATE SETTING SET 
            STATUS = ?
        WHERE ID = ?
    """

    cursor = dataConnect.cursor()
    cursor.execute(query, (status, id)) 

    dataConnect.commit()
    dataConnect.close()

# def deleteImage(id):
#     dataConnect = sqlite3.connect("dtb3003.db")

#     query = """
#         DELETE FROM IMAGE WHERE ID = ?
#     """

#     cursor = dataConnect.cursor()
#     cursor.execute(query, (id,)) 

#     dataConnect.commit()
#     dataConnect.close()


def getSettingAll():
    dataConnect = sqlite3.connect("dtb3003.db")

    query = """
        SELECT * FROM SETTING
    """
    cursor = dataConnect.cursor()
    SettingList = cursor.execute(query).fetchall()
    
    return SettingList

