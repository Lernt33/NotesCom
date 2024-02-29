import sqlite3
class DataBase():
    __slots__ = ('__db',)
    def __init__(self,db):
        __db = f'databases/{db}'
    # def user_count(self):
    #     with sqlite3.connect(self.__db) as conn:
    #         cur = conn.cursor()
    #