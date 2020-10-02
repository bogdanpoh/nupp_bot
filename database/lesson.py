import constants


class Lesson(object):
    id = 0
    row = ""
    day_name = ""
    time_start = ""
    time_end = ""
    group_id = ""
    week = ""
    info = ""

    def __init__(self, row=None, day_name=None, time_start=None, time_end=None, group_id=None, week=None, info=None,
                 id=0, data=None):

        if data:
            self.id = data[0]
            self.row = data[1]
            self.day_name = data[2]
            self.time_start = data[3]
            self.time_end = data[4]
            self.group_id = data[5]
            self.week = data[6]
            self.info = data[7]
        else:
            self.id = id
            self.row = row
            self.day_name = day_name
            self.time_start = time_start
            self.time_end = time_end
            self.group_id = group_id
            self.week = week
            self.info = info

        if str(self.info).find("None"):
            if self.info.find("None") > 0:
                index_start = self.info.find("None")
                new_info = self.info[0:index_start-2]
                self.info = new_info

    def format_print(self):
        return "week: {6} №{0} day: {1} time: {2} - {3} group: {4} info: {5}".format(
            self.row,
            self.day_name,
            self.time_start,
            self.time_end,
            self.group_id,
            self.info,
            self.week)

    def format_message(self, is_teacher_format=False):

        row = ""

        if str(self.row) == str(1):
            row = constants.one_number
        elif str(self.row) == str(2):
            row = constants.two_number
        elif str(self.row) == str(3):
            row = constants.three_number
        elif str(self.row) == str(4):
            row = constants.four_number
        elif str(self.row) == str(5):
            row = constants.five_number
        elif str(self.row) == str(6):
            row = constants.six_number

        if is_teacher_format:
            return "{0} <b>{1}-{2}</b> – <i>{3}, {4}</i>".format(row,
                                                                 self.time_start,
                                                                 self.time_end,
                                                                 self.group_id,
                                                                 self.info)
        else:
            return "{0} <b>{1}-{2}</b> – <i>{3}</i>".format(row,
                                                            self.time_start,
                                                            self.time_end,
                                                            self.info)
