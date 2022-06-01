import os
import sqlite3
from abc import ABC, abstractmethod
import traceback

DB_PATH = os.path.join(os.path.dirname(__file__), 'mydb.db')

def execute(statement: str, params: dict = None) -> (str, bool):
    con = sqlite3.connect(DB_PATH)
    cursor = con.cursor()
    try:
        cursor.execute(statement, params if params else {})
        res = cursor.fetchall()
        con.commit()
        return res, True
    except:
        print(traceback.format_exc())
        return traceback.format_exc(), False
    finally:
        cursor.close()
        con.close()


def init_db():
    execute('CREATE TABLE IF NOT EXISTS categories'
            '(id INTEGER PRIMARY KEY,'
            'name VARCHAR NOT NULL,'
            'UNIQUE (name));')
    execute('CREATE TABLE IF NOT EXISTS courses'
            '(id INTEGER PRIMARY KEY,'
            'name VARCHAR NOT NULL,'
            'is_online BOOLEAN NOT NULL,'
            'address VARCHAR,'
            'category_id INTEGER NOT NULL,'
            'UNIQUE (name, category_id),'
            'FOREIGN KEY (category_id) REFERENCES categories(id)'
            ' ON DELETE CASCADE);')

class EducationServise(ABC):

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @staticmethod
    @abstractmethod
    def list_all():
        pass


class Category(EducationServise):

    def __init__(self, name):
        self.name = name

    def create(self):
        statement = 'INSERT INTO categories VALUES (NULL, :name)'
        params = {'name': self.name}
        execute(statement, params)

    def delete(self):
        statement = 'DELETE FROM categories WHERE name = :name'
        params = {'name': self.name}
        execute(statement, params)

    @staticmethod
    def list_all():
        statement = 'SELECT name FROM categories'
        res, success = execute(statement)
        if success:
            return [{'name': r[0]} for r in res]
        else:
            return f'Something went wrong. Error {res}'


class Course(EducationServise):

    def __init__(self, name: str, category_id: int, is_online: bool = True,
                 address: str = None):
        self.name = name
        self.category_id = category_id
        self.is_online = is_online
        self.address = address

    def create(self):
        statement = 'INSERT INTO courses VALUES (NULL, :name, :is_online, '\
                    ':address, :category_id)'
        params = {
                'name': self.name,
                'is_online': int(self.is_online),
                'address': self.address,
                'category_id': self.category_id
                }
        execute(statement, params)

    def delete(self):
        statement = 'DELETE FROM courses WHERE name = :name and' \
                    ' category_id = :category_id'
        params = {
                'name': self.name,
                'category_id': self.category_id
            }
        execute(statement, params)

    @staticmethod
    def list_all():
        statement = 'SELECT * FROM courses'
        res, success = execute(statement)
        if success:
            return [name[0] for name in res]
        else:
            return f'Something went wrong. Error {res}'


if __name__ == '__main__':
    init_db()
    # for category in ['правильное питание', 'спорт', 'просвещение']:
    #     Category(category).create()

    for course in ['плавание', 'бег', 'ходьба']:
        Course(course, 2).create()