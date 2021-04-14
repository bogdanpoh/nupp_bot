import telebot
import constants
import config
import tools
from managers import db_manager
from managers.file_manager import FileManager
from excel import read_lessons
from excel import read_session

bot = telebot.TeleBot(config.admin_token)

admin_commands = [
    "start",
    "drop_table_users", "drop_session",
    "remove_lessons", "remove_users", "remove_group", "session_remove_by_id",
    "rename_group_id",
    "get_db_bot", "change_week",
    "remove_lessons_by_id"
]


def is_admin(message):
    return True if message.chat.id == constants.admin_chat_id else False


@bot.message_handler(commands=admin_commands)
def commands_handler(message):
    chat_id = message.chat.id
    msg = str(message.text)

    if is_admin(message):
        if msg == "/start":
            bot.send_message(chat_id, "Hi, admin")

        elif msg == "/remove_lessons":
            db_manager.remove_lessons()
            lessons = db_manager.get_lessons()
            if not lessons:
                bot.send_message(chat_id, "Table {0} is cleared".format(constants.table_lessons))

        elif msg == "/remove_users":
            db_manager.remove_users()
            users = db_manager.get_users()
            if len(users) == 0:
                bot.send_message(chat_id, "Table {0} cleared".format(constants.table_users))

        elif msg == "/rename_group_id":
            reply_message = bot.send_message(chat_id, "Enter group_id and new group_id (101еМ, 101ЕМ):")
            bot.register_next_step_handler(reply_message, process_rename_group_id)

        elif msg == "/remove_group":
            reply_message = bot.send_message(chat_id, "Enter group_id:")
            bot.register_next_step_handler(reply_message, process_remove_group)

        elif msg == "/get_db_bot":
            db_file = open(constants.db_name, "rb")
            bot.send_document(chat_id, db_file)

        elif msg == "/drop_table_users":
            db_manager.drop_table(constants.table_users)
            bot.send_message(chat_id, "Table {} is drop".format(constants.table_users))

        elif msg == "/drop_session":
            db_manager.drop_session()
            count_session = len(db_manager.get_sessions())

            if count_session == 0:
                bot.send_message(chat_id, "Table {} is clead".format(constants.table_session))

        elif msg == "/change_week":
            db_manager.change_week()
            current_week = db_manager.get_current_week()
            bot.send_message(chat_id, current_week)

        elif msg == "/session_remove_by_id":
            reply_message = bot.send_message(chat_id, "Enter group id: ")
            bot.register_next_step_handler(reply_message, process_remove_session_by_group_id)

        elif msg == "/remove_lessons_by_id":
            reply_message = bot.send_message(chat_id, "Enter group id: ")
            bot.register_next_step_handler(reply_message, process_remove_lessons_by_course)
    else:
        bot.send_message(chat_id, "Sorry, you is not admin")


@bot.message_handler(content_types=["text"])
def text_handler(message):
    chat_id = message.chat.id
    msg = str(message.text)

    if is_admin(message):
        if msg == "0":
            command_list = ""
            for command in admin_commands:
                command_list += str("/" + command) + "\n\n"

            bot.send_message(chat_id, command_list)

        elif msg == "s":
            sessions = db_manager.get_sessions()
            if len(sessions) == 0:
                bot.send_message(chat_id, "Table {} is clear".format(constants.table_session))
            for session in sessions:
                print(session.format_print())
    else:
        bot.send_message(chat_id, "Sorry, you is not admin")


@bot.message_handler(content_types=["document"])
def file_handler(message):
    answer_succes = "success"
    answer_failed = "failed"
    file_path = FileManager.download_file(bot, message, FileManager.path_for_excel)
    file_first_symbol = message.document.file_name[0]
    type_of_file = None
    answer = "file: {} - ".format(str(message.document.file_name))
    data = ""

    FileManager.if_file_exists_remove(FileManager.path_for_txt)
    FileManager.if_file_exists_remove(FileManager.path_for_excel)

    if file_first_symbol == "s":
        type_of_file = constants.table_session
        sessions = read_session.read_session(file_path)
        count_sessions = len(sessions)
        if sessions:
            for session in sessions:
                data += session.format_print() + "\n"
            if count_sessions > 0:
                answer += answer_succes
        else:
            answer += answer_failed

    elif file_first_symbol == "q":
        type_of_file = constants.table_session
        qualifications = read_session.read_session(file_path)
        count_qualifications = len(qualifications)
        if qualifications:
            for item in qualifications:
                data += item.format_print() + "\n"
            if count_qualifications > 0:
                answer += answer_succes
        else:
            answer += answer_failed
    else:
        type_of_file = constants.table_lessons
        lessons = read_lessons.read_lessons(file_path)
        if lessons:
            weeks = set()
            for lesson in lessons:
                weeks.add(lesson.week)
                data += lesson.format_print() + "\n"
            if len(weeks) == 2:
                answer += answer_succes
        else:
            answer += answer_failed

    if data:
        tools.write_to_file(FileManager.path_for_txt, data)
        with open(FileManager.path_for_txt, "rb") as file:
            bot.send_document(message.chat.id, file)

    bot.send_message(message.chat.id, answer)

    if type_of_file is None:
        bot.send_message(message.chat.id, "don`t found info")

# process
def process_rename_group_id(message):
    group_id = str(message.text).replace(" ", "").split(",")

    if db_manager.is_group(group_id[0]):
        bot.send_message(message.chat.id, "this is correct group_id")
        db_manager.rename_group_id(group_id[0], group_id[-1])
    else:
        bot.send_message(message.chat.id, "this is dont correct group_id")


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


def process_remove_session_by_group_id(message):
    group_id = str(message.text)
    chat_id = message.chat.id

    if db_manager.is_group_on_session(group_id):
        db_manager.remove_session_by_group_id(group_id)
        if not db_manager.is_group_on_session(group_id):
            bot.send_message(chat_id, "Group {} is remove".format(group_id))
    else:
        bot.send_message(chat_id, "Group {} is don't found".format(group_id))


def process_remove_lessons_by_course(message):
    pick_group = message.text
    groups = db_manager.get_group_list()

    for group in groups:
        if pick_group in group:
            try:
                db_manager.remove_lessons_by_group_id(group)
            except Exception as e:
                print("error when remove lesson by course: {}".format(e))


def main():
    try:
        bot.infinity_polling(True)
    except Exception as ex:
        print(str(ex))
        bot.send_message(constants.admin_chat_id, "Admin bot is off..")


main()
