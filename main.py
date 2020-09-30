import telebot
import constants
import config
import sqlite3
from database.user import User
from database.teacher import Teacher
from database.event import Event
from database import db_manager
import tools
import os
import threading
import time


current_token = config.test_token
bot = telebot.TeleBot(current_token)
lang = constants.lang_ua

# if not exists tables, create it
db_manager.create_table_users()
db_manager.create_table_teachers()
db_manager.create_table_lessons()
db_manager.create_table_week()
db_manager.create_table_events()
db_manager.create_table_faculty()

command_list = ["remove_lessons", "remove_teachers", "remove_users", "remove_events", "remove_weeks", "remove_group",
                "remove_faculty", "rename_group_id",
                "drop_table_events", "drop_table_users",
                "start", "settings", "about", "help", "en",
                "change_group", "change_lang", "change_week",
                "current_week", "get_users", "get_users_count", "send_all_message", "teacher", "get_teachers",
                "enable_reminders", "disable_reminders",
                "get_db_bot", "groups", "get_groups","events", "time", "user", "count_groups", "count_lessons", "remove_me"]


def get_groups():

    faculties = db_manager.get_faculties()
    faculties_name = []

    answer = ""

    for faculty in faculties:
        faculties_name.append(faculty.faculty)

    faculties_sorted = tools.remove_repetition(faculties_name)

    for faculty in faculties_sorted:

        groups = db_manager.get_group_id_by_faculty_name(faculty)

        answer += tools.to_bold(faculty) + " - "

        if groups:
            answer += tools.array_to_one_line(tools.sorted_groups(groups))[:-2]
        else:
            answer += "None"

        answer += "\n\n"

    return answer


def parse_send_message(chat_id, text, keyboard=None):

    if keyboard:
        message = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = bot.send_message(chat_id, text, parse_mode="HTML")

    return message


def show_log(message, is_command):
    user = tools.get_user_info_from_message(message)

    if current_token == config.token:
        format_info = str("@" + tools.to_bold(user.name_user) + " - " + message.text)

        if not is_command:

            answer = constants.not_found_answer

            if db_manager.is_user(user.chat_id):
                if db_manager.get_user_by_chat_id(user.chat_id).language == constants.lang_en:
                    answer = constants.not_found_answer_en

            parse_send_message(message.chat.id, answer + " - " + tools.to_bold(message.text))

        parse_send_message(constants.admin_log, format_info)

    time.sleep(2)

    info = str(user.name_user + " - " + message.text)

    print(info)


@bot.message_handler(regexp="/add_faculty")
def handler(message):
    reply_message = bot.send_message(message.chat.id, "Enter faculty_file: ")

    bot.register_next_step_handler(reply_message, process_add_faculty)


@bot.message_handler(regexp="date")
def handler(message):
    current_week = db_manager.get_current_week()

    day_name = tools.get_current_day_name()
    day_and_month = tools.get_current_day_and_month()

    date = tools.get_current_date()

    print("Current week: {}, day_name: {}, day_month: {}, date: {}".format(current_week, day_name, day_and_month,date))


@bot.message_handler(regexp="def_week")
def handler(message):
    db_manager.set_default_week()

    current_week = db_manager.get_current_week()

    bot.send_message(message.chat.id, current_week)


@bot.message_handler(regexp="/check_group")
def handler(message):
    reply_message = bot.send_message(message.chat.id, "Enter group_id:")
    bot.register_next_step_handler(reply_message, process_check_group_id)

# commands admin
@bot.message_handler(regexp="0001")
def regexp_handler(message):

    commands = ""

    for command in command_list:
        commands += "/" + command + "\n"

    bot.send_message(message.chat.id, commands)


@bot.message_handler(regexp="statistics_info")
def statistic_commands_handler(message):

    answer = """/count_groups - Загальна кількість груп, чий розклад в боті
/groups - Список груп, які є в боті
/get_users - отримати загальну кількість користувачів та список
/get_users_count - отримати загальну кількість користувачів"""

    parse_send_message(message.chat.id, answer)


# commands handler
@bot.message_handler(commands=command_list)
def commands_handler(message):
    msg = message.text
    chat_id = message.chat.id
    current_week = db_manager.get_current_week()

    is_command = True

    if msg == "/start":
        users = db_manager.get_users()

        if users:
            for user in users:
                if str(chat_id) == user.chat_id:
                    bot.send_message(chat_id, constants.you_is_register, reply_markup=tools.get_required_keyboard())
                    return

        select_answer = constants.start_answer

        if lang == constants.lang_en:
            select_answer = constants.start_answer_en

        answer = parse_send_message(chat_id, select_answer)

        groups = db_manager.get_group_list()

        if groups:
            select_answer_pick_group = constants.pick_your_group

            if lang == constants.lang_en:
                select_answer_pick_group = constants.pick_your_group_en

            reply_message = bot.reply_to(answer, select_answer_pick_group + "\n\n" + get_groups(), parse_mode="HTML")

            bot.register_next_step_handler(reply_message, process_group_step)

        else:
            bot.send_message(chat_id, "Dont found groups in DB")

    elif msg == "/settings":
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == "/about":

        answer = constants.about_answer

        if db_manager.is_user(chat_id):
            if db_manager.get_user_by_chat_id(chat_id).language == constants.lang_en:
                answer = constants.about_answer_en

        parse_send_message(chat_id, answer)

    elif msg == "/help":
        bot.send_message(chat_id, constants.help_answer)

    elif msg == "/change_group":

        list_groups = get_groups()

        answer_change_group = constants.pick_your_group.split("\n")[0]
        cancel = constants.cancel

        if db_manager.is_user(chat_id):
            if db_manager.get_user_by_chat_id(chat_id).language == constants.lang_en:
                answer_change_group = constants.pick_your_group_en.split("\n")[0]
                cancel = constants.cancel_en

        reply_message = bot.send_message(chat_id,
                                         answer_change_group + "\n\n" + list_groups + cancel,
                                         parse_mode="HTML")
        bot.register_next_step_handler(reply_message, process_change_group_step)

    elif msg == "/change_lang":
        if db_manager.is_user(chat_id):

            current_lang = db_manager.get_user_by_chat_id(chat_id).language

            new_lang = constants.lang_ua

            if current_lang == constants.lang_ua:
                new_lang = constants.lang_en
                answer = "Language"
            else:
                new_lang = constants.lang_ua
                answer = "Мова"

            db_manager.update_user_lang(chat_id, new_lang)

            bot.send_message(chat_id, "{} - {}".format(answer, new_lang), reply_markup=tools.get_required_keyboard(new_lang))

    elif msg == "/get_users":
        users = db_manager.get_users()

        if users:
            count_users = len(users)

            answer = "Кількість користувачів: " + str(count_users) + "\n\n"

            bot.send_message(chat_id, answer)

            for user in users:
                answer += "Нікнейм: " + user.name_user + ", група - " + user.group_id + "\n"

            path = os.path.join(constants.documents_directory, constants.txt_file)

            if os.path.isfile(path):
                os.remove(path)

            tools.write_to_file(path, answer)

            if os.path.isfile(path):
                info = open(path, "rb")

                bot.send_document(chat_id, info)

        else:
            answer = "Таблиця користувачів <b>порожня</b>"
            parse_send_message(chat_id, answer)

    elif msg == "/remove_users":
        db_manager.remove_users()

        users = db_manager.get_users()

        if len(users) == 0:
            bot.send_message(chat_id, "Table {0} cleared".format(constants.table_users))

    elif msg == "/remove_lessons":
        db_manager.remove_lessons()

        lessons = db_manager.get_lessons()

        if not lessons:
            bot.send_message(chat_id, "Table {0} is cleared".format(constants.table_lessons))

    elif msg == "/current_week":
        bot.send_message(chat_id, current_week)

    elif msg == "/change_week":
        db_manager.change_week()

        current_week = db_manager.get_current_week()

        bot.send_message(chat_id, current_week)

    elif msg == "/remove_weeks":
        db_manager.remove_weeks()

    elif msg == "/teacher":
        reply_message = bot.send_message(chat_id, "Please, enter Your name:")

        bot.register_next_step_handler(reply_message, process_register_teacher)

    elif msg == "/get_teachers":
        teachers = db_manager.get_teachers()

        teachers_str = "Count: " + str(len(teachers)) + "\n\n" + tools.data_to_str(data=teachers, is_class=True)

        if teachers_str:
            bot.send_message(chat_id, teachers_str)
        else:
            bot.send_message(chat_id, "DB {0} is clear".format(constants.table_teachers))

    elif msg == "/remove_teachers":
        db_manager.remove_teachers()

        teachers = db_manager.get_teachers()

        if not teachers:
            bot.send_message(chat_id, "Table {0} cleared".format(constants.table_teachers))

    elif msg == "/remove_events":
        db_manager.remove_events()

        events = db_manager.get_events()

        if not events:
            bot.send_message(chat_id, "Table {} is cleared".format(constants.table_events))

    elif msg == "/disable_reminders":
        bot.send_message(chat_id, "Функція запрацює з появою постійного розкладу")
        # if db_manager.is_registration_event(chat_id, current_week):
        #     db_manager.remove_event_by_chat_id(chat_id)
        #     bot.send_message(chat_id, constants.reminders_disable)

    elif msg == "/enable_reminders":
        # user = db_manager.get_user_by_chat_id(chat_id)
        # week = current_week
        # day = tools.get_current_day_name()
        # current_time = tools.get_current_time()
        #
        # if db_manager.is_registration_event(chat_id, current_week):
        #     bot.send_message(chat_id, constants.reminders_is_enable)
        #     return
        #
        # if not day:
        #     day_name = tools.format_name_day(constants.monday)
        #     week = tools.get_next_week(current_week)
        # else:
        #     day_name = day
        #
        # lesson = db_manager.get_lessons_by_day_name(day_name=day_name, group_id=user.group_id, week=current_week)
        #
        # if lesson:
        #     lesson = lesson[0]
        #     if tools.is_today_register_time_for_event(current_time, tools.format_time_for_event(lesson.time_start)):
        #         day_name = tools.get_next_day_name()
        #
        #         if not day_name:
        #             day_name = tools.format_name_day(constants.monday)
        #             week = tools.get_next_week(current_week)
        #
        #         lesson_by_day_name = db_manager.get_lessons_by_day_name(day_name, week, user.group_id)
        #
        #         if len(lesson_by_day_name) > 2:
        #             lesson = lesson_by_day_name[0]
        #
        #
        #     event = Event(group_id=user.group_id,
        #                   week=lesson.week,
        #                   day_name=lesson.day_name,
        #                   chat_id=user.chat_id,
        #                   send_time=tools.format_time_for_start_event(tools.format_time_for_event(lesson.time_start)),
        #                   is_send=False)
        #
        #     db_manager.add_event(event)
        #     bot.send_message(chat_id, constants.reminders_enable)
        #
        # else:
        bot.send_message(chat_id, "Функція запрацює з появою постійного розкладу")

    elif msg == "/get_db_bot":
        db_file = open("telegram_bot.db", "rb")
        bot.send_document(chat_id, db_file)

    elif msg == "/groups":

        groups = get_groups()

        if groups:
            parse_send_message(chat_id, get_groups())
        else:
            bot.send_message(chat_id, "DB Lessons is clear")

    elif msg == "/events":
        events = db_manager.get_events()

        if not events:
            bot.send_message(chat_id, "DB Event is clear")

        else:
            answer = "Count: {0}\n\n".format(str(len(events)))

            for event in events:
                answer += event.format_print() + "\n\n"

            bot.send_message(chat_id, answer)

    elif msg == "/time":
        bot.send_message(chat_id, tools.get_current_time())

    elif msg == "/user":

        user = db_manager.get_user_by_chat_id(chat_id)

        if user:
            tools.get_user_info_from_message(message)

            bot.send_message(chat_id, user.format_print())

    elif msg == "/count_groups":
        groups = db_manager.get_group_list()

        parse_send_message(chat_id, "Кількість груп: <i>{}</i>".format(str(len(groups))))

    elif msg == "/count_lessons":
        lessons = db_manager.get_lessons()

        bot.send_message(chat_id, str(len(lessons)))

    elif msg == "/remove_me":
        db_manager.remove_user_by_chat_id(chat_id)
        db_manager.remove_teacher_by_chat_id(chat_id)

        bot.send_message(chat_id, "You removed from DB")

    elif msg == "/get_users_count":
        users = db_manager.get_users()

        if users:
            count_users = str(len(users))
            parse_send_message(chat_id, "Всього користувачів: <i>{}</i>".format(count_users))

        else:
            parse_send_message(chat_id, "Таблиця користувачів <b>порожня</b>")

    elif msg == "/drop_table_events":
        db_manager.drop_table(constants.table_events)

        bot.send_message(chat_id, "Table {0} is drop".format(constants.table_events))

    elif msg == "/drop_table_users":
        db_manager.drop_table(constants.table_users)
        bot.send_message(chat_id, "Table {} is drop".format(constants.table_users))

    elif msg == "/send_all_message":
        reply_message = bot.send_message(chat_id, "Напешіть повідомлення:")

        bot.register_next_step_handler(reply_message, process_send_messages)

    elif msg == "/remove_group":
        reply_message = bot.send_message(chat_id, "Enter group_id:")

        bot.register_next_step_handler(reply_message, process_remove_group)

    elif msg == "/remove_faculty":
        db_manager.remove_faculty()

        if len(db_manager.get_faculties()) == 0:
            bot.send_message(chat_id, "Table {} is clear".format(constants.table_faculty))

    elif msg == "/rename_group_id":
        reply_message = bot.send_message(chat_id, "Enter group_id and new group_id (101еМ, 101ЕМ):")
        bot.register_next_step_handler(reply_message, process_rename_group_id)

    elif msg == "/get_groups":
        groups = tools.sorted_groups(db_manager.get_group_list())

        answer = ""

        for group in groups:
            answer += str(group) + "\n"


        bot.send_message(chat_id, answer)

    else:
        is_command = False

    show_log(message, is_command)


def send_not_register(chat_id, lang):
    if lang == constants.lang_en:
        bot.send_message(chat_id, constants.not_register_en)
    else:
        bot.send_message(chat_id, constants.not_register)


def send_not_lessons(chat_id, lang, is_today=False):

    if lang == constants.lang_en:

        if is_today:
            msg = constants.no_lessons_today_en
        else:
            msg = constants.no_lessons_tomorrow_en

    else:

        if is_today:
            msg = constants.no_lessons_today
        else:
            msg = constants.no_lessons_tomorrow

    bot.send_message(chat_id, msg)


# handler text massages
@bot.message_handler(content_types=["text"])
def message_handler(message):
    msg = str(message.text)
    chat_id = str(message.chat.id)
    current_week = db_manager.get_current_week()
    groups = db_manager.get_group_list()
    is_command = True

    user_lang = constants.lang_ua

    if db_manager.is_user(chat_id):
        user_lang = db_manager.get_user_by_chat_id(chat_id).language
    else:
        bot.send_message(chat_id, constants.not_register)

    if not current_week:
        db_manager.set_default_week()

    if msg == constants.keyboard_setting or msg == constants.keyboard_setting_en:

        answer = constants.settings_answer

        if user_lang == constants.lang_en:
            answer = constants.settings_answer_en

        parse_send_message(chat_id, answer)

    elif msg == constants.keyboard_current_lessons or msg == constants.keyboard_current_lessons_en:
        group_id = db_manager.get_user_group_id(chat_id)
        day_name = tools.get_current_day_name()
        teacher = db_manager.get_teacher_by_chat_id(chat_id)

        if teacher:
            lessons = db_manager.get_teacher_lessons_by_week_and_day_name(teacher.name_teacher, day_name, current_week)

            if lessons:
                tools.sorted_lessons(lessons)

                lessons_str = tools.format_lessons_day_for_message(lessons,
                                                                   day_name,
                                                                   is_teacher_format=True)
                parse_send_message(chat_id, lessons_str)
            else:
                bot.send_message(chat_id, constants.no_lessons_today)
            return

        if group_id:
            if not day_name:
                # bot.send_message(chat_id, constants.no_lessons_today)
                send_not_lessons(chat_id, user_lang, is_today=True)
                return

            else:
                lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

                if lessons:
                    lessons_str = tools.format_lessons_day_for_message(lessons, day_name, lang=user_lang)
                    parse_send_message(chat_id, lessons_str)
                else:
                    send_not_lessons(chat_id, user_lang, is_today=True)
                    # parse_send_message(chat_id, constants.no_lessons_today)

        else:
            # bot.send_message(chat_id, "Please, send /start")

            send_not_register(chat_id, user_lang)

    elif msg == constants.keyboard_tomorrow_lessons or msg == constants.keyboard_tomorrow_lessons_en:
        teacher = db_manager.get_teacher_by_chat_id(chat_id)
        day_name = tools.get_next_day_name()
        group_id = db_manager.get_user_group_id(chat_id)

        if teacher:
            lessons = db_manager.get_teacher_lessons_by_week_and_day_name(teacher.name_teacher, day_name, current_week)

            if lessons:
                tools.sorted_lessons(lessons)

                lessons_str = tools.format_lessons_day_for_message(lessons, day_name, is_teacher_format=True)
                parse_send_message(chat_id, lessons_str)
            else:
                # bot.send_message(chat_id, constants.no_lessons_tomorrow)
                send_not_lessons(chat_id, user_lang, is_today=False)
            return

        if group_id:
            if not day_name:
                # bot.send_message(chat_id, constants.no_lessons_tomorrow)
                send_not_lessons(chat_id, user_lang, is_today=False)
                return

            else:
                lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

                if lessons:
                    lessons_str = tools.format_lessons_day_for_message(lessons, day_name, lang=user_lang)
                    parse_send_message(chat_id, lessons_str)
                else:
                    send_not_lessons(chat_id, user_lang, is_today=False)
                    # bot.send_message(chat_id, constants.no_lessons_tomorrow)
        else:
            # bot.send_message(chat_id, "Please, send /start")
            send_not_register(chat_id, user_lang)

    elif msg == constants.keyboard_week_lessons or msg == constants.keyboard_week_lessons_en:
        teacher = db_manager.get_teacher_by_chat_id(chat_id)
        group_id = db_manager.get_user_group_id(chat_id)

        if teacher:
            lessons = db_manager.get_teacher_lessons_by_week(teacher.name_teacher, current_week)

            if lessons:
                tools.sorted_lessons(lessons)

                lessons_str = tools.format_lessons_week_for_message(lessons, is_format_teacher=True)

                parse_send_message(chat_id, lessons_str)
                return
            else:
                bot.send_message(chat_id, "Dont found lessons")

        if group_id:

            lessons = db_manager.get_lessons_by_week(group_id, current_week)

            if lessons:
                lessons_week_str = tools.format_lessons_week_for_message(lessons, lang=user_lang)

                parse_send_message(chat_id, lessons_week_str)
            else:
                bot.send_message(chat_id, constants.dont_found_group)

        else:
            # bot.send_message(chat_id, "Please, send /start")
            send_not_register(chat_id, user_lang)

    elif msg[0] == "_":
        search_chat_id = msg.replace("_", "")

        if db_manager.is_user(search_chat_id):
            user = db_manager.get_user_by_chat_id(search_chat_id)
            bot.send_message(chat_id, user.format_print())
        else:
            bot.send_message(chat_id, "User dont found")

    else:
        is_command = False

        if groups:
            for group in groups:
                if str(group) == str(msg):
                    lessons = db_manager.get_lessons_by_week(group, current_week)
                    answer = tools.format_lessons_week_for_message(lessons, lang=user_lang)

                    is_command = True

                    if answer:
                        parse_send_message(chat_id, answer)
                    else:
                        parse_send_message(chat_id, constants.dont_found_group)

    show_log(message, is_command)


@bot.message_handler(content_types=["document"])
def file_handler(message):
    path = os.path.join(constants.documents_directory, constants.excel_file)

    if not os.path.exists(constants.documents_directory):
        os.mkdir(constants.documents_directory)

    if os.path.exists(path):
        os.remove(path)

    file_info = bot.get_file(message.document.file_id)
    type_file = str(file_info.file_path).split(".")[-1]

    if type_file == constants.excel_file_type or type_file == constants.excel_file_type_a:
        downloaded_file = bot.download_file(file_info.file_path)

        tools.download_file(path + "." + type_file, downloaded_file)

        file_path = ""

        if os.path.isfile(
                os.path.join(constants.documents_directory, constants.excel_file + "." + constants.excel_file_type)):
            file_path = os.path.join(constants.documents_directory,
                                     constants.excel_file + "." + constants.excel_file_type)
        elif os.path.isfile(
                os.path.join(constants.documents_directory, constants.excel_file + "." + constants.excel_file_type_a)):
            file_path = os.path.join(constants.documents_directory,
                                     constants.excel_file + "." + constants.excel_file_type_a)

        lessons = tools.read_lessons(file_path)

        if lessons:
            group_id = lessons[0].group_id

            if db_manager.is_group(group_id):
                db_manager.remove_lessons_by_group_id(group_id)

            for lesson in lessons:
                try:
                    db_manager.add_lesson(lesson)
                except sqlite3.Error as error:
                    bot.send_message(constants.admin_chat_id, "Error in add lesson to DB " + str(error))

            answer_str = "Lessons {0} add to database".format(group_id)
            parse_send_message(message.chat.id, answer_str)
            parse_send_message(constants.admin_log, answer_str)
            print(answer_str)
        else:
            bot.send_message(message.chat.id, "Lessons dont found")
    else:
        parse_send_message(message.chat.id, "File is not" + tools.to_bold("xlsx") + " and " + tools.to_bold("xls"))


# callback functions
def process_register_teacher(message):
    lessons = db_manager.get_lessons()

    list = []

    entered_name = str(message.text)

    for lesson in lessons:
        result = tools.search_teacher_in_str(lesson, entered_name)

        if result:
            list.append(result)

    if len(list) > 1:
        db_manager.add_teacher(Teacher(name_teacher=entered_name, chat_id=message.chat.id))
        parse_send_message(message.chat.id, constants.thanks_for_a_registration, keyboard=tools.get_required_keyboard())


def process_change_group_step(message):

    if db_manager.is_group(message.text):
        db_manager.update_user_group(message.chat.id, message.text)

        if db_manager.is_user(message.chat.id):
            if db_manager.get_user_by_chat_id(message.chat.id).language == constants.lang_en:
                bot.send_message(message.chat.id, constants.change_group_en)
            else:
                bot.send_message(message.chat.id, constants.change_group)

    else:

        if message.text == "/cancel":

            if db_manager.get_user_by_chat_id(message.chat.id).language == constants.lang_en:
                bot.send_message(message.chat.id, constants.cancel_success_en)
            else:
                bot.send_message(message.chat.id, constants.cancel_success)
            return

        # groups = db_manager.get_group_list()

        # line_groups = tools.array_to_one_line(groups)
        groups = get_groups()

        answer_pick = constants.pick_your_group.split("\n")[0]
        cancel = constants.cancel

        if db_manager.get_user_by_chat_id(message.chat.id).language == constants.lang_en:
            answer_pick = constants.pick_your_group_en.split("\n")[0]
            cancel = constants.cancel_en

        reply_message = bot.send_message(message.chat.id, answer_pick + "\n\n" + groups + cancel, parse_mode="HTML")

        bot.register_next_step_handler(reply_message, process_change_group_step)


def process_group_step(message):
    chat_id = message.chat.id
    group_id = str(message.text)

    global lang

    if message.text == "/teacher":
        reply_message = bot.send_message(chat_id, "Enter you name: ")
        bot.register_next_step_handler(reply_message, process_register_teacher)
        return

    if message.text == "/en":
        lang = constants.lang_en
    elif message.text == "/ua":
        lang = constants.lang_ua

    is_group = db_manager.is_group(group_id)

    if is_group:
        user = tools.get_user_info_from_message(message)

        if user:
            user.group_id = group_id
            user.language = lang
            db_manager.add_user(user)

            select_answer = constants.thanks_for_a_registration

            if lang == constants.lang_en:
                select_answer = constants.thanks_for_a_registration_en

            bot.send_message(chat_id, select_answer,
                             reply_markup=tools.get_required_keyboard(lang))

            parse_send_message(constants.admin_log, tools.to_bold("New user") + " - {0} , {1}: {2}"
                               .format(user.name_user, tools.to_bold("group"), user.group_id))
    else:
        select_answer = constants.pick_your_group

        if lang == constants.lang_en:
            select_answer = constants.pick_your_group_en

        reply_message = bot.reply_to(message, select_answer + "\n\n" + get_groups(), parse_mode="HTML")
        bot.register_next_step_handler(reply_message, process_group_step)


def process_remove_group(message):

    group_id = str(message.text)

    if db_manager.is_group(group_id):
        try:
            db_manager.remove_group(group_id)
            bot.send_message(message.chat.id, "Remove {} success".format(group_id))
        except:
            bot.send_message(message.chat.id, "Error remove group {}".format(group_id))

    else:
        bot.send_message(message.chat.id, "Dont found group: {}".format(group_id))


def process_send_messages(message):
    users = db_manager.get_users()

    msg = str(message.text)

    for user in users:
        time.sleep(10)
        if user.language == constants.lang_en:
            answer = constants.warning_en + "\n\n" + msg
        else:
            answer = constants.warning + "\n\n" + msg

        log = "send to {}".format(user.name_user)

        try:
            parse_send_message(user.chat_id, answer)
            parse_send_message(constants.admin_log, log)
            print(log)
        except:
            log = "Error in send message to user {} id: {}".format(user.name_user, user.chat_id)
            bot.send_message(constants.admin_log, log)
            print(log)

    bot.send_message(message.chat.id, "Success")


def process_add_faculty(message):

    path = os.path.join(constants.documents_directory, constants.excel_file_faculty)

    file_info = bot.get_file(message.document.file_id)
    type_file = str(file_info.file_path).split(".")[-1]

    if type_file == constants.excel_file_type or type_file == constants.excel_file_type_a:
        downloaded_file = bot.download_file(file_info.file_path)

        tools.download_file(path + "." + type_file, downloaded_file)

    path += "." + type_file

    if os.path.isfile(path):
        info = tools.read_faculty(path)

        for el in info:
            db_manager.add_faculty(el)


def check_current_week(current_time):
    if current_time == constants.change_week_time:
        if tools.get_current_day_name() == tools.format_name_day(constants.monday):
            db_manager.change_week()
            current_week = db_manager.get_current_week()
            bot.send_message(constants.admin_log, "week is change, current week - {}".format(current_week))
            print("week is change, current week - {}".format(current_week))
        else:
            bot.send_message(constants.admin_log, "Current day: {}".format(tools.get_current_day_name()))


def check_current_time():

    next_time = tools.get_current_time()

    while True:
        week = db_manager.get_current_week()
        day_name = tools.get_current_day_name()
        current_time = tools.get_current_time()

        if next_time != current_time:
            check_current_week(current_time)
            next_time = current_time

            print(current_time)
            bot.send_message(constants.admin_log, str(current_time))

            try:
                time_events = db_manager.get_list_time_events()

                if time_events:
                    for time in time_events:
                        if time == current_time:
                            events = db_manager.get_event(day_name, week, time)

                            if events:
                                for event in events:
                                    if not event.is_send and day_name == event.day_name and week == event.week:
                                        lessons = db_manager.get_lessons_by_day_name(event.day_name, event.week,
                                                                                     event.group_id)
                                        parse_send_message(event.chat_id,
                                                           tools.format_lessons_day_for_message(lessons,
                                                                                                event.day_name))

                                        next_day_name = tools.get_next_day_name()

                                        next_week = week

                                        if not next_day_name:
                                            next_day_name = tools.format_name_day(constants.monday)
                                            next_week = tools.get_next_week(week)

                                        next_lessons = db_manager.get_lessons_by_day_name(next_day_name, next_week,
                                                                                          event.group_id)

                                        lesson_time_start = tools.format_time_for_event(next_lessons[0].time_start)
                                        lesson_time_start_with_delta = tools.format_time_for_start_event(
                                            lesson_time_start)
                                        event.set_send_time(lesson_time_start_with_delta)
                                        event.set_week(next_week)
                                        event.set_day_name(next_day_name)

                                        db_manager.update_event(event)
            except sqlite3.OperationalError as error:
                print(str(error))
                bot.send_message(constants.admin_chat_id, str(error))
                bot.send_message(constants.admin_log, str(error))


def process_rename_group_id(message):
    group_id = str(message.text).replace(" ", "").split(",")

    if db_manager.is_group(group_id[0]):
        bot.send_message(message.chat.id, "this is correct group_id")
        db_manager.rename_group_id(group_id[0], group_id[-1])
    else:
        bot.send_message(message.chat.id, "this is dont correct group_id")


def process_check_group_id(message):
    group_id = str(message.text)

    if db_manager.is_group(group_id):
        bot.send_message(message.chat.id, "{} is group".format(group_id))
    else:
        bot.send_message(message.chat.id, "{} is dont group".format(group_id))


def main():
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as ex:
        print(str(ex))
        bot.send_message(constants.admin_chat_id, str(ex))
        bot.send_message(constants.admin_log, str(ex))

# bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    # check_time_thread = threading.Thread(target=check_current_time, daemon=True)
    # check_time_thread.start()

    # bot.send_message(constants.admin_chat_id, "Bot is run")
    # bot.send_message(constants.admin_log, "Bot is run")
    main()

