import psycopg2
import constants
from database.user import User
from database.lesson import Lesson
from database.teacher import Teacher
from database.event import Event
import tools


def get_db_connect():
    return psycopg2.connect(dbname=constants.db_name,
                            user=constants.user,
                            password=constants.password,
                            host=constants.host,
                            port=constants.port)


def get_cursor(db):
    return db.cursor()


def close_connection(cursor, connection):
    cursor.close()
    connection.close()


# create tables
def create_table_users():
    db = get_db_connect()
    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id SERIAL PRIMARY KEY,
    name_user TEXT,
    group_id TEXT,
    chat_id TEXT)
    """.format(constants.table_users))

    db.commit()
    close_connection(cursor, db)


def create_table_teachers():
    db = get_db_connect()
    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id SERIAL PRIMARY KEY,
    name_teacher TEXT,
    chat_id TEXT)
    """.format(constants.table_teachers))

    cursor.close()
    close_connection(cursor, db)


def create_table_lessons():
    db = get_db_connect()
    cursor = get_cursor(db)

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
    close_connection(cursor, db)


def create_table_week():
    db = get_db_connect()
    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (
    id SERIAL PRIMARY KEY,
    current_week TEXT)
    """.format(constants.table_week))

    db.commit()
    close_connection(cursor, db)


def create_table_events():
    db = get_db_connect()
    cursor = get_cursor(db)

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
    close_connection(cursor, db)


# user
def add_user(user):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "INSERT INTO {0} (name_user, group_id, chat_id) VALUES ('{1}', '{2}', '{3}')".format(
        constants.table_users,
        user.name_user,
        user.group_id,
        user.chat_id)

    cursor.execute(query)

    db.commit()
    close_connection(cursor, db)


def get_users():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_users)

    cursor.execute(query)

    data = cursor.fetchall()

    close_connection(cursor, db)

    if data:
        users = tools.data_to_list_class(data, "user")
        return users
    else:
        return None


def get_user_by_chat_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE chat_id = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)

    answer = cursor.fetchall()

    close_connection(cursor, db)

    if answer:
        for data in answer:
            return User(data=data)


def get_user_group_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE chat_id = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)

    answer = cursor.fetchall()

    if answer:
        for data in answer:
            user = User(data=data)

            return user.group_id

    close_connection(cursor, db)


def update_user_group(chat_id, group_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "UPDATE {0} SET group_id = '{1}' WHERE chat_id = '{2}'"\
        .format(constants.table_users, str(group_id), str(chat_id))

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def is_user(chat_id):

    is_registration = False

    users = get_users()

    for user in users:
        if user.chat_id == chat_id:
            is_registration = True

    return is_registration


def remove_users():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_users)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def remove_user_by_chat_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE chat_id = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


# lesson
def add_lesson(lesson):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "INSERT INTO {0} (row, day_name, time_start, time_end, group_id, week, info) VALUES (" \
            "{1}, '{2}', '{3}', '{4}', '{5}', '{6}', \'{7}\')"\
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
    close_connection(cursor, db)


def remove_lessons():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_lessons)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def remove_lessons_by_group_id(group_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE group_id='{1}'".format(constants.table_lessons, group_id)
    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def get_lessons():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_lessons)

    cursor.execute(query)

    data = cursor.fetchall()

    lessons = tools.data_to_list_class(data, "lesson")

    close_connection(cursor, db)

    return lessons


def get_group_list():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_lessons)

    cursor.execute(query)

    data = cursor.fetchall()

    list = []

    close_connection(cursor, db)

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
    db = get_db_connect()
    cursor = get_cursor(db)

    query = str("SELECT * FROM {0} WHERE day_name = '{day_name}' AND week = '{week}' AND group_id = '{group}'")\
        .format(constants.table_lessons,
                day_name=day_name,
                group=group_id,
                week=week)

    cursor.execute(query)

    data = cursor.fetchall()

    close_connection(cursor, db)

    lessons = tools.data_to_list_class(data, "lesson")

    if lessons:
        return lessons
    else:
        return None


def get_lessons_by_week(group_id, week):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE week = '{1}' AND  group_id = '{2}'".format(constants.table_lessons, week, group_id)

    cursor.execute(query)

    data = cursor.fetchall()

    lessons = tools.data_to_list_class(data, "lesson")

    close_connection(cursor, db)

    return lessons


# week
def set_default_week():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "INSERT INTO {0} (current_week) VALUES ('{1}')".format(constants.table_week, constants.first_week)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def get_current_week():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_week)

    cursor.execute(query)

    current_week = cursor.fetchall()

    close_connection(cursor, db)

    for el in current_week:
        if el:
            return el[-1]

    return None


def change_week():
    db = get_db_connect()
    cursor = get_cursor(db)

    current_week = get_current_week()

    week = ""

    if current_week == constants.first_week:
        week = constants.second_week
    elif current_week == constants.second_week:
        week = constants.first_week

    query = "UPDATE {0} SET current_week='{1}'".format(constants.table_week, week)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


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
    db = get_db_connect()
    cursor = get_cursor(db)

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

    close_connection(cursor, db)


def get_event(day_name, week, time):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE send_time = '{1}' AND day_name = '{2}' AND week = '{3}'".format(
        constants.table_events,
        time,
        day_name,
        week)

    cursor.execute(query)

    result = cursor.fetchall()

    close_connection(cursor, db)

    answer = []

    if result:
        for el in result:
            if el:
                answer.append(Event(data=el))

        return answer
    else:
        return None


def is_registration_event(chat_id, week):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE chat_id = '{1}' AND week = '{2}'".format(constants.table_events,
                                                                              chat_id,
                                                                              week)

    cursor.execute(query)

    data = cursor.fetchall()

    close_connection(cursor, db)

    if len(data) > 0:
        return True
    else:
        return False


def get_events():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_events)
    cursor.execute(query)

    data = cursor.fetchall()

    events = tools.data_to_list_class(data, "event")

    close_connection(cursor, db)

    return events


def update_event(event):
    db = get_db_connect()
    cursor = get_cursor(db)

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

    close_connection(cursor, db)


def get_list_time_events():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT send_time FROM {0}".format(constants.table_events)

    cursor.execute(query)

    result = cursor.fetchall()

    list_times = []

    close_connection(cursor, db)

    if result:
        for el in result:
            list_times.append(el[0])

        return list_times
    else:
        return None


def remove_events():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_events)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def remove_event_by_chat_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE chat_id = '{1}'".format(constants.table_events, chat_id)
    cursor.execute(query)

    db.commit()
    close_connection(cursor, db)


def drop_table_events():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DROP TABLE {0}".format(constants.table_events)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)
