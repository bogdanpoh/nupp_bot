import telebot
import constants
from database.user import User
from database import db_manager

bot = telebot.TeleBot(constants.token)

# if not exists tables, create it
db_manager.create_table_users()


def get_user_info(message):

    name = ""

    username = message.chat.username
    user_id = message.from_user.id

    if username:
        name = username
    else:
        name = "user_" + user_id

    return User(name_user=name, chat_id=user_id)


# required keyboard
def get_required_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(constants.keyboard_setting)
    markup.add(constants.keyboard_current_lessons, constants.keyboard_tomorrow_lessons)
    markup.add(constants.keyboard_week_lessons)

    return markup


def parse_send_message(chat_id, text, keyboard=None):

    message = None

    if keyboard:
        message = bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=keyboard)
    else:
        message = bot.send_message(chat_id, text, parse_mode="HTML")

    return message


# commands handler
@bot.message_handler(commands=["start", "settings", "about", "get_users", "drop_users"])
def commands_handler(message):

    msg = message.text
    chat_id = message.chat.id

    if msg == "/start":

        users = db_manager.get_users()

        for user in users:
            if str(chat_id) == user.chat_id:
                bot.send_message(chat_id, constants.you_is_register, reply_markup=get_required_keyboard())
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


@bot.message_handler(content_types=["text"])
def message_handler(message):

    msg = message.text
    chat_id = message.chat.id

    if msg == constants.keyboard_setting:
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == 'db':

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


def process_group_step(message):

    group_id = str(message.text)

    user = get_user_info(message)

    user.group_id = group_id

    db_manager.add_user(user)

    bot.send_message(message.chat.id, constants.thanks_for_a_registration, reply_markup=get_required_keyboard())


bot.polling(none_stop=True, interval=0)
