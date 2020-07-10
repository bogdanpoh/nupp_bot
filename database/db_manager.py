import sqlite3
import constants
from database.user import User
from database.lesson import Lesson

db = sqlite3.connect('db_bot.db', check_same_thread=False)

cursor = db.cursor()


def create_table_users():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id INTEGER PRIMARY KEY,
    name_user TEXT,
    group_id TEXT,
    chat_id TEXT)
    """.format(constants.table_users))

    db.commit()


def create_table_lessons():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY,
    row TEXT,
    day_name TEXT,
    time_start TEXT,
    time_end TEXT,
    group_id TEXT,
    week TEXT,
    info TEXT)
    """.format(constants.table_lessons))

    db.commit()


def add_user(user):
    query = "INSERT INTO {0} (name_user, group_id, chat_id) VALUES (?, ?, ?)".format(constants.table_users)

    val = (user.name_user, user.group_id, user.chat_id)

    cursor.execute(query, val)
    db.commit()


def get_users():
    query = "SELECT * FROM {0}".format(constants.table_users)

    data = cursor.execute(query)

    list_users = []

    for el in data:
        list_users.append(User(data=el))

    return list_users


def get_user_by_chat_id(chat_id):
    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_users, chat_id)

    answer = cursor.execute(query)

    if answer:
        for property in answer:
            return User(data=property)
    else:
        return None


def remove_users():
    query = "DELETE FROM {0}".format(constants.table_users)

    cursor.execute(query)
    db.commit()


def add_lesson(lesson):
    query = "INSERT INTO {0} (row, day_name, time_start, time_end, group_id, week, info) VALUES (?, ?, ?, ?, ?, ?, ?)".format(constants.table_lessons)

    val = (lesson.row, lesson.day_name, lesson.time_start, lesson.time_end, lesson.group_id, lesson.week, lesson.info)

    cursor.execute(query, val)
    db.commit()


def remove_lessons():
    query = "DELETE FROM {0}".format(constants.table_lessons)

    cursor.execute(query)
    db.commit()


def get_lessons():
    query = "SELECT * FROM {0}".format(constants.table_lessons)

    data = cursor.execute(query)

    list_lessons = []

    for el in data:
        list_lessons.append(Lesson(data=el))

    return list_lessons
