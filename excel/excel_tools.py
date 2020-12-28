from itertools import groupby
import xlrd
import datetime


def format_audience_name(name):

    answer = str(name).replace(" ", "").replace("-", "")

    if answer[-2] == '.':
        return answer[0:-2]
    else:
        return answer

def remove_repetition(data):
    return [el for el, _ in groupby(data)]

def remove_empty_element_in_array(data):
    result = []
    for el in data:
        is_empty_str = str(el).replace(" ", "")
        if el and is_empty_str:
            result.append(el)

    return list(result)

def remove_repetition_in_str(string):
    return " ".join(str(string).split())

def format_group_id(group_name):

    group_id = (remove_repetition_in_str(group_name)).replace(" ", "").replace(".", "")

    if len(str(group_id).split("-")) > 1:
        group = str(group_id).split("-")

        group_id = group[0] + group[-1]

    return group_id

def format_date_from_excel(book, date_value):

    if type(date_value) == str:
        return str(date_value).replace(" ", "")

    datetime_answer = datetime.datetime(*xlrd.xldate_as_tuple(date_value, book.datemode))

    return datetime_answer.strftime("%d.%m.%Y")