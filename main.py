import telebot
import constants
import sqlite3
from database.user import User
from database.teacher import Teacher
from database.event import Event
from database import db_manager
import tools
import os
import threading

bot = telebot.TeleBot(constants.token)

# if not exists tables, create it
db_manager.create_table_users()
db_manager.create_table_teachers()
db_manager.create_table_lessons()
db_manager.create_table_week()
db_manager.create_table_events()

command_list = ["start", "settings", "about", "change_group", "get_users", "drop_table_events", "drop_users",
                "drop_lessons", "remove_events", "current_week", "change_week", "teacher", "drop_teachers",
                "enable_reminders"]


def parse_send_message(chat_id, text, keyboard=None):

    if keyboard:
        message = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = bot.send_message(chat_id, text, parse_mode="HTML")

    return message


def show_log(message, is_command):
    user = tools.get_user_info(message)
    info = str(user.name_user + " - " + message.text)

    print(info)

    format_info = str("<b>" + user.name_user + "</b> - " + message.text)

    if not is_command:
        parse_send_message(message.chat.id, constants.not_found_answer + " - <b>" + message.text + "</b>")

    parse_send_message(constants.admin_log, format_info)


@bot.message_handler(regexp="my_event")
def handler(message):
    current_week = db_manager.get_current_week()

    count_my_events = db_manager.is_registration_event(message.chat.id, current_week)

    bot.send_message(message.chat.id, str(count_my_events))


@bot.message_handler(regexp="set_default_week")
def handler(message):
    db_manager.set_default_week()


@bot.message_handler(regexp="0001")
def regexp_handler(message):

    commands = ""

    for command in command_list:
        commands += "/" + command + "\n"

    bot.send_message(message.chat.id, commands)


# commands handler
@bot.message_handler(commands=command_list)
def commands_handler(message):
    msg = message.text
    chat_id = message.chat.id

    is_command = True

    if msg == "/start":
        users = db_manager.get_users()

        if users:
            for user in users:
                if str(chat_id) == user.chat_id:
                    bot.send_message(chat_id, constants.you_is_register, reply_markup=tools.get_required_keyboard())
                    return

        answer = parse_send_message(chat_id, constants.start_answer)

        groups = db_manager.get_group_list()

        if groups:
            list_groups = tools.array_to_one_line(tools.sorted_groups(groups))

            reply_message = bot.reply_to(answer, constants.pick_your_group + "\n\n" + list_groups[:-2], parse_mode="HTML")

            bot.register_next_step_handler(reply_message, process_group_step)

        else:
            bot.send_message(chat_id, "Dont found groups in DB")

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

        if users:
            count_users = len(users)

            answer = "Count users " + str(count_users) + "\n\n"

            for user in users:
                answer += user.name_user + " - " + user.group_id + ", "

        else:
            answer = "DB Users is empty"

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

    elif msg == "/drop_table_events":
        db_manager.drop_table_events()
        bot.send_message(chat_id, "Table {0} is drop".format(constants.table_events))

    elif msg == "/remove_events":
        db_manager.remove_events()

        if len(db_manager.get_events()) == 0:
            bot.send_message(chat_id, "DB Events is clear")

    elif msg == "/enable_reminders":
        current_week = db_manager.get_current_week()

        user = db_manager.get_user_by_chat_id(chat_id)

        day = tools.get_current_day_name()

        if db_manager.is_registration_event(chat_id, current_week):
            bot.send_message(chat_id, "You event is register")
            return

        if not day:
            day_name = tools.format_name_day(constants.monday)
        else:
            day_name = day

        lessons = db_manager.get_lessons_by_day_name(day_name=day_name, group_id=user.group_id, week=current_week)

        if lessons:
            lesson = lessons[0]

            if not tools.is_today_register_time_for_event(tools.get_current_time(), tools.format_time_for_event(lesson.time_start)):
                day_name = tools.get_next_day_name()

                if not day_name:
                    day_name = tools.format_name_day(constants.monday)
                    week = tools.get_next_week(current_week)

                    lesson = db_manager.get_lessons_by_day_name(day_name, week, user.group_id)[0]

            event = Event(group_id=user.group_id,
                          week=lesson.week,
                          day_name=lesson.day_name,
                          chat_id=user.chat_id,
                          send_time=tools.format_time_for_start_event(tools.format_time_for_event(lesson.time_start)),
                          is_send=False)

            db_manager.add_event(event)
            bot.send_message(chat_id, "Reminder is on")
        else:
            bot.send_message(constants.admin_chat_id, "dont lessons")

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

    if not current_week:
        db_manager.set_default_week()

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
                bot.send_message(chat_id, constants.no_lessons_today)
                return

            else:
                lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

                if lessons:
                    lessons_str = tools.format_lessons_day_for_message(lessons, day_name)
                    parse_send_message(chat_id, lessons_str)

        else:
            bot.send_message(chat_id, "Please, send /start")

    elif msg == constants.keyboard_tomorrow_lessons:
        group_id = db_manager.get_user_group_id(chat_id)

        if group_id:
            day_name = tools.get_next_day_name()

            if not day_name:
                bot.send_message(chat_id, constants.no_lessons_tomorrow)
                return

            else:
                lessons = db_manager.get_lessons_by_day_name(day_name, current_week, group_id)

                if lessons:
                    lessons_str = tools.format_lessons_day_for_message(lessons, day_name)
                    parse_send_message(chat_id, lessons_str)
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
        db_manager.remove_user_by_chat_id(chat_id)

        bot.send_message(chat_id, "You removed from DB")

    elif msg == "time":
        bot.send_message(chat_id, tools.get_current_time())

    elif msg == "events":
        events = db_manager.get_events()

        if len(events) == 0:
            bot.send_message(chat_id, "DB Event is clear")

        else:
            answer = "Count: {0}\n\n".format(str(len(events)))

            for event in events:
                answer += event.format_print() + "\n\n"

            bot.send_message(chat_id, answer)

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

            # bot.send_message(message.chat.id, "".format(group_id))
            parse_send_message(message.chat.id, "Lessons {0} add to database".format(group_id))
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

        parse_send_message(constants.admin_log, "<b>New user</b> - {0}".format(user.name_user))
    else:
        groups = tools.sorted_groups(db_manager.get_group_list())
        list_groups = tools.array_to_one_line(groups)
        reply_message = bot.reply_to(message, constants.pick_your_group + "\n\n" + list_groups[:-2], parse_mode="HTML")
        bot.register_next_step_handler(reply_message, process_group_step)


def check_current_time():

    while True:
        week = db_manager.get_current_week()
        day_name = tools.get_current_day_name()
        current_time = tools.get_current_time()

        # print(current_time)

        time_events = db_manager.get_list_time_events()

        for time in time_events:
            if time == current_time:
                events = db_manager.get_event(day_name, week, time)

                if events:
                    for event in events:
                        if not event.is_send and day_name == event.day_name and week == event.week:
                            lessons = db_manager.get_lessons_by_day_name(event.day_name, event.week, event.group_id)
                            parse_send_message(event.chat_id,
                                               tools.format_lessons_day_for_message(lessons, event.day_name))

                            next_day_name = tools.get_next_day_name()

                            next_week = week

                            if not next_day_name:
                                next_day_name = tools.format_name_day(constants.monday)
                                next_week = tools.get_next_week(week)

                            next_lessons = db_manager.get_lessons_by_day_name(next_day_name, next_week, event.group_id)

                            lesson_time_start = tools.format_time_for_event(next_lessons[0].time_start)
                            event.set_send_time(tools.format_time_for_start_event(lesson_time_start))
                            event.set_week(next_week)
                            event.set_day_name(next_day_name)

                            db_manager.update_event(event)


def main():
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as ex:
        print(str(ex))
        bot.send_message(constants.admin_chat_id, str(ex))
        bot.send_message(constants.admin_log, str(ex))

# bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    check_time_thread = threading.Thread(target=check_current_time, daemon=True)
    check_time_thread.start()

    # bot.send_message(constants.admin_chat_id, "Bot is run")
    # bot.send_message(constants.admin_log, "Bot is run")
    main()

