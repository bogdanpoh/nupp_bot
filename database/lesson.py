class Lesson(object):
    id = 0
    row = ""
    day_name = ""
    time_start = ""
    time_end = ""
    group_id = ""
    week = ""
    info = ""

    def __init__(self, row=None, day_name=None, time_start=None, time_end=None, group_id=None, week=None, info=None, id=0, data=None):

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

    def format_print(self):
        return "{0}, {1}, {2}-{3}, {4}, {5}, {6}".format(self.row, self.day_name, self.time_start, self.time_end, self.group_id, self.info, self.week)
