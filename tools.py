import constants
import xlrd
from itertools import groupby
from database.lesson import Lesson


def format_list(array):
    return list(filter(None, array))


def remove_repetition_in_str(string):
    return "".join(ch for ch, _ in groupby(string))


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


def remove_empty_str(data):
    result = []

    for element in data:
        if element:
            result.append(element)

    return result

def read_excel(path):
    path = "101ТК.xlsx"
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    data = [sheet.row_values(rownum) for rownum in range(sheet.nrows)]

    index = None
    day_name = None
    time_start = None
    time_end = None
    group_id = None
    week = None
    info = None

    first_week = "І ТИЖДЕНЬ"
    second_week = "І I ТИЖДЕНЬ"

    clear_data = []

    for el in data:
        clear_data.append(remove_repetition(el))

    group_id = clear_data[1][-1]
    print(group_id)

    lessons = []

    for data in clear_data:

        first_element = data[0]
        last_element = data[-1]
        count_last_element = len(last_element)

        if first_element == first_week:
            week = "first_week"
            print(week)

        if first_element == second_week:
            week = "last_week"
            print(week)

        if first_element == constants.monday or first_element == constants.tuesday \
                or first_element == constants.wednesday or first_element == constants.thursday or first_element == constants.friday:
            day_name = format_name_day(first_element)

            print(day_name)

        if count_last_element > 9:

            time = data[-2]

            info = remove_repetition_in_str(last_element)

            time_start = format_start_time(time)
            time_end = format_end_time(time)

            index = format_index_lesson(time_start)

            lesson = Lesson(index, day_name, time_start, time_end, group_id, week, info)
            lessons.append(lesson)

    return lessons


read_excel("")
