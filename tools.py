import constants
import xlrd
from itertools import groupby
from database.lesson import Lesson
from database.user import User
from database.event import Event
from database.teacher import Teacher
import datetime
from datetime import timedelta
import telebot

time_delta = timedelta(minutes=20)


def to_bold(string):
    return "<b>" + str(string) + "</b>"


def is_today_register_time_for_event(time, lesson_time):
    current_time = datetime.datetime.strptime(time, constants.format_time)
    lesson_start_time = datetime.datetime.strptime(lesson_time, constants.format_time)

    result = str(lesson_start_time - current_time)

    if len(result.split(",")) > 1:
        return True
    else:
        return False


def format_time_for_start_event(time):

    start_time = datetime.datetime.strptime(time, constants.format_time) - time_delta

    start_time_str = str(start_time).split(" ")[-1]

    full_start_time_str = start_time_str.split(":")

    return full_start_time_str[0] + ":" + full_start_time_str[1]


def format_time_for_event(time):
    time_str = str(time).replace(".", ":")

    if len(time_str.split(":")[0]) < 2:
        return "0" + time_str
    else:
        return time_str


def format_lessons_day_for_message(lessons, day_name, is_teacher_format=False, lang=constants.lang_ua):

    print(lang)

    lessons_str = ""

    if is_teacher_format:
        for lesson in lessons:
            lessons_str += lesson.format_message(is_teacher_format=True) + "\n"
    else:
        for lesson in lessons:
            lessons_str += lesson.format_message() + "\n"

    if lang == constants.lang_en:
        return str(day_name).capitalize() + "\n\n" + lessons_str

    return str(format_name_day(day_name) + "\n\n" + lessons_str)


def get_next_week(current_week):

    if current_week == constants.first_week:
        return constants.second_week
    else:
        return constants.first_week


def get_current_time():
    now = datetime.datetime.now() - datetime.timedelta(minutes=7)

    current_time = now.strftime("%H:%M")

    return current_time


def get_lessons_row(lesson):
    return lesson.row


def sorted_lessons(lessons):
    lessons.sort(key=get_lessons_row)

    return lessons


def sorted_groups(groups):
    return sorted(groups)


def array_to_one_line(data):
    line = ""

    for el in data:
        line += str(el) + ", "

    return line


def search_teacher_in_str(lesson, teacher_name):
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

    if new_str == teacher_name:
        return lesson


def get_lessons_days(lessons):

    day_names = []

    for lesson in lessons:
        day_names.append(lesson.day_name)

    return set(day_names)


def format_lessons_week_for_message(lessons, is_format_teacher=False, lang=constants.lang_ua):

    answer = ""
    day_name = ""

    if is_format_teacher:

        days = get_lessons_days(lessons)
        sorted_days = sorted(days, key=constants.const_sorted_days.index)

        for day in sorted_days:
            for lesson in lessons:
                if day == lesson.day_name:
                    if not day_name:
                        answer += format_name_day(day) + "\n" + lesson.format_message(is_teacher_format=True) + "\n"
                        day_name = day
                    else:
                        answer += lesson.format_message(is_teacher_format=True) + "\n"
            answer += "\n"
            day_name = ""

    else:
        for lesson in lessons:
            if not day_name:
                day_name = lesson.day_name

                if lang == constants.lang_en:
                    answer += str(day_name).capitalize() + "\n"
                else:
                    answer += format_name_day(day_name) + "\n"

            if day_name:
                if day_name == lesson.day_name:
                    answer += lesson.format_message() + "\n"

                else:
                    day_name = lesson.day_name

                    if lang == constants.lang_en:
                        answer += "\n" + str(day_name).capitalize() + "\n" + lesson.format_message() + "\n"
                    else:
                        answer += "\n" + format_name_day(day_name) + "\n" + lesson.format_message() + "\n"

    return answer


def data_to_str(data, is_class=False, is_message=False):

    answer = ""

    for el in data:
        try:
            if is_class:
                answer += str(el.format_print() + "\n\n")
            elif is_message:
                answer += str(el.format_message() + "\n\n")
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
        elif to_class == "teacher":
            list_answer.append(Teacher(data=el))
        elif to_class == "event":
            list_answer.append(Event(data=el))

    return list_answer


def get_current_day_and_month():
    return datetime.datetime.now().strftime("%d.%m")


def get_current_date():
    return datetime.datetime.now().strftime("%d.%m.%Y")


def get_current_day_name():
    now = datetime.datetime.now()

    day_name = now.strftime("%A").casefold()

    if day_name == "sunday" or day_name == "saturday":
        return None

    return day_name


def get_next_day_name():

    next_day = datetime.datetime.now() + datetime.timedelta(days=1)

    day_name = next_day.strftime("%A").casefold()

    if day_name == "sunday" or day_name == "saturday":
        return None

    return day_name


def download_file(path, file):
    with open(path, "wb") as new_file:
        new_file.write(file)


def write_to_file(path, text):
    with open(path, "w") as file:
        file.write(text)


def get_required_keyboard(lang=None):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    if lang == constants.lang_en:
        markup.add(constants.keyboard_setting_en)
        markup.add(constants.keyboard_current_lessons_en, constants.keyboard_tomorrow_lessons_en)
        markup.add(constants.keyboard_week_lessons_en)
    else:
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

        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        if first_name:
            name += first_name + " "

        if last_name:
            name += last_name

        if not name:
            name = "user_" + str(user_id)
        else:
            name += "_" + str(user_id)

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
    elif name_day == "monday":
        return constants.monday
    elif name_day == "tuesday":
        return constants.tuesday
    elif name_day == "wednesday":
        return constants.wednesday
    elif name_day == "thursday":
        return constants.thursday
    elif name_day == "friday":
        return constants.friday


def format_index_lesson(time, markup=False, is_covid=False):

    if time == '8.30':
        if markup:
            return "\U00000031"
        else:
            return 1
    elif time == '10.00':
        if markup:
            return "\U00000032"
        else:
            return 2
    elif time == '11.50':
        if markup:
            return "\U00000033"
        else:
            return 3
    elif time == '13.20':
        if markup:
            return "\U00000034"
        else:
            return 4
    elif time == '14.50':
        if markup:
            return "\U00000035"
        else:
            return 5
    elif time == '16.20':
        if markup:
            return "\U00000036"
        else:
            return 6
    elif is_covid:
        if time == "11.30":
            if markup:
                return "\U00000033"
            else:
                return 3

        elif time == "13.30":
            if markup:
                return "\U00000034"
            else:
                return 4
        elif time == "15.00":
            if markup:
                return "\U00000035"
            else:
                return 5
        elif time == "16:30":
            if markup:
                return "\U00000036"
            else:
                return 6


def format_start_time(time):
    return time.split("-")[0]


def format_end_time(time):
    return time.split("-")[-1]


def format_group_id(group_name):

    group_id = (remove_repetition_in_str(group_name)).replace(" ", "").replace(".", "")

    if len(str(group_id).split("-")) > 1:
        group = str(group_id).split("-")

        group_id = group[0] + group[-1]

    return group_id

def format_enter_help(lessons):

    edit_lessons = []

    word = "Використовуйте".lower()

    lection = "Л".lower()
    practical = "пр."
    lab = "лаб"

    enter_help = None
    enter_help_day_name = None

    for lesson in lessons:
        # lection_index = lesson.info.lower().find(lection)
        #
        # if lection_index >= 0 and lesson.info[lection_index + 1] != "а":
        #
        #     new_info = lesson.info[2: -1]
        #     lesson.info = "<b>Лекція</b> " + new_info
        #
        # elif lesson.info.find(practical) >= 0:
        #     new_info = lesson.info[4: -1]
        #     lesson.info = "<b>Практика</b> " + new_info
        #
        # elif lesson.info.find(lab) >= 0:
        #     new_info = lesson.info[4: -1]
        #     lesson.info = "<b>Лабораторна робота</b> " + new_info

        if lesson.info.lower().find(word) >= 0:
            enter_help = lesson.info.split(",")[-1]
            enter_help_day_name = lesson.day_name

        if enter_help_day_name:
            if lesson.day_name == enter_help_day_name and lesson.info.lower().find(word) < 0:
                lesson.info += ", " + enter_help

            if lesson.day_name != enter_help_day_name:
                enter_help = None

        edit_lessons.append(lesson)

    return edit_lessons


def read_lessons(path):
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

    enter_help = None

    # group id
    group_id = ""

    for el in data:
        clear_data.append(remove_repetition(el))

    group_name = clear_data[1][-1]

    if not group_name:
        group_name = clear_data[1][-2]

    group_id = format_group_id(group_name)

    lessons = []

    for data in clear_data:

        clear_element = remove_empty_element(data)

        if clear_element:
            first_element = clear_element[0]

            # print(clear_element)

            if len(clear_element) > 3 and len(clear_element[-2]) != 9 and len(clear_element[-2]) != 11:
                last_element = str(clear_element[-2] + ", " + clear_element[-1])
            else:
                last_element = str(clear_element[-1])

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

            if last_element.lower().find("Використовуйте".lower()) >= 0:
                enter_help = last_element

            if count_last_element > 9 and count_last_element > 11 and len(clear_element) > 2:

                time = str(clear_element[1])
                # print(last_element)

                for element in clear_element:
                    if len(str(element)) == 9 or len(str(element)) == 11:
                        time = str(element)

                # info = last_element
                info = remove_repetition_in_str(last_element)

                defis = 0

                for symbol in time:
                    if symbol == "-":
                        defis += 1

                if defis == 2:
                    time_list = list(time)

                    if len(time) == 9:
                        time_list[1] = "."
                    elif len(time) == 11:
                        time_list[2] = "."

                    time = "".join(time_list)

                if time:
                    time_start = format_start_time(str(time)).replace(" ", "")
                    time_end = format_end_time(str(time)).replace(" ", "")

                else:
                    time_start = "00.00"
                    time_end = "00.00"

                row = format_index_lesson(time_start, is_covid=True)

                if week is None:
                    week = constants.first_week

                lesson = Lesson(row, day_name, time_start, time_end, group_id, week, info)

                if row is not None and day_name is not None:
                    if enter_help:
                        lesson.info += ", {}".format(remove_repetition_in_str(enter_help))

                    lessons.append(lesson)
                    enter_help = ""

                # else:
                #     print(lesson.format_print())

    return format_enter_help(lessons)

    # wb = xlrd.open_workbook(path)
    # sheet = wb.sheet_by_index(0)
    # sheet.cell_value(0, 0)
    #
    # data = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]
    #
    # row = None
    # day_name = None
    # time_start = None
    # time_end = None
    # group_id = None
    # week = None
    # info = None
    #
    # first_week = "І ТИЖДЕНЬ"
    # second_week = "І I ТИЖДЕНЬ"
    # second_week_a = "ІI ТИЖДЕНЬ"
    # second_week_a_a = "ІІ ТИЖДЕНЬ"
    #
    # clear_data = []
    #
    # #group id
    # group_id = ""
    #
    # for el in data:
    #     clear_data.append(remove_repetition(el))
    #
    # group_name = clear_data[1][-1]
    #
    # if not group_name:
    #     group_name = clear_data[1][-2]
    #
    # group_id = format_group_id(group_name)
    #
    # lessons = []
    #
    # for data in clear_data:
    #
    #     clear_element = remove_empty_element(data)
    #
    #     if clear_element:
    #         first_element = clear_element[0]
    #         last_element = str(clear_element[-1])
    #
    #         count_last_element = len(last_element)
    #
    #         if first_element == first_week:
    #             week = constants.first_week
    #             # print(week)
    #
    #         elif first_element == second_week or first_element == second_week_a or first_element == second_week_a_a:
    #             week = constants.second_week
    #             # print(week)
    #
    #         if first_element == constants.monday or first_element == constants.tuesday \
    #                 or first_element == constants.wednesday or first_element == constants.thursday or first_element == constants.friday:
    #             day_name = format_name_day(first_element)
    #
    #             # print(day_name)
    #
    #         if count_last_element > 9 and count_last_element > 11:
    #
    #             time = None
    #
    #             if len(clear_element) > 2:
    #                 time = clear_element[-2]
    #
    #             # info = last_element
    #             info = remove_repetition_in_str(last_element)
    #
    #             if time:
    #                 time_start = format_start_time(str(time))
    #                 time_end = format_end_time(str(time))
    #             else:
    #                 time_start = "00:00"
    #                 time_end = "00:00"
    #
    #             row = format_index_lesson(time_start, is_covid=True)
    #
    #             if week is None:
    #                 week = constants.first_week
    #
    #             lesson = Lesson(row, day_name, time_start, time_end, group_id, week, info)
    #
    #             if row is not None and day_name is not None:
    #                 lessons.append(lesson)
    #
    # return lessons
