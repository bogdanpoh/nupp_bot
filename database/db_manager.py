import psycopg2
import constants
from database.user import User
from database.lesson import Lesson
from database.teacher import Teacher
from database.event import Event
import tools


db = psycopg2.connect(dbname=constants.db_name,
                      user=constants.user,
                      password=constants.password,
                      host=constants.host,
                      port=constants.port)
cursor = db.cursor()


# create tables
def create_table_users():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id SERIAL PRIMARY KEY,
    name_user TEXT,
    group_id TEXT,
    chat_id TEXT)
    """.format(constants.table_users))

    db.commit()


def create_table_teachers():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id SERIAL PRIMARY KEY,
    name_teacher TEXT,
    chat_id TEXT)
    """.format(constants.table_teachers))

    db.commit()


def create_table_lessons():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (id SERIAL PRIMARY KEY,
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
    CREATE TABLE IF NOT EXISTS {0} (
    id SERIAL PRIMARY KEY,
    current_week TEXT)
    """.format(constants.table_week))

    db.commit()


def create_table_events():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (
    id SERIAL PRIMARY KEY,
    group_id TEXT,
    day_name TEXT,
    week TEXT,
    chat_id TEXT,
    send_time TEXT,
    is_send BOOLEAN)
    """.format(constants.table_events))

    db.commit()


# user
def add_user(user):
    query = "INSERT INTO {0} (name_user, group_id, chat_id) VALUES ('{1}', '{2}', '{3}')".format(
        constants.table_users,
        user.name_user,
        user.group_id,
        user.chat_id)

    cursor.execute(query)
    db.commit()


def get_users():
    query = "SELECT * FROM {0}".format(constants.table_users)

    cursor.execute(query)

    data = cursor.fetchall()

    if data:
        users = tools.data_to_list_class(data, "user")

        return users

    else:
        return None


def get_user_by_chat_id(chat_id):
    query = "SELECT * FROM {0} WHERE chat_id = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)

    answer = cursor.fetchall()

    if answer:
        for data in answer:
            return User(data=data)


def get_user_group_id(chat_id):
    query = "SELECT * FROM {0} WHERE chat_id = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)

    answer = cursor.fetchall()

    if answer:
        for data in answer:
            user = User(data=data)

            return user.group_id


def update_user_group(chat_id, group_id):
    query = "UPDATE {0} SET group_id = '{1}' WHERE chat_id = '{2}'"\
        .format(constants.table_users, str(group_id), str(chat_id))

    cursor.execute(query)
    db.commit()


def is_user(chat_id):

    is_registration = False

    users = get_users()

    for user in users:
        if user.chat_id == chat_id:
            is_registration = True

    return is_registration


def remove_users():
    query = "DELETE FROM {0}".format(constants.table_users)

    cursor.execute(query)
    db.commit()


def remove_user_by_chat_id(chat_id):
    query = "DELETE FROM {0} WHERE chat_id = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)
    db.commit()


# lesson
def add_lesson(lesson):
    query = "INSERT INTO {0} (row, day_name, time_start, time_end, group_id, week, info) VALUES (" \
            "{1}, '{2}', {3}, {4}, '{5}', '{6}', \'{7}\')"\
        .format(constants.table_lessons,
                lesson.row,
                lesson.day_name,
                lesson.time_start,
                lesson.time_end,
                lesson.group_id,
                lesson.week,
                str(lesson.info).replace("'", "`"))

    cursor.execute(query)
    db.commit()


def remove_lessons():
    query = "DELETE FROM {0}".format(constants.table_lessons)

    cursor.execute(query)
    db.commit()


def remove_lessons_by_group_id(group_id):
    query = "DELETE FROM {0} WHERE group_id='{1}'".format(constants.table_lessons, group_id)
    cursor.execute(query)
    db.commit()


def get_lessons():
    query = "SELECT * FROM {0}".format(constants.table_lessons)

    data = cursor.execute(query)

    lessons = tools.data_to_list_class(data, "lesson")

    return lessons


def get_group_list():
    query = "SELECT * FROM {0}".format(constants.table_lessons)

    cursor.execute(query)

    data = cursor.fetchall()

    list = []

    if data:
        for el in data:
            list.append(Lesson(data=el).group_id)

        return set(list)


def is_group(group_id):
    groups = get_group_list()

    if groups:
        for group in groups:
            if group == group_id:
                return True

    return False


def get_lessons_by_day_name(day_name, week, group_id):
    query = str("SELECT * FROM {0} WHERE day_name = '{day_name}' AND week = '{week}' AND group_id = '{group}'")\
        .format(constants.table_lessons,
                day_name=day_name,
                group=group_id,
                week=week)

    cursor.execute(query)

    data = cursor.fetchall()

    lessons = tools.data_to_list_class(data, "lesson")

    if lessons:
        return lessons
    else:
        return None


def get_lessons_by_week(group_id, week):

    query = "SELECT * FROM {0} WHERE week = '{1}' AND  group_id = '{2}'".format(constants.table_lessons, week, group_id)

    cursor.execute(query)

    data = cursor.fetchall()

    lessons = tools.data_to_list_class(data, "lesson")

    return lessons


# week
def set_default_week():
    query = "INSERT INTO {0} (current_week) VALUES ('{1}')".format(constants.table_week, constants.first_week)

    cursor.execute(query)
    db.commit()


def get_current_week():

    query = "SELECT * FROM {0}".format(constants.table_week)

    cursor.execute(query)

    current_week = cursor.fetchall()

    for el in current_week:
        if el:
            return el[-1]

    return None


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


# teacher
def add_teacher(teacher):
    pass
    # query = "INSERT INTO {0} (name_teacher, chat_id) VALUES (?, ?)".format(constants.table_teachers)
    #
    # val = (teacher.name_teacher, teacher.chat_id)
    #
    # cursor.execute(query, val)
    # db.commit()


def remove_teachers():
    pass
    # query = "DELETE FROM {0}".format(constants.table_teachers)
    #
    # cursor.execute(query)
    # db.commit()


def get_teachers():
    pass
    # query = "SELECT * FROM {0}".format(constants.table_teachers)
    #
    # list = []
    #
    # result = cursor.execute(query)
    #
    # if result:
    #     for el in result:
    #         list.append(Teacher(data=el))
    #
    #     return list
    #
    # else:
    #     return None


def get_teacher_by_chat_id(chat_id):
    # query = "SELECT * FROM {0} WHERE chat_id = '{1}'".format(constants.table_teachers, chat_id)
    #
    # answer = cursor.execute(query)
    #
    # if answer:
    #     for data in answer:
    #         return Teacher(data=data)
    # else:
    #     return None

    pass


def get_teacher_lessons(day_name, week):
    pass


# event
def add_event(event):
    query = "INSERT INTO {0} (group_id, day_name, week, chat_id, send_time, is_send) " \
            "VALUES ('{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(constants.table_events,
                                                                       event.group_id,
                                                                       event.day_name,
                                                                       event.week,
                                                                       event.chat_id,
                                                                       str(event.send_time).replace(".", ":"),
                                                                       event.is_send)

    cursor.execute(query)
    db.commit()


def get_event(day_name, week, time):
    query = "SELECT * FROM {0} WHERE send_time = '{1}' AND day_name = '{2}' AND week = '{3}'".format(
        constants.table_events,
        time,
        day_name,
        week)

    cursor.execute(query)

    result = cursor.fetchall()

    if result:
        for el in result:
            if el:
                return Event(data=el)
    else:
        return None


def get_events():
    query = "SELECT * FROM {0}".format(constants.table_events)
    cursor.execute(query)

    data = cursor.fetchall()

    events = tools.data_to_list_class(data, "event")

    return events


def update_event(event):
    # "UPDATE {0} SET group_id = '{1}' WHERE chat_id = '{2}'"
    query = "UPDATE {0} SET day_name = '{1}', send_time = '{2}', week = '{3}', is_send = '{4}' WHERE id = '{5}'".format(
        constants.table_events,
        event.day_name,
        event.send_time,
        event.week,
        event.is_send,
        event.id)
    cursor.execute(query)
    db.commit()


def get_list_time_events():
    query = "SELECT send_time FROM {0}".format(constants.table_events)

    cursor.execute(query)

    result = cursor.fetchall()

    list_times = []

    if result:
        for el in result:
            list_times.append(el[0])

        return list_times
    else:
        return None


def remove_events():
    query = "DELETE FROM {0}".format(constants.table_events)

    cursor.execute(query)
    db.commit()


def drop_table_events():
    query = "DROP TABLE {0}".format(constants.table_events)

    cursor.execute(query)
    db.commit()
