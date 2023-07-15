import sqlite3
import random, string
from KCPTapi import GetAllTeachers, GetAllGroups
class Database:
    @staticmethod
    def generate_password(length,seed:int):
        random.seed(seed)
        characters = string.ascii_letters + string.digits
        password = ''.join(random.choice(characters) for _ in range(length))
        return password
    @staticmethod
    def RegUser(ChatId, Group: str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id FROM Groups WHERE GroupName = ?", (Group,))
            result = c.fetchone()
            if result:
                group_id = result[0]
            else:
                return

            # Добавляем нового пользователя в таблицу Users
            c.execute('''
    INSERT INTO Users (id, group_id)
    VALUES (?, ?)
    ON CONFLICT (id) DO UPDATE SET group_id = EXCLUDED.group_id;
''', (ChatId, group_id))
            conn.commit()
    @staticmethod
    def RegPrepod(ChatId:int, Password:str):
        check_password = False
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT EXISTS(SELECT 1 FROM PrepodUsers WHERE Password = ?)", (Password,))
            result = cursor.fetchone()
            check_password = bool(result)
        if(not check_password): return False
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            # Добавляем нового пользователя в таблицу Users
            c.execute('''
             UPDATE PrepodUsers
             SET chatid = ?
             WHERE Password = ?
            ''', (ChatId, Password))
            conn.commit()
        return True

    @staticmethod
    def Execute(query: str, params: dict = None):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute(query, params) if params else conn.execute(query)
            result = cursor.fetchone()
            if result:
                return cursor.fetchall()
            else:
                return result
    @staticmethod
    def RemovePrepodUser(chatid):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("UPDATE PrepodUsers SET chatid = NULL WHERE chatid = ?", (chatid,))
    @staticmethod
    def GetAllGroups():
        with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT GroupName FROM Groups")
            return c.fetchall()
    @staticmethod
    def GetGroupIdByUserId(ChatId):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT Users.group_id FROM Users WHERE Users.id=?", (ChatId,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    @staticmethod
    def getPrepodFioByChatId(ChatId:str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT PrepodUsers.FIO FROM PrepodUsers WHERE chatid = ?", (ChatId,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    @staticmethod
    def getPrepodIdByChatId(ChatId:str):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT PrepodUsers.apiid FROM PrepodUsers WHERE chatid = ?", (ChatId,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    @staticmethod
    def is_user_prepod(user_id):
        with sqlite3.connect('ScheduleBot.db') as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM PrepodUsers WHERE chatid = ?", (user_id,))
            result = cursor.fetchone()
            if(result[0] == 0):
                return False
            else: return True
    @staticmethod
    def is_user_exists(user_id):
        with sqlite3.connect('ScheduleBot.db') as conn:
          c = conn.cursor()
          c.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
          result = c.fetchone()
          return result is not None
    @staticmethod
    def StartDatabase():
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 DROP TABLE IF EXISTS Groups
                ''')

        # with sqlite3.connect('ScheduleBot.db') as conn:
        #     conn.execute('''
        #          DROP TABLE IF EXISTS Users
        #         ''')
        
        #Создание таблицы с группами
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Groups (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   GroupName TEXT NOT NULL
                   )
                ''')
        with sqlite3.connect('ScheduleBot.db') as con:
            cur = con.cursor()
            data = []
            for i in GetAllGroups():
                t = (i["ID"], i["Name"])
                data.append(t)

            cur.executemany('INSERT INTO Groups(Id,GroupName) VALUES (?, ?)', data)
            con.commit()
        
        #Создание таблицы пользователей с привилегиями преподавателей
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS PrepodUsers (
                         apiid INTEGER PRIMARY KEY NOT NULL,
                         Password TEXT NOT NULL,
                         chatid INTEGER,
                         FIO TEXT NOT NULL
                         )''')
        with sqlite3.connect('ScheduleBot.db') as con:
            cur = con.cursor()
            data = []
            for i in GetAllTeachers():
                if len(i["SecondName"]) < 2 :
                    continue
                else:
                    t = (i["ID"], i["Surname"]+" "+i['FirstName']+" "+i['SecondName'], Database.generate_password(8,i["ID"]))
                    data.append(t)

            cur.executemany('INSERT INTO PrepodUsers(apiid,FIO,Password) VALUES (?, ?, ?)', data)
            con.commit()
        #Создание таблицы с пользователями
        with sqlite3.connect('ScheduleBot.db') as conn:
            conn.execute('''
                 CREATE TABLE IF NOT EXISTS Users (
                   id INTEGER PRIMARY KEY,
                   group_id INTEGER NOT NULL,
                   FOREIGN KEY (group_id) REFERENCES Groups(id)
                   )
                ''')
'''Database.StartDatabase()
with sqlite3.connect('ScheduleBot.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM Users")
            print(c.fetchall())'''