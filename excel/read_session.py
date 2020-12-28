import xlrd
from database.session import Session
from excel import excel_tools

def read_session(path):
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)

    data = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]

    group_id = ""
    info = []
    session_array = []

    for item in data:
        new_item = excel_tools.remove_empty_element_in_array(item)

        if new_item:
            info.append(new_item)

    for item in info:

        # print(item)

        index = info.index(item)

        if index == 2:
            if len(item) > 0:
                group_id = excel_tools.format_group_id(item[0])

        if index > 3:
            audience = excel_tools.format_audience_name(item[5])
            date = excel_tools.format_date_from_excel(wb, item[0])

            teacher_name = excel_tools.remove_repetition_in_str(item[4])

            time_value = item[1]

            if type(time_value) is not str:
                time = excel_tools.format_time(item[1])
            else:
                time = time_value

            session_item = Session(group_id=group_id,
                                   date=date,
                                   time=time,
                                   type=item[2],
                                   name=item[3],
                                   teacher_name=teacher_name,
                                   audience=audience)

            if session_item:
                session_array.append(session_item)

    if session_array:
        return session_array
    else:
        return None
