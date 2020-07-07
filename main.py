import telebot
import constants

bot = telebot.TeleBot(constants.token)


def parse_send_message(chat_id, text):
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


bot.polling(none_stop=True, interval=0)