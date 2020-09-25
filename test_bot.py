# import telebot
# import constants
# import os
# import tools
#
# token = "1330494074:AAEnuSDqmiBh04KvsnmSuCnrRA6jdIVXsOs"
#
# bot = telebot.TeleBot(token)
#
#
# @bot.message_handler(commands=["start"])
# def commands_handler(message):
#     chat_id = message.chat.id
#     msg = str(message.text)
#
#     if chat_id == constants.admin_chat_id:
#         if msg == "/start":
#             bot.send_message(chat_id, "Hello world!")
#     else:
#         bot.send_message(chat_id, "Sorry, you is not admin")
#
#
# @bot.message_handler(content_types=["text"])
# def text_handler(message):
#     chat_id = message.chat.id
#     msg = str(message.text)
#
#     if chat_id == constants.admin_chat_id:
#         if msg == "test":
#             bot.send_message(chat_id, "Ok")
#     else:
#         bot.send_message(chat_id, "Sorry, you is not admin")
#
#
# @bot.message_handler(content_types=["document"])
# def read_file_handler(message):
#
#     chat_id = message.chat.id
#
#     path = os.path.join(constants.documents_directory, constants.excel_file)
#
#     if os.path.exists(path):
#         os.remove(path)
#
#     file_info = bot.get_file(message.document.file_id)
#     type_file = str(file_info.file_path).split(".")[-1]
#
#     downloaded_file = bot.download_file(file_info.file_path)
#
#     tools.download_file(path + "." + type_file, downloaded_file)
#
#     file_path = os.path.join(constants.documents_directory,
#                                      constants.excel_file + "." + type_file)
#
#     lessons = tools.read_lessons(file_path)
#
#     if lessons:
#
#         first_week = []
#         second_week = []
#
#         for lesson in lessons:
#             if lesson.week == constants.first_week:
#                 first_week.append(lesson)
#             elif lesson.week == constants.second_week:
#                 second_week.append(lesson)
#
#         answer_first_week = tools.format_lessons_week_for_message(first_week)
#         answer_second_week = tools.format_lessons_week_for_message(second_week)
#
#         if chat_id == constants.admin_chat_id:
#
#             bot.send_message(chat_id, lessons[0].group_id)
#
#             if answer_first_week:
#                 bot.send_message(chat_id, tools.to_bold(constants.first_week) + "\n\n" + answer_first_week, parse_mode="HTML")
#             else:
#                 bot.send_message(chat_id, "{} is not".format(constants.first_week))
#
#             if answer_second_week:
#                 bot.send_message(chat_id, tools.to_bold(constants.second_week) + "\n\n" + answer_second_week, parse_mode="HTML")
#             else:
#                 bot.send_message(chat_id, "{} is not".format(constants.second_week))
#
#
# def main():
#     try:
#         bot.polling(none_stop=True, interval=0)
#     except Exception as ex:
#         print(str(ex))
#         bot.send_message(constants.admin_chat_id, "Test bot is off..")
#
#
# main()


import telebot
import constants
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

token = "1330494074:AAEnuSDqmiBh04KvsnmSuCnrRA6jdIVXsOs"

bot = telebot.TeleBot(token)


def get_number_markup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Get number", request_contact=True))
    return markup


def remove_markup():
    return ReplyKeyboardRemove()


@bot.message_handler(content_types=["contact"])
def contact_handler(message):
    chat_id = message.chat.id

    phone_number = str(message.contact.phone_number)
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    answer = str("Номер телефону +{}".format(phone_number))

    if chat_id:
        answer += "\nChat id: {}".format(chat_id)

    if first_name:
        answer += "\nІм'я: {}".format(first_name)

    if last_name:
        answer += "\nПрізвище: {}".format(last_name)

    if username:
        answer += "\nЮзернейм: @{}".format(username)

    bot.send_message(chat_id, "Дякуємо, очікуйте звінок!)", reply_markup=remove_markup())
    bot.send_message(constants.admin_chat_id, answer)


@bot.message_handler(commands=["start"])
def message_handler(message):
    bot.send_message(message.chat.id, "Hello, take your number", reply_markup=get_number_markup())


bot.polling(none_stop=True, interval=0)
