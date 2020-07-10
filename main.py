import telebot
import constants
from database.user import User
from database import db_manager
import tools
import os

bot = telebot.TeleBot(constants.token)

# if not exists tables, create it
db_manager.create_table_users()
db_manager.create_table_lessons()


def parse_send_message(chat_id, text, keyboard=None):

    message = None

    if keyboard:
        message = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = bot.send_message(chat_id, text, parse_mode="HTML")

    return message


# commands handler
@bot.message_handler(commands=["start", "settings", "about", "get_users", "drop_users", "add_lessons"])
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

        reply_message = bot.reply_to(answer, constants.pick_your_group)

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
            answer = "Count users " + str(count_users)

        bot.send_message(chat_id, answer)

    elif msg == "/drop_users":
        db_manager.remove_users()

        bot.send_message(chat_id, "Table Users cleared")

    elif msg == "/add_lessons":
        tools.read_excel()


@bot.message_handler(content_types=["text"])
def message_handler(message):

    msg = message.text
    chat_id = message.chat.id

    if msg == constants.keyboard_setting:
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == "db":

        users = db_manager.get_users()

        list = ""

        if users:
            for user in users:
                list += user.format_print() + "\n"

            bot.send_message(chat_id, list)

        else:
            bot.send_message(chat_id, "Table users is empty")

    else:
        parse_send_message(chat_id, constants.not_found_answer)


# callback functions
def process_group_step(message):

    group_id = str(message.text)

    user = tools.get_user_info(message)

    user.group_id = group_id

    db_manager.add_user(user)

    bot.send_message(message.chat.id, constants.thanks_for_a_registration, reply_markup=tools.get_required_keyboard())


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

        with open(path+"."+type_file)



bot.polling(none_stop=True, interval=0)
