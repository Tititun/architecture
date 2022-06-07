import os
import sqlite3
from abc import ABC, abstractmethod
from typing import Union
import traceback

DB_PATH = os.path.join(os.path.dirname(__file__), 'mydb.db')

def execute(statement: str, params: dict = None) -> (str, bool):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute(statement, params if params else {})
        res = [dict(r) for r in cursor.fetchall()]
        conn.commit()
        return res, True
    except:
        print(traceback.format_exc())
        return traceback.format_exc(), False
    finally:
        cursor.close()
        conn.close()


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

    @abstractmethod
    def update(self):
        pass

    @staticmethod
    @abstractmethod
    def list_all():
        pass


class Category(EducationServise):

    def __init__(self, name):
        if isinstance(name, int):
            self.id = name
            statement = 'SELECT name FROM categories WHERE id = :id'
            params = {'id': name}
            name, _ = execute(statement, params)
            self.name = name[0]['name']
        else:
            self.name = name

    def create(self):
        statement = 'INSERT INTO categories VALUES (NULL, :name)'
        params = {'name': self.name}
        execute(statement, params)

    def delete(self):
        statement = 'DELETE FROM categories WHERE name = :name'
        params = {'name': self.name}
        execute(statement, params)

    def update(self, name):
        statement = 'UPDATE categories SET name = :new_name' \
                    ' WHERE name = :old_name'
        params = {
            'new_name': name,
            'old_name': self.name
        }
        _, success =execute(statement, params)
        return success

    @staticmethod
    def list_all():
        statement = 'SELECT * FROM categories'
        res, success = execute(statement)
        if success:
            return res
        else:
            return f'Something went wrong. Error {res}'


class Course(EducationServise):

    def __init__(self, name: Union[str, int] = '', category_id: int = None,
                 is_online: bool = True, address: str = None,
                 id:int = None):
        if isinstance(name, int):
            self.id = name
            statement = 'SELECT * FROM courses WHERE id = :id'
            params = {'id': name}
            data, _ = execute(statement, params)
            data = data[0]
            self.name = data['name']
            self.category_id = data['category_id']
            self.is_online = data['is_online']
            self.address = data['address']
        else:
            self.name = name
            self.category_id = category_id
            self.is_online = is_online
            self.address = address
            self.id = id

    @classmethod
    def get_course(cls, id_):
        statement = 'SELECT * FROM courses where id = :id'
        params = {'id': id_}
        res, _ = execute(statement, params)
        return Course(**res[0])

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
        statement = 'SELECT id FROM courses WHERE name = :name' \
                    ' and category_id = :category_id'
        id_, _ = execute(statement, params)
        return int(id_[0]['id'])

    def delete(self):
        statement = 'DELETE FROM courses WHERE id = :id'
        params = {'id': self.id}
        execute(statement, params)

    def update(self, **kwargs):
        id_ = kwargs['id']
        del kwargs['id']
        for k, v in kwargs.items():
            statement = f'UPDATE courses SET {k} = :value WHERE id = :id'
            params = {
                'value': v,
                'id': id_
            }
            execute(statement, params)

    @staticmethod
    def list_all():
        statement = 'SELECT * FROM courses'
        res, success = execute(statement)
        if success:
            return res
        else:
            return f'Something went wrong. Error {res}'


if __name__ == '__main__':
    init_db()
    for category in ['правильное питание', 'спорт', 'просвещение']:
        Category(category).create()
    for course in ['подсчет калорий', 'вегетарианство']:
        Course(course, 1).create()
    for course in ['плавание', 'бег', 'ходьба']:
        Course(course, 2).create()
    for course in ['чтение', 'мудрость']:
        Course(course, 3).create()

