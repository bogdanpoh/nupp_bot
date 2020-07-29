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

command_list = ["0001", "start", "settings", "about", "change_group", "get_users", "drop_users", "drop_lessons",
                "current_week", "change_week", "teacher", "drop_teachers"]


def parse_send_message(chat_id, text, keyboard=None):
    message = None

    if keyboard:
        message = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = bot.send_message(chat_id, text, parse_mode="HTML")

    return message


def show_log(message, is_command):
    user = tools.get_user_info(message)
    info = str(user.name_user + " - " + message.text)
    print(info)

    if not is_command:
        parse_send_message(message.chat.id, constants.not_found_answer + " - " + message.text)

    bot.send_message(constants.admin_log, info)


# commands handler
@bot.message_handler(commands=command_list)
def commands_handler(message):
    msg = message.text
    chat_id = message.chat.id

    is_command = True

    if msg == "/0001":

        commands = ""

        for command in command_list:
            commands += "/" + command + "\n"

        bot.send_message(chat_id, commands)

    elif msg == "/start":
        users = db_manager.get_users()

        for user in users:
            if str(chat_id) == user.chat_id:
                bot.send_message(chat_id, constants.you_is_register, reply_markup=tools.get_required_keyboard())
                return

        answer = parse_send_message(chat_id, constants.start_answer)

        groups = db_manager.get_group_list()

        list_groups = tools.array_to_one_line(tools.sorted_groups(groups))

        reply_message = bot.reply_to(answer, constants.pick_your_group + "\n\n" + list_groups[:-2], parse_mode="HTML")

        bot.register_next_step_handler(reply_message, process_group_step)

    elif msg == "/settings":
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == "/about":
        parse_send_message(chat_id, constants.about_anser)

    elif msg == "/change_group":

        groups = db_manager.get_group_list()

        list_groups = tools.array_to_one_line(tools.sorted_groups(groups))

        reply_message = bot.send_message(chat_id, constants.pick_your_group + "\n\n" + list_groups, parse_mode="HTML")
        bot.register_next_step_handler(reply_message, process_change_group_step)

    elif msg == "/get_users":
        users = db_manager.get_users()

        answer = ""

        count_users = len(users)

        if count_users == 0:
            answer = "DB Users is empty"
        else:
            answer = "Count users " + str(count_users) + "\n\n"

        for user in users:
            answer += user.name_user + " - " + user.group_id + ", "

        bot.send_message(chat_id, answer[:-2])

    elif msg == "/drop_users":
        db_manager.remove_users()

        bot.send_message(chat_id, "Table {0} cleared".format(constants.table_users))

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

    else:
        is_command = False

    show_log(message, is_command)


# handler text massages
@bot.message_handler(content_types=["text"])
def message_handler(message):
    msg = message.text
    chat_id = message.chat.id
    current_week = db_manager.get_current_week()
    groups = db_manager.get_group_list()
    is_command = True

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
                bot.send_message(chat_id, constants.no_lessons_tomorrow)
                return

            else:
                lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

                if lessons:

                    lessons_str = tools.data_to_str(lessons, is_message=True)

                else:
                    bot.send_message(chat_id, constants.no_lessons_today)
                    return

                if lessons_str:

                    answer = tools.format_name_day(day_name) + "\n\n" + lessons_str

                    parse_send_message(chat_id, answer)

        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == constants.keyboard_tomorrow_lessons:
        group_id = db_manager.get_user_group_id(chat_id)

        if group_id:
            day_name = tools.get_next_day_name()

            if not day_name:
                bot.send_message(chat_id, constants.no_lessons_tomorrow)
                return

            lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

            if lessons:
                lessons_str = tools.data_to_str(lessons, is_message=True)

            else:
                bot.send_message(chat_id, constants.no_lessons_tomorrow)
                return

            if lessons_str:

                answer = tools.format_name_day(day_name) + "\n\n" + lessons_str

                parse_send_message(chat_id, answer)
        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == constants.keyboard_week_lessons:
        group_id = db_manager.get_user_group_id(chat_id)

        if group_id:

            lessons = db_manager.get_lessons_by_week(group_id, current_week)

            answer = tools.format_lessons_week_for_message(lessons)

            parse_send_message(chat_id, answer)

        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == "user":

        user = db_manager.get_user_by_chat_id(chat_id)

        tools.get_user_info(message)

        bot.send_message(chat_id, user.format_print())

    elif msg == "groups":

        sorted_groups = tools.sorted_groups(groups)

        answer = tools.array_to_one_line(sorted_groups)

        bot.send_message(chat_id, answer[:-2])

    elif msg == "count-lessons":
        lessons = db_manager.get_lessons()

        bot.send_message(chat_id, str(len(lessons)))

    elif msg == "remove-me":
        is_remove = True

        db_manager.remove_user_by_chat_id(chat_id)

        if not db_manager.is_user(chat_id):
            bot.send_message(chat_id, "You removed from DB")

    elif msg == "time":
        bot.send_message(chat_id, tools.get_current_time())

    else:
        is_command = False

        if groups:
            for group in groups:
                if group == msg:
                    lessons = db_manager.get_lessons_by_week(group, current_week)
                    answer = tools.format_lessons_week_for_message(lessons)

                    parse_send_message(chat_id, answer)
                    is_command = True

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

        lessons = tools.read_lessons(file_path)

        if lessons:
            group_id = lessons[0].group_id

            if db_manager.is_group(group_id):
                db_manager.remove_lessons_by_group_id(group_id)

            for lesson in lessons:
                try:
                    db_manager.add_lesson(lesson)
                except sqlite3.DatabaseError as error:
                    bot.send_message(constants.admin_chat_id, "Error in add lesson to DB " + str(error))

            bot.send_message(message.chat.id, "Lessons add to database")
        else:
            bot.send_message(message.chat.id, "Lessons dont found")
    else:
        parse_send_message(message.chat.id, "File is not <b>xlsx</b> and <b>xls</b>")


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


def process_change_group_step(message):

    if db_manager.is_group(message.text):
        db_manager.update_user_group(message.chat.id, message.text)
        bot.send_message(message.chat.id, constants.change_group)

    else:
        groups = db_manager.get_group_list()

        line_groups = tools.array_to_one_line(groups)

        reply_message = bot.send_message(message.chat.id, constants.pick_your_group + "\n\n" + line_groups, parse_mode="HTML")

        bot.register_next_step_handler(reply_message, process_change_group_step)


def process_group_step(message):
    group_id = str(message.text)

    is_group = db_manager.is_group(group_id)

    if is_group:
        user = tools.get_user_info(message)
        user.group_id = group_id
        db_manager.add_user(user)
        bot.send_message(message.chat.id, constants.thanks_for_a_registration,
                         reply_markup=tools.get_required_keyboard())
        bot.send_message(constants.admin_log, "New user - {0}".format(user.name_user))
    else:
        groups = tools.sorted_groups(db_manager.get_group_list())
        list_groups = tools.array_to_one_line(groups)
        reply_message = bot.reply_to(message, constants.pick_your_group + "\n\n" + list_groups[:-2], parse_mode="HTML")
        bot.register_next_step_handler(reply_message, process_group_step)


bot.polling(none_stop=True, interval=0, timeout=0)
