import os
import sqlite3
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
    execute(init_categories)
    execute(init_courses)
    execute(init_users)
    execute(init_users_courses)


init_categories = """CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY, name VARCHAR NOT NULL,
                     UNIQUE (name));"""

init_courses = 'CREATE TABLE IF NOT EXISTS courses (id INTEGER PRIMARY KEY,' \
              ' name VARCHAR NOT NULL, is_online BOOLEAN NOT NULL,' \
              ' address VARCHAR, category_id INTEGER NOT NULL, \
               UNIQUE (name, category_id), FOREIGN KEY (category_id)' \
              ' REFERENCES categories(id) ON DELETE CASCADE);'\

init_users = """CREATE TABLE IF NOT EXISTS users (
                id integer PRIMARY KEY,
                name VARCHAR NOT NULL,
                UNIQUE(name)
            );"""

init_users_courses = """CREATE TABLE IF NOT EXISTS users_courses (
                        id integer PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        course_id INTEGER NOT NULL,
                        UNIQUE(user_id, course_id),
                        FOREIGN KEY (user_id) REFERENCES users(id)
                         ON DELETE CASCADE,
                        FOREIGN KEY (course_id) REFERENCES courses(id) 
                        ON DELETE CASCADE
                    );"""
