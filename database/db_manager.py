import sqlite3
import constants
from database.user import User

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

    user = cursor.execute(query)

    return User(data=user[0])


def remove_users():
    query = "DELETE FROM {0}".format(constants.table_users)

    cursor.execute(query)
    db.commit()
