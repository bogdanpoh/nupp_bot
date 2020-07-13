import sqlite3
import constants
from database.user import User
from database.lesson import Lesson
import tools

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


def create_table_week():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (id INTEGER PRIMARY KEY, current_week TEXT)
    """.format(constants.table_week))

    db.commit()


def add_user(user):
    query = "INSERT INTO {0} (name_user, group_id, chat_id) VALUES (?, ?, ?)".format(constants.table_users)

    val = (user.name_user, user.group_id, user.chat_id)

    cursor.execute(query, val)
    db.commit()


def get_users():
    query = "SELECT * FROM {0}".format(constants.table_users)

    data = cursor.execute(query)

    users = tools.data_to_list_class(data, "user")

    return users


def get_user_by_chat_id(chat_id):
    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_users, chat_id)

    answer = cursor.execute(query)

    if answer:
        for data in answer:
            return User(data=data)
    else:
        return None


def get_user_group_id(chat_id):
    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_users, chat_id)

    answer = cursor.execute(query)

    if answer:
        for data in answer:
            user = User(data=data)

            return user.group_id
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

    lessons = tools.data_to_list_class(data, "lesson")

    return lessons


def get_group_list():
    query = "SELECT * FROM {0}".format(constants.table_lessons)

    data = cursor.execute(query)

    list = []

    for el in data:
        list.append(Lesson(data=el).group_id)

    return set(list)


def get_lessons_by_day_name(day_name, group_id, week):
    query = "SELECT * FROM {0} WHERE `day_name`='{1}' AND `group_id`='{2}' AND `week`='{3}'".format(constants.table_lessons, day_name, week, group_id)

    data = cursor.execute(query)

    lessons = tools.data_to_list_class(data, "lesson")

    if lessons:
        return lessons
    else:
        return None


def get_lessons_by_week(group_id, week):

    query = "SELECT * FROM {0} WHERE `week`='{1}' AND `group_id`='{2}'".format(constants.table_lessons, week, group_id)

    data = cursor.execute(query)

    lessons = tools.data_to_list_class(data, "lesson")

    return lessons


def get_current_week():

    query = "SELECT * FROM {0}".format(constants.table_week)

    current_week = cursor.execute(query)

    for el in current_week:
        if el:
            return el[-1]


def change_week():

    current_week = get_current_week()

    week = ""

    if current_week == constants.first_week:
        week = constants.second_week
    elif current_week == constants.second_week:
        week = constants.first_week

    query = "UPDATE {0} SET current_week='{1}'".format(constants.table_week, week)

    cursor.execute(query)
    db.commit()

