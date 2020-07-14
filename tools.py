import constants
import xlrd
from itertools import groupby
from database.lesson import Lesson
from database.user import User
import datetime
import telebot


def search_teacher_in_str(lesson, teacher_name):
    # string = "John Appleseed U.S. 07.09"

    end_index = len(str(lesson.info))

    index = lesson.info.find(teacher_name)

    if index < 0:
        return None

    new_str = ""

    dot_counter = 2

    while index < end_index:

        if dot_counter > 0:
            new_str += lesson.info[index]

        if lesson.info[index] == ".":
            dot_counter -= 1

        index += 1

    # print(teacher_name)
    # print(new_str)
    if new_str == teacher_name:
        return lesson


def data_to_str(data, is_class=False):

    answer = ""

    for el in data:
        try:
            if is_class:
                answer += str(el.format_print() + "\n\n")
            else:
                answer += str(el) + "\n\n"
        except Exception as ex:
            print("Error in func data_to_list_str", ex)

    return answer


def data_to_list_class(data, to_class):

    list_answer = []

    for el in data:
        if to_class == "user":
            list_answer.append(User(data=el))
        elif to_class == "lesson":
            list_answer.append(Lesson(data=el))

    return list_answer


def get_current_day_name():
    now = datetime.datetime.now()

    day_name = now.strftime("%A").casefold()

    return day_name


def get_next_day_name():

    next_day = datetime.datetime.now() + datetime.timedelta(days=1)

    day_name = next_day.strftime("%A").casefold()

    return day_name


def download_file(path, file):
    with open(path, "wb") as new_file:
        new_file.write(file)


# required keyboard
def get_required_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(constants.keyboard_setting)
    markup.add(constants.keyboard_current_lessons, constants.keyboard_tomorrow_lessons)
    markup.add(constants.keyboard_week_lessons)

    return markup


def get_user_info(message):

    name = ""

    username = message.chat.username
    user_id = message.from_user.id

    if username:
        name = username
    else:
        name = "user_" + user_id

    return User(name_user=name, chat_id=user_id)


def remove_repetition_in_str(string):
    return " ".join(string.split())


def remove_empty_element(data):
    result = []
    for el in data:
        is_empty_str = str(el).replace(" ", "")
        if el and is_empty_str:
            result.append(el)

    return list(result)


def remove_repetition(data):
    return [el for el, _ in groupby(data)]


def format_name_day(name_day):
    if name_day == constants.monday:
        return "monday"
    elif name_day == constants.tuesday:
        return "tuesday"
    elif name_day == constants.wednesday:
        return "wednesday"
    elif name_day == constants.thursday:
        return "thursday"
    elif name_day == constants.friday:
        return "friday"


def format_index_lesson(time):
    if time == '8.30':
        return 1
    elif time == '10.00':
        return 2
    elif time == '11.50':
        return 3
    elif time == '13.20':
        return 4
    elif time == '14.50':
        return 5
    elif time == '16.20':
        return 6


def format_start_time(time):
    return time.split("-")[0]


def format_end_time(time):
    return time.split("-")[-1]


def read_excel(path):
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    data = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]

    row = None
    day_name = None
    time_start = None
    time_end = None
    group_id = None
    week = None
    info = None

    first_week = "І ТИЖДЕНЬ"
    second_week = "І I ТИЖДЕНЬ"
    second_week_a = "ІI ТИЖДЕНЬ"
    second_week_a_a = "ІІ ТИЖДЕНЬ"

    clear_data = []

    for el in data:
        clear_data.append(remove_repetition(el))

    group_id = clear_data[1][-1]

    if not group_id:
        group_id = clear_data[1][-2]

    lessons = []

    for data in clear_data:

        clear_element = remove_empty_element(data)

        # print(clear_element)

        if clear_element:
            first_element = clear_element[0]
            last_element = clear_element[-1]
            count_last_element = len(last_element)

            if first_element == first_week:
                week = constants.first_week
                # print(week)

            elif first_element == second_week or first_element == second_week_a or first_element == second_week_a_a:
                week = constants.second_week
                # print(week)

            if first_element == constants.monday or first_element == constants.tuesday \
                    or first_element == constants.wednesday or first_element == constants.thursday or first_element == constants.friday:
                day_name = format_name_day(first_element)

                # print(day_name)

            if count_last_element > 9 and count_last_element > 11:

                if len(clear_element) > 2:
                    time = clear_element[-2]

                # info = last_element
                info = remove_repetition_in_str(last_element)

                time_start = format_start_time(str(time))
                time_end = format_end_time(str(time))

                row = format_index_lesson(time_start)
                lesson = Lesson(row, day_name, time_start, time_end, group_id, week, info)
                # print(lesson.format_print())
                lessons.append(lesson)

    return lessons