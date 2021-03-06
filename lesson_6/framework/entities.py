import datetime
from abc import ABC, abstractmethod
from typing import Union
from .sql import execute, init_db


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


class Student:
    def __init__(self, name: str, id=None):
        self.name = name
        self.id = id if id else self.fetch_id()

    def fetch_id(self):
        res, success = execute('SELECT id FROM users WHERE name = :name',
                                params={'name': self.name})
        return res[0]['id'] if res else None

    def create(self):
        statement = 'INSERT INTO users VALUES (NULL, :name)'
        params = {'name': self.name}
        execute(statement, params)
        self.id = self.fetch_id()
        return self

    @staticmethod
    def fetch_user_by_id(id_):
        res, _ = execute('SELECT * FROM users WHERE id = :id',
                                params={'id': id_})
        return Student(name=res[0]['name'], id=res[0]['id'])

    @staticmethod
    def fetch_user_by_name(name):
        res, _ = execute('SELECT * FROM users WHERE name = :name',
                         params={'name': name})
        if not res:
            return
        else:
            return Student(name)

    @staticmethod
    def list_all():
        statement = 'SELECT * FROM users'
        return execute(statement)[0]


if __name__ == '__main__':
    init_db()
    for category in ['???????????????????? ??????????????', '??????????', '??????????????????????']:
        Category(category).create()
    for course in ['?????????????? ??????????????', '????????????????????????????']:
        Course(course, 1).create()
    for course in ['????????????????', '??????', '????????????']:
        Course(course, 2).create()
    for course in ['????????????', '????????????????']:
        Course(course, 3).create()
