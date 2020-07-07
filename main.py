import telebot
import constants

bot = telebot.TeleBot(constants.token)


def get_user_info(message):

    chat_id = message.chat.id
    info = ""

    bot.send_message(chat_id, message.chat)

    last_name = message.chat.last_name
    first_name = message.chat.first_name
    username = message.chat.username
    user_id = message.from_user.id

    if last_name:
        print(last_name)

    if first_name:
        print(first_name)

    if username:
        print(username)

    if user_id:
        print(user_id)

    return info

# required keyboard
def get_required_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(constants.keyboard_setting)
    markup.add(constants.keyboard_current_lessons, constants.keyboard_tomorrow_lessons)
    markup.add(constants.keyboard_week_lessons)

    return markup


def parse_send_message(chat_id, text, keyboard=get_required_keyboard()):

    if keyboard:
        bot.send_message(chat_id, text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, parse_mode="HTML")


# commands handler
@bot.message_handler(commands=["start", "settings", "about"])
def commands_handler(message):

    msg = message.text
    chat_id = message.chat.id

    if msg == '/start':
        parse_send_message(chat_id, constants.start_answer)

    elif msg == '/settings':
        parse_send_message(chat_id, constants.settings_answer)

    elif msg == '/about':
        parse_send_message(chat_id, constants.about_anser)


@bot.message_handler(content_types=["text"])
def message_handler(message):

    msg = message.text
    chat_id = message.chat.id

    if msg == constants.keyboard_setting:
        parse_send_message(chat_id, constants.settings_answer)

    else:

        get_user_info(message)

        # parse_send_message(chat_id, constants.not_found_answer)


bot.polling(none_stop=True, interval=0)
