import telebot
import constants
import os
import tools
import config
from database import db_manager
import time

bot = telebot.TeleBot(config.admin_token)

admin_commands = ["start",
                  "drop_table_users", "drop_session",
                  "remove_lessons", "remove_users", "remove_group", "session_remove_by_id",
                  "rename_group_id",
                  "get_db_bot", "send_all_message", "change_week"
                  ]

db_path = os.path.join("..", constants.db_name)


def is_admin(message):
    chat_id = message.chat.id

    if chat_id == constants.admin_chat_id:
        return True
    else:
        return False


@bot.message_handler(commands=admin_commands)
def commands_handler(message):
    chat_id = message.chat.id
    msg = str(message.text)

    if is_admin(message):

        if msg == "/start":
            bot.send_message(chat_id, "Hi, admin")

        elif msg == "/send_all_message":

            reply_message = bot.send_message(chat_id, "Напешіть повідомлення:")

            bot.register_next_step_handler(reply_message, process_send_messages)

        elif msg == "/remove_lessons":
            db_manager.remove_lessons(db_path)

            lessons = db_manager.get_lessons(db_path)

            if not lessons:
                bot.send_message(chat_id, "Table {0} is cleared".format(constants.table_lessons))

        elif msg == "/remove_users":
            db_manager.remove_users(db_path)

            users = db_manager.get_users(db_path)

            if len(users) == 0:
                bot.send_message(chat_id, "Table {0} cleared".format(constants.table_users))

        elif msg == "/rename_group_id":
            reply_message = bot.send_message(chat_id, "Enter group_id and new group_id (101еМ, 101ЕМ):")
            bot.register_next_step_handler(reply_message, process_rename_group_id)

        elif msg == "/remove_group":
            reply_message = bot.send_message(chat_id, "Enter group_id:")

            bot.register_next_step_handler(reply_message, process_remove_group)

        elif msg == "/get_db_bot":
            db_file = open(db_path, "rb")
            bot.send_document(chat_id, db_file)

        elif msg == "/drop_table_users":
            db_manager.drop_table(constants.table_users, db_path)
            bot.send_message(chat_id, "Table {} is drop".format(constants.table_users))

        elif msg == "/drop_session":
            db_manager.drop_session(db_path)

            count_session = len(db_manager.get_sessions(db_path))

            if count_session == 0:
                bot.send_message(chat_id, "Table {} is clead".format(constants.table_session))

        elif msg == "/change_week":
            db_manager.change_week(db_path)
            current_week = db_manager.get_current_week(db_path)
            bot.send_message(chat_id, current_week)

        elif msg == "/session_remove_by_id":
            reply_message = bot.send_message(chat_id, "Enter group id: ")
            bot.register_next_step_handler(reply_message, process_remove_session_by_group_id)
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

            sessions = db_manager.get_sessions(db_path)

            if len(sessions) == 0:
                bot.send_message(chat_id, "Table {} is clear".format(constants.table_session))

            for session in sessions:
                print(session.format_print())


    else:
        bot.send_message(chat_id, "Sorry, you is not admin")


# process
def process_send_messages(message):
    users = db_manager.get_users(db_path)

    msg = str(message.text)

    for user in users:

        time.sleep(5)

        answer = constants.warning_en if user.language == constants.lang_en + "\n\n" + msg else constants.warning + "\n\n" + msg

        log = "Send to {}".format(user.name_user)

        try:
            bot.send_message(user.chat_id, answer, parse_mode="HTML", reply_markup=tools.get_required_keyboard(user.language))
            print(log)

        except:
            log = "Error in send message to user {} \n id: {} \n Remove user from database".format(user.name_user, user.chat_id)
            db_manager.remove_user_by_chat_id(user.chat_id, db_path)
            print(log)

    bot.send_message(message.chat.id, "All users received the message")


def process_rename_group_id(message):
    group_id = str(message.text).replace(" ", "").split(",")

    if db_manager.is_group(group_id[0], db_path):
        bot.send_message(message.chat.id, "this is correct group_id")
        db_manager.rename_group_id(group_id[0], group_id[-1], db_path)
    else:
        bot.send_message(message.chat.id, "this is dont correct group_id")

def process_remove_group(message):
    group_id = str(message.text)

    if db_manager.is_group(group_id, db_path):

        try:
            db_manager.remove_group(group_id, db_path)
            bot.send_message(message.chat.id, "Remove {} success".format(group_id))

        except:
            bot.send_message(message.chat.id, "Error remove group {}".format(group_id))

    else:
        bot.send_message(message.chat.id, "Dont found group: {}".format(group_id))

def process_remove_session_by_group_id(message):
    group_id = str(message.text)
    chat_id = message.chat.id

    if db_manager.is_group_on_session(group_id, db_path):
        db_manager.remove_session_by_group_id(group_id, db_path)

        if not db_manager.is_group_on_session(group_id, db_path):
            bot.send_message(chat_id, "Group {} is remove".format(group_id))

    else:
        bot.send_message(chat_id, "Group {} is don't found".format(group_id))

def main():
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as ex:
        print(str(ex))
        bot.send_message(constants.admin_chat_id, "Admin bot is off..")


main()
