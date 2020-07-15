import telebot
import constants
import sqlite3
from database.user import User
from database.teacher import Teacher
from database import db_manager
import tools
import os

bot = telebot.TeleBot(constants.token)

# if not exists tables, create it
db_manager.create_table_users()
db_manager.create_table_teachers()
db_manager.create_table_lessons()
db_manager.create_table_week()


def parse_send_message(chat_id, text, keyboard=None):
    message = None

    if keyboard:
        message = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = bot.send_message(chat_id, text, parse_mode="HTML")

    return message


# commands handler
@bot.message_handler(
    commands=["start", "settings", "about", "get_users", "drop_users", "add_lessons", "drop_lessons", "current_week",
              "change_week", "teacher", "drop_teachers"])
def commands_handler(message):
    msg = message.text
    chat_id = message.chat.id

    if msg == "/start":

        users = db_manager.get_users()

        for user in users:
            if str(chat_id) == user.chat_id:
                bot.send_message(chat_id, constants.you_is_register, reply_markup=tools.get_required_keyboard())
                return

        answer = parse_send_message(chat_id, constants.start_answer)

        groups = db_manager.get_group_list()

        # list_groups = tools.data_to_str(groups)

        list_groups = ""

        for group in groups:
            list_groups += str(group) + ", "

        reply_message = bot.reply_to(answer, constants.pick_your_group + "\n\n" + list_groups)

        bot.register_next_step_handler(reply_message, process_group_step)

    elif msg == "/settings":
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == "/about":
        parse_send_message(chat_id, constants.about_anser)

    elif msg == "/get_users":

        users = db_manager.get_users()

        answer = ""
        count_users = len(users)

        if count_users == 0:
            answer = "DB Users is empty"
        else:
            answer = "Count users " + str(count_users) + "\n\n"

        for user in users:
            answer += user.name_user + ", "

        bot.send_message(chat_id, answer)

    elif msg == "/drop_users":
        db_manager.remove_users()

        bot.send_message(chat_id, "Table {0} cleared".format(constants.table_users))

    elif msg == "/add_lessons":
        handle_message = bot.send_message(chat_id, "Enter file")
        bot.register_next_step_handler(handle_message, process_download_file_step)

    elif msg == "/drop_lessons":
        db_manager.remove_lessons()

        lessons = db_manager.get_lessons()

        if len(lessons) == 0:
            bot.send_message(chat_id, "Table {0} is cleared".format(constants.table_lessons))

    elif msg == "/current_week":
        current_week = db_manager.get_current_week()

        bot.send_message(chat_id, current_week)

    elif msg == "/change_week":
        db_manager.change_week()

        current_week = db_manager.get_current_week()

        bot.send_message(chat_id, current_week)

    elif msg == "/teacher":

        reply_message = bot.send_message(chat_id, "Please, enter Your name:")

        bot.register_next_step_handler(reply_message, process_register_teacher)

    elif msg == "/drop_teachers":

        db_manager.remove_teachers()

        teachers = db_manager.get_teachers()

        if not teachers:
            bot.send_message(chat_id, "Table {0} cleared".format(constants.table_teachers))


# handler text massages
@bot.message_handler(content_types=["text"])
def message_handler(message):
    msg = message.text
    chat_id = message.chat.id

    if msg == constants.keyboard_setting:
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == constants.keyboard_current_lessons:
        group_id = db_manager.get_user_group_id(chat_id)

        teacher = db_manager.get_teacher_by_chat_id(chat_id)

        if teacher:
            print(teacher.format_print())

        elif group_id:
            day_name = tools.get_current_day_name()

            if not day_name:
                bot.send_message(chat_id, "Dont lessons current :)")
                return

            current_week = db_manager.get_current_week()

            lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

            lessons_str = tools.data_to_str(lessons, is_message=True)

            if lessons_str:

                answer = tools.format_name_day(day_name) + "\n\n" + lessons_str

                bot.send_message(chat_id, answer)

        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == constants.keyboard_tomorrow_lessons:
        group_id = db_manager.get_user_group_id(chat_id)

        if group_id:
            day_name = tools.get_next_day_name()

            if not day_name:
                bot.send_message(chat_id, "Dont lessons current :)")
                return

            current_week = db_manager.get_current_week()

            lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

            lessons_str = tools.data_to_str(lessons, is_message=True)

            if lessons_str:

                answer = tools.format_name_day(day_name) + "\n\n" + lessons_str

                bot.send_message(chat_id, answer)
        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == constants.keyboard_week_lessons:
        group_id = db_manager.get_user_group_id(chat_id)

        if group_id:
            current_week = db_manager.get_current_week()

            lessons = db_manager.get_lessons_by_week(group_id, current_week)

            answer = ""
            day_name = ""

            for lesson in lessons:
                if not day_name:
                    day_name = lesson.day_name
                    answer += tools.format_name_day(day_name) + "\n"

                if day_name:
                    if day_name == lesson.day_name:
                        answer += lesson.format_message() + "\n"

                    else:
                        day_name = lesson.day_name
                        answer += "\n" + tools.format_name_day(day_name) + "\n" + lesson.format_message() + "\n"

            bot.send_message(chat_id, answer)

            # if lessons_str:
            #     bot.send_message(chat_id, lessons_str)
        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == "user":

        group_id = db_manager.get_user_group_id(chat_id)

        bot.send_message(chat_id, group_id)

    elif msg == "groups":

        groups = db_manager.get_group_list()

        print(groups)

    else:
        parse_send_message(chat_id, constants.not_found_answer)


# callback functions
def process_register_teacher(message):
    lessons = db_manager.get_lessons()

    list = []

    entered_name = str(message.text)

    for lesson in lessons:
        info = str(lesson.info)

        result = tools.search_teacher_in_str(lesson, entered_name)

        if result:
            list.append(result)
            print(result.format_print())

    if len(list) > 1:
        db_manager.add_teacher(Teacher(entered_name, message.chat.id))


def process_group_step(message):
    group_id = str(message.text)

    groups = db_manager.get_group_list()

    not_registered = True

    for group in groups:
        if group_id == group:
            user = tools.get_user_info(message)

            not_registered = False

            user.group_id = group_id

            db_manager.add_user(user)

            bot.send_message(message.chat.id, constants.thanks_for_a_registration, reply_markup=tools.get_required_keyboard())

    if not_registered:
        list_groups = tools.data_to_str(groups)

        reply_message = bot.reply_to(message, constants.pick_your_group + "\n\n" + list_groups)

        bot.register_next_step_handler(reply_message, process_group_step)


def process_download_file_step(message):
    path = os.path.join(constants.documents_directory, constants.excel_file)

    if not os.path.exists(constants.documents_directory):
        os.mkdir(constants.documents_directory)

    if not message.content_type == "document":
        bot.send_message(message.chat.id, constants.file_not_found)
        return

    file_info = bot.get_file(message.document.file_id)
    type_file = str(file_info.file_path).split(".")[-1]

    if os.path.exists(path):
        os.remove(path)

    if type_file == 'xlsx' or type_file == "xls":
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

        lessons = tools.read_excel(file_path)

        for lesson in lessons:
            try:
                db_manager.add_lesson(lesson)
            except sqlite3.DatabaseError as error:
                bot.send_message(constants.admin_chat_id, "Error in add lesson to DB " + str(error))

        bot.send_message(message.chat.id, "File read")


bot.polling(none_stop=True, interval=0)
