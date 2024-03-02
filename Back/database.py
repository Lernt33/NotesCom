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

db = DataBase('db.db')
# print(db.check_email("admin@admin"))
# print(db.register_user("lox@lox1","1234"))
print(db.login_user("lox@lox1","1234"))