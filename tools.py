import constants

from database.lesson import Lesson
from database.user import User
from database.event import Event
from database.teacher import Teacher
from database.faculty import Faculty
from database.session import Session
import datetime
from datetime import timedelta
import telebot

from excel import read_lessons

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
    lessons_str = ""

    if is_teacher_format:
        for lesson in lessons:
            lessons_str += lesson.format_message(is_teacher_format=True) + "\n"
    else:
        for lesson in lessons:
            lessons_str += lesson.format_message() + "\n"

    if lang == constants.lang_en:
        return str(day_name).capitalize() + "\n\n" + lessons_str

    return str(read_lessons.format_name_day(day_name) + "\n\n" + lessons_str)


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
                        answer += read_lessons.format_name_day(day) + "\n" + lesson.format_message(is_teacher_format=True) + "\n"
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
                    answer += read_lessons.format_name_day(day_name) + "\n"

            if day_name:
                if day_name == lesson.day_name:
                    answer += lesson.format_message() + "\n"

                else:
                    day_name = lesson.day_name

                    if lang == constants.lang_en:
                        answer += "\n" + str(day_name).capitalize() + "\n" + lesson.format_message() + "\n"
                    else:
                        answer += "\n" + read_lessons.format_name_day(day_name) + "\n" + lesson.format_message() + "\n"

    return answer


def data_to_str(data, is_class=False, is_message=False, is_iteration=False):

    answer = ""

    single_enter = "\n"
    double_enter = "\n\n"

    for el in data:
        try:
            if is_class:
                answer += str(el.format_print() + double_enter)
            elif is_message:
                if is_iteration:

                    enter = ""

                    index = data.index(el) % 2

                    if index == 0:
                        enter = single_enter
                    else:
                        enter = double_enter

                    answer += str(el.format_message() + enter)
                else:
                    answer += str(el.format_message() + double_enter)
            else:
                answer += str(el) + double_enter
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
        elif to_class == "faculty":
            list_answer.append(Faculty(data=el))
        elif to_class == "session":
            list_answer.append(Session(data=el))

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
        markup.add(constants.keyboard_last_week_en, constants.keyboard_week_lessons_en)
    else:
        markup.add(constants.keyboard_setting)
        markup.add(constants.keyboard_current_lessons, constants.keyboard_tomorrow_lessons)
        markup.add(constants.keyboard_last_week, constants.keyboard_week_lessons)

    return markup


def get_user_info_from_message(message):

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




def read_faculty(path):
    wb = xlrd.open_workbook(path)

    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    data = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]

    clear_data = []

    faculties = []

    for el in data:
        for index in el:
            if index:
                try:
                    if int(index):
                        pass
                except:
                    new_index = read_lessons.remove_repetition_in_str(index)
                    if len(read_lessons.format_group_id(new_index)) > 14:
                        clear_data.append(new_index)
                    else:
                        clear_data.append(read_lessons.format_group_id(new_index))

    faculty = ""

    for el in clear_data[5:]:
        if len(el) > 12:
            faculty = str(el)
        elif faculty:
            faculties.append(Faculty(faculty, str(el)))

    return faculties


