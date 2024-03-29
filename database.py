import sqlite3
from datetime import datetime
from crypting import CryptingAlgorithm

def Test():
    print('test')
class DataBase():
    __slots__ = ('__db',)
    def __init__(self,db):
        self.__db = f'{db}'
        print(self.__db)
    def __str__(self):
        return f'{self.__db}'
    def exanple(self):
        return True
    def check_email(self,email):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT count(email) AS TOTAL FROM users WHERE email="{email}"')
            result = cur.fetchone()[0]
        if result == 0: return True
        return False
    def register_user(self,email,psw):
        if self.check_email(email):
            with sqlite3.connect(self.__db) as conn:
                cur = conn.cursor()
                cur.execute('INSERT INTO users (email,psw,date) VALUES (?,?,?);',(email,CryptingAlgorithm(psw).encoding(),datetime.today().date()))
            return True
        return False
    def login_user(self,email,psw):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM users WHERE email="{email}"')
            result = cur.fetchone()
        try:
            if result[2] == CryptingAlgorithm(psw):
                return True
        except Exception as e:
            return False
    def get_id(self,email):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT id FROM users WHERE email="{email}"')
            result = str(cur.fetchone()[0])
        print(result)
        return result
    def exist_id(self,id):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT count(id) AS TOTAL FROM users WHERE id="{id}"')
            result = cur.fetchone()[0]
        if result == 0: return False
        return True
    def get_notes(self):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT notes.id,notes.note,notes.date,users.email,notes.noteid FROM users JOIN notes ON users.id = notes.id')
            result = cur.fetchall()
        return result
    def insert_notes(self,email,note):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'INSERT INTO notes (id,note,date) SELECT users.id,"{note}","{datetime.today().date()}" FROM users WHERE users.email="{email}";')
        return True
    def get_notes_by_email(self,email):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT notes.*,users.email FROM users JOIN notes ON users.id = notes.id WHERE users.email="{email}"')
            result = cur.fetchall()
        if len(result) >0:
            return result
        return "no"

    def get_all_notes(self):
        with sqlite3.connect(self.__db) as conn:
            cur = conn.cursor()
            cur.execute(
                f'SELECT notes.*,users.email FROM users JOIN notes ON users.id = notes.id')
            result = cur.fetchall()
        if len(result) > 0:
            return result
        return "no"
        # return False ['None1','There are no notes','None1','None1']
    def get_email_by_noteid(self,noteid):
        try:
            with sqlite3.connect(self.__db) as conn:
                cur = conn.cursor()
                cur.execute(f'SELECT users.email FROM users JOIN notes ON users.id = notes.id WHERE Noteid={noteid}')
                result = cur.fetchone()[0]
            return result
        except Exception:
            return None
    def update_note(self,noteid,new_note):
        try:
            with sqlite3.connect(self.__db) as conn:
                cur = conn.cursor()
                cur.execute(f"UPDATE notes SET note='{new_note}' WHERE Noteid={noteid}")
            return True
        except Exception:
            return False
    def delete_by_noteid(self,noteid):
        try:
            with sqlite3.connect(self.__db) as conn:
                cur = conn.cursor()
                cur.execute(f"Delete from notes WHERE Noteid={noteid}")
            return True
        except Exception:
            return False
# db = DataBase('db.db')
# print(db.get_email_by_noteid('4'))
# print(db.check_email("admin@admin"))
# print(db.register_user("lox@lox1","1234"))
# print(db.login_user("lox@lox1","1234"))