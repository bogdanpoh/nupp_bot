import xlrd
import constants
from model.lesson import Lesson
from excel import excel_tools


def format_index_lesson(time, markup=False, is_covid=False):
    if time == '8.30' or time == '8:30':
        if markup:
            return "\U00000031"
        else:
            return 1
    elif time == '10.00' or time == '10:00':
        if markup:
            return "\U00000032"
        else:
            return 2
    elif time == '11.50' or time == '11:50':
        if markup:
            return "\U00000033"
        else:
            return 3
    elif time == '13.20' or time == '13:20':
        if markup:
            return "\U00000034"
        else:
            return 4
    elif time == '14.50' or time == '14:50':
        if markup:
            return "\U00000035"
        else:
            return 5
    elif time == '16.20' or time == '16:20':
        if markup:
            return "\U00000036"
        else:
            return 6
    elif is_covid:
        if time == '11.30' or time == '11:30':
            if markup:
                return "\U00000033"
            else:
                return 3

        elif time == '13.30' or time == '13:30':
            if markup:
                return "\U00000034"
            else:
                return 4
        elif time == '15.00' or time == '15:00':
            if markup:
                return "\U00000035"
            else:
                return 5
        elif time == '16.30' or time == '16:30':
            if markup:
                return "\U00000036"
            else:
                return 6

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


def format_start_time(time):
    return time.split("-")[0]


def format_end_time(time):
    return time.split("-")[-1]


def remove_digit(data):
    result = []
    for el in data:
        if type(el) != float:
            if len(el) > 5 and len(el) > 4:
                result.append(el)

    return result

def read_lessons(path):
    row = None
    day_name = None
    time_start = None
    time_end = None
    group_id = None
    week = None
    info = None
    clear_data = []
    enter_help = None

    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    data = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]

    for el in data:
        clear_data.append(excel_tools.remove_repetition(el))

    group_name = clear_data[0][-1]

    if not group_name:
        group_name = clear_data[1][-1]
        if not group_name:
            group_name = clear_data[1][-2]
            if not group_name:
                group_name = clear_data[0][-1]

    group_id = excel_tools.format_group_id(group_name)
    lessons = []

    for data in clear_data:
        empty_element = excel_tools.remove_empty_element_in_array(data)
        clear_element = remove_digit(empty_element)

        if clear_element:
            first_element = clear_element[0]
            last_element = clear_element[-1]

            if len(clear_element) > 3 and len(clear_element[-2]) != 9 and len(clear_element[-2]) != 11:
                last_element = str(str(clear_element[-2]) + ", " + str(clear_element[-1]))
            else:
                last_element = str(clear_element[-1])

            count_last_element = len(last_element)

            if first_element == constants.first_week_name or\
                    first_element == constants.first_week_name_alternative or\
                    first_element == constants.first_week_name.upper() or\
                    first_element == constants.first_week_name_alternative.upper():
                week = constants.first_week

            if first_element == constants.second_week or\
                    first_element == constants.second_week_name_alternative or\
                    first_element == constants.second_week_name_alternative_1 or\
                    constants.first_week == constants.test_week_name or\
                    first_element == constants.second_week_name.upper() or\
                    first_element == constants.second_week_name_alternative.upper() or\
                    first_element == constants.second_week_name_alternative_1.upper():
                week = constants.second_week

            if first_element == constants.monday or first_element == constants.tuesday \
                    or first_element == constants.wednesday or first_element == constants.thursday or first_element == constants.friday:
                day_name = format_name_day(first_element)

            if count_last_element > 9 and count_last_element > 11:
                if len(last_element) > 9 and len(last_element) > 12 or last_element.lower()[0] == "ф":
                    info = excel_tools.remove_repetition_in_str(last_element)
                else:
                    info = None

                if last_element.lower().find("Використовуйте".lower()) == 0:
                    info = None

                time = ""

                if len(first_element) <= 12:
                    if len(clear_element) == 3:
                        time = str(clear_element[1]).replace(" ", "")
                    else:
                        time = str(first_element).replace(" ", "")

                if time:
                    time_start = format_start_time(str(time)).replace(" ", "")
                    time_end = format_end_time(str(time)).replace(" ", "")

                row = format_index_lesson(time_start, is_covid=True)

                if week is None:
                    week = constants.second_week

                    if group_id is None:
                        group_id = excel_tools.format_group_id(clear_data[0][-1])

                lesson = Lesson(row, day_name, time_start, time_end, group_id, week, info)
                lessons.append(lesson)

    return lessons
