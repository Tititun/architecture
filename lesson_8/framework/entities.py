import threading
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


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Category):
            return CategoryMapper()


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.create_new()
        self.update_dirty()
        self.delete_removed()

    def create_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).create(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Category(DomainObject):

    def __init__(self, name, id):
        self.name = name
        self.id = id


class CategoryMapper:

    def create(self, name):
        statement = 'INSERT INTO categories VALUES (NULL, :name)'
        params = {'name': name}
        execute(statement, params)
        res, _ = execute('SELECT name, id FROM categories where name=:name',
                         params)
        return Category(res[0]['name'], res[0]['id'], params)

    @staticmethod
    def delete(category):
        statement = 'DELETE FROM categories WHERE name = :name'
        params = {'name': category.name}
        execute(statement, params)

    @staticmethod
    def update(category):
        statement = 'UPDATE categories SET name = :new_name' \
                    ' WHERE id = :id'
        params = {
            'new_name': category.name,
            'id': category.id
        }
        _, success = execute(statement, params)
        return success

    @staticmethod
    def fetch_by_id(id_):
        statement = "SELECT name FROM categories where id=:id"
        params = {'id': id_}
        res, _ = execute(statement, params)
        if res:
            return Category(res[0]['name'], id_)


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
        name, category_id = kwargs.get('name'), kwargs.get('category_id')
        if name and category_id:
            statements = f'SELECT * FROM courses WHERE' \
                         f' category_id = :category_id AND name = :name'
            params = {
                'category_id': category_id,
                'name': name
            }
            res, _ = execute(statements, params)
            if res:
                return
        for k, v in kwargs.items():
            statement = f'UPDATE courses SET {k} = :value WHERE id = :id'
            params = {
                'value': v,
                'id': id_
            }
            execute(statement, params)
        return True

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
    for category in ['правильное питание', 'спорт', 'просвещение']:
        CategoryMapper.create(category)
    for course in ['подсчет калорий', 'вегетарианство']:
        Course(course, 1).create()
    for course in ['плавание', 'бег', 'ходьба']:
        Course(course, 2).create()
    for course in ['чтение', 'мудрость']:
        Course(course, 3).create()
