import sqlite3
import constants
from database.user import User
from database.lesson import Lesson
from database.teacher import Teacher
from database.event import Event
import tools


def get_db_connect(name_db=None):

    if name_db:
        return sqlite3.connect(name_db, check_same_thread=False)
    else:
        return sqlite3.connect(constants.db_name, check_same_thread=False)


def get_cursor(db):
    return db.cursor()


def close_connection(cursor, connection):
    cursor.close()
    connection.close()


# create tables
def create_table_users(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id INTEGER PRIMARY KEY,
    name_user TEXT,
    group_id TEXT,
    chat_id TEXT,
    language TEXT)
    """.format(constants.table_users))

    db.commit()
    close_connection(cursor, db)


def create_table_teachers(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0}
    (id INTEGER PRIMARY KEY,
    name_teacher TEXT,
    chat_id TEXT)
    """.format(constants.table_teachers))

    db.commit()
    close_connection(cursor, db)


def create_table_lessons(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

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
    close_connection(cursor, db)


def create_table_week(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (
    id INTEGER PRIMARY KEY,
    current_week TEXT)
    """.format(constants.table_week))

    db.commit()
    close_connection(cursor, db)


def create_table_events(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (
    id INTEGER PRIMARY KEY,
    group_id TEXT,
    day_name TEXT,
    week TEXT,
    chat_id TEXT,
    send_time TEXT,
    is_send BOOLEAN)
    """.format(constants.table_events))

    db.commit()
    close_connection(cursor, db)


def create_table_faculty(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (
    id INTEGER PRIMARY KEY,
    faculty TEXT,
    group_id TEXT)
    """.format(constants.table_faculty))

    db.commit()
    close_connection(cursor, db)


def create_table_session(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS {0} (
    id INTEGER PRIMARY KEY,
    group_id TEXT,
    date TEXT,
    time TEXT,
    type TEXT,
    name TEXT,
    teacher_name TEXT,
    audience TEXT)
    """.format(constants.table_session))

    db.commit()
    close_connection(cursor, db)

# session
def add_session(session, db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "INSERT INTO {0} (group_id, date, time, type, name, teacher_name, audience) VALUES (?, ?, ?, ?, ?, ?, ?)".format(constants.table_session)

    val = (session.group_id, session.date, session.time, session.type, session.name, session.teacher_name, session.audience)

    cursor.execute(query, val)

    db.commit()
    close_connection(cursor, db)

def get_sessions(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_session)

    data = cursor.execute(query)

    if data:
        session_list = tools.data_to_list_class(data, to_class="session")
        close_connection(cursor, db)
        return session_list
    else:
        close_connection(cursor, db)
        return None

def get_session_list_by_group_id(group_id, db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "SELECT * FROM {0}  WHERE `group_id` = '{1}'".format(constants.table_session, group_id)

    data = cursor.execute(query)

    if data:
        session_list = tools.data_to_list_class(data, to_class="session")
        close_connection(cursor, db)
        return session_list
    else:
        close_connection(cursor, db)
        return None

def is_group_on_session(group_id, db_name=None):
    sessions = get_sessions(db_name)

    if sessions:
        for session in sessions:
            if str(session.group_id) == str(group_id):
                return True

    return False

def remove_session_by_group_id(group_id, db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE `group_id` = '{1}'".format(constants.table_session, group_id)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)

def drop_session(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "DELETE FROM {0} ".format(constants.table_session)

    cursor.execute(query)

    db.commit()
    close_connection(cursor, db)

# user
def add_user(user, db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "INSERT INTO {0} (name_user, group_id, chat_id, language) VALUES (?, ?, ?, ?)".format(constants.table_users)

    val = (user.name_user, user.group_id, user.chat_id, user.language)

    cursor.execute(query, val)

    db.commit()
    close_connection(cursor, db)


def get_users(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_users)

    data = cursor.execute(query)

    if data:
        users = tools.data_to_list_class(data, "user")
        close_connection(cursor, db)
        return users
    else:
        close_connection(cursor, db)
        return None


def get_user_by_chat_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)
    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_users, chat_id)

    user = cursor.execute(query)

    if user:
        for info in user:
            close_connection(cursor, db)
            return User(data=info)


def get_user_group_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_users, chat_id)

    user = cursor.execute(query)

    if user:
        for data in user:
            close_connection(cursor, db)
            return User(data=data).group_id


def update_user_group(chat_id, group_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "UPDATE {0} SET `group_id` = '{1}' WHERE `chat_id` = '{2}'"\
        .format(constants.table_users, str(group_id), str(chat_id))

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def update_user_lang(chat_id, lang):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "UPDATE {0} SET `language` = '{1}' WHERE `chat_id` = '{2}'".format(constants.table_users, str(lang), str(chat_id))

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def is_user(chat_id):

    is_registration = False

    users = get_users()

    for user in users:
        if str(user.chat_id) == str(chat_id):
            is_registration = True

    return is_registration


def remove_users(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_users)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def remove_user_by_chat_id(chat_id, db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_users, chat_id)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


# lesson
def add_lesson(lesson, db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "INSERT INTO {0} (row, day_name, time_start, time_end, group_id, week, info) VALUES (" \
            "?, ?, ?, ?, ?, ?, ?)".format(constants.table_lessons)

    val = (lesson.row,
           lesson.day_name,
           lesson.time_start,
           lesson.time_end,
           lesson.group_id,
           lesson.week,
           str(lesson.info).replace("'", "`"))

    cursor.execute(query, val)
    db.commit()
    close_connection(cursor, db)


def remove_lessons(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_lessons)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def remove_lessons_by_group_id(group_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE `group_id` = '{1}'".format(constants.table_lessons, group_id)
    cursor.execute(query)

    db.commit()
    close_connection(cursor, db)


def get_lessons(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_lessons)

    data = cursor.execute(query)

    lessons = tools.data_to_list_class(data, "lesson")

    close_connection(cursor, db)

    return lessons


def get_group_list(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_lessons)

    data = cursor.execute(query)

    list = []

    if data:
        for el in data:
            list.append(Lesson(data=el).group_id)

        close_connection(cursor, db)
        return set(list)

    close_connection(cursor, db)


def is_group(group_id, db_name=None):
    groups = get_group_list(db_name)

    if groups:
        for group in groups:
            if str(group) == str(group_id):
                return True

    return False


def remove_group(group_id, db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE `group_id` = '{1}'".format(constants.table_lessons, group_id)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def get_lessons_by_day_name(day_name, week, group_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = str("SELECT * FROM {0} WHERE `day_name` = '{day_name}' AND `week` = '{week}' AND `group_id` = '{group}'")\
        .format(constants.table_lessons,
                day_name=day_name,
                group=group_id,
                week=week)

    data = cursor.execute(query)

    lessons = tools.data_to_list_class(data, "lesson")

    if lessons:
        close_connection(cursor, db)
        return lessons
    else:
        close_connection(cursor, db)
        return None


def get_lessons_by_week(group_id, week):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE `week` = '{1}' AND  `group_id` = '{2}'".format(constants.table_lessons, week, group_id)

    data = cursor.execute(query)

    lessons = tools.data_to_list_class(data, "lesson")

    close_connection(cursor, db)

    return lessons


def rename_group_id(group_id, new_group_id, db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "UPDATE {0} SET `group_id` = '{1}' WHERE `group_id` = '{2}'" \
        .format(constants.table_lessons, str(new_group_id), str(group_id))

    db.execute(query)
    db.commit()
    close_connection(cursor, db)


# week
def set_default_week(db_name=None, week=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    set_week = constants.first_week

    if week:
        set_week = week

    query = "INSERT INTO {0} (current_week) VALUES ('{1}')".format(constants.table_week, set_week)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def get_current_week(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_week)

    try:
        current_week = cursor.execute(query)

        for el in current_week:
            if el:
                close_connection(cursor, db)
                return el[-1]
    except sqlite3.Error as error:
        str_error = str(error)
        print(str_error)
        return str_error

    close_connection(cursor, db)
    return None


def change_week(db_name=None):

    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    current_week = get_current_week(db_name)

    week = ""

    if current_week == constants.first_week:
        week = constants.second_week
    elif current_week == constants.second_week:
        week = constants.first_week

    query = "UPDATE {0} SET `current_week` = '{1}' ".format(constants.table_week, week)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)


def remove_weeks():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_week)
    cursor.execute(query)

    db.commit()
    close_connection(cursor, db)


# teacher
def add_teacher(teacher):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "INSERT INTO {0} (name_teacher, chat_id) VALUES (?, ?)".format(constants.table_teachers)

    val = (teacher.name_teacher, teacher.chat_id)

    cursor.execute(query, val)
    db.commit()

    close_connection(cursor, db)


def remove_teachers():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_teachers)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def remove_teacher_by_chat_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0} WHERE `chat_id` = {1}".format(constants.table_teachers, chat_id)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def get_teachers():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_teachers)

    teachers = cursor.execute(query)

    list = []

    if teachers:
        for teacher in teachers:
            list.append(Teacher(data=teacher))

        close_connection(cursor, db)
        return list
    else:
        close_connection(cursor, db)
        return None


def get_teacher_by_chat_id(chat_id):
    db = get_db_connect()
    cursor = get_cursor(db)
    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_teachers, chat_id)

    teachers = cursor.execute(query)

    if teachers:
        for teacher in teachers:
            close_connection(cursor, db)
            return Teacher(data=teacher)
    else:
        close_connection(cursor, db)
        return None


def get_teacher_lessons(teacher_name):
    lessons = get_lessons()

    lessons_teacher = []

    for lesson in lessons:
        result = tools.search_teacher_in_str(lesson, teacher_name)

        if result:
            lessons_teacher.append(result)

    if lessons_teacher:
        return lessons_teacher
    else:
        return None


def get_teacher_lessons_by_day_name(teacher_name, day_name):
    lessons = get_teacher_lessons(teacher_name)

    lessons_by_day_name = []

    if lessons:
        for lesson in lessons:
            if lesson.day_name == day_name:
                lessons_by_day_name.append(lesson)

    if lessons_by_day_name:
        return lessons_by_day_name
    else:
        return None


def get_teacher_lessons_by_week(teacher_name, week):
    lessons = get_teacher_lessons(teacher_name)

    lessons_by_week = []

    if lessons:
        for lesson in lessons:
            if lesson.week == week:
                lessons_by_week.append(lesson)

    if lessons_by_week:
        return lessons_by_week
    else:
        return None


def get_teacher_lessons_by_week_and_day_name(teacher_name, day_name, week):

    lessons = get_teacher_lessons(teacher_name)

    lessons_by_week_and_day_name = []

    if lessons:
        for lesson in lessons:
            if lesson.day_name == day_name and lesson.week == week:
                lessons_by_week_and_day_name.append(lesson)

    if lessons_by_week_and_day_name:
        return lessons_by_week_and_day_name
    else:
        return None


# event
def add_event(event):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "INSERT INTO {0} (group_id, day_name, week, chat_id, send_time, is_send) " \
            "VALUES (?, ?, ?, ?, ?, ?)".format(constants.table_events)

    val = (event.group_id,
           event.day_name,
           event.week,
           event.chat_id,
           str(event.send_time).replace(".", ":"),
           event.is_send)

    cursor.execute(query, val)
    db.commit()

    close_connection(cursor, db)


def get_event(day_name, week, time):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE `send_time` = '{1}' AND `day_name` = '{2}' AND `week` = '{3}'".format(
        constants.table_events,
        time,
        day_name,
        week)

    result = cursor.execute(query)

    answer = []

    if result:
        for el in result:
            if el:
                answer.append(Event(data=el))

        close_connection(cursor, db)
        return answer
    else:
        close_connection(cursor, db)
        return None


def is_registration_event(chat_id, week):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0} WHERE `chat_id` = '{1}' AND `week` = '{2}'".format(constants.table_events,
                                                                                  chat_id,
                                                                                  week)
    data = cursor.execute(query)

    events = []

    if data:
        for el in data:
            events.append(el)

        if len(events) > 0:
            close_connection(cursor, db)
            return True
        else:
            close_connection(cursor, db)
            return False


def get_events():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_events)

    data = cursor.execute(query)

    events = tools.data_to_list_class(data, "event")

    close_connection(cursor, db)

    return events


def update_event(event):
    db = get_db_connect()
    cursor = get_cursor(db)

    # "UPDATE {0} SET group_id = '{1}' WHERE chat_id = '{2}'"
    query = "UPDATE {0} SET `day_name` = '{1}', `send_time` = '{2}', `week` = '{3}', `is_send` = '{4}' " \
            "WHERE `id` = '{5}'".format(constants.table_events, event.day_name,
                                        event.send_time, event.week, event.is_send, event.id)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


def get_list_time_events():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT `send_time` FROM {0}".format(constants.table_events)

    result = cursor.execute(query)

    list_times = []

    if result:
        for el in result:
            list_times.append(el[0])

        close_connection(cursor, db)
        return list_times
    else:
        close_connection(cursor, db)
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

    query = "DELETE FROM {0} WHERE `chat_id` = '{1}'".format(constants.table_events, chat_id)
    cursor.execute(query)

    db.commit()
    close_connection(cursor, db)


def drop_table(table_name, db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "DROP TABLE {0}".format(table_name)

    cursor.execute(query)
    db.commit()

    close_connection(cursor, db)


# faculty
def add_faculty(faculty, db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "INSERT INTO {0} (faculty, group_id) VALUES (?, ?)".format(constants.table_faculty)

    val = (faculty.faculty, faculty.group_id)

    try:
        cursor.execute(query, val)
    except:
        print("dont add faculty to db")

    db.commit()

    close_connection(cursor, db)


def get_faculties(db_name=None):
    if db_name:
        db = get_db_connect(db_name)
    else:
        db = get_db_connect()

    cursor = get_cursor(db)

    query = "SELECT * FROM {0}".format(constants.table_faculty)

    data = cursor.execute(query)

    if data:
        faculties = tools.data_to_list_class(data, "faculty")
        close_connection(cursor, db)
        return faculties
    else:
        close_connection(cursor, db)
        return None


def get_faculty_by_group_id(group_id):
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "SELECT faculty FROM {} WHERE `group_id` = '{}'".format(constants.table_faculty, group_id)

    data = cursor.execute(query)

    if data:
        for el in data:
            return str(el[0])
        close_connection(cursor, db)
    else:
        close_connection(cursor, db)
        return None


def get_group_id_by_faculty_name(faculty_name):
    db = get_db_connect()
    cursor = get_cursor(db)

    answer = []

    query = str("SELECT * FROM {} WHERE `faculty` = '{}'") \
        .format(constants.table_faculty, faculty_name)

    data = cursor.execute(query)

    faculties = tools.data_to_list_class(data, "faculty")
    lessons = get_lessons()

    for faculty in faculties:
        if str(faculty.faculty) == faculty_name:

            for lesson in lessons:
                if str(lesson.group_id) == str(faculty.group_id):
                    answer.append(faculty.group_id)
                    break

    if faculties:
        close_connection(cursor, db)
        return answer
    else:
        close_connection(cursor, db)
        return None


def remove_faculty():
    db = get_db_connect()
    cursor = get_cursor(db)

    query = "DELETE FROM {0}".format(constants.table_faculty)

    cursor.execute(query)
    db.commit()
    close_connection(cursor, db)
