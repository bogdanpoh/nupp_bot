class Lesson(object):
    id = 0
    index = ""
    day_name = ""
    time_start = ""
    time_end = ""
    group_id = ""
    week = ""
    info = ""

    def __init__(self, index, day_name, time_start, time_end, group_id, week, info, id=0):
        self.id = id
        self.index = index
        self.day_name = day_name
        self.time_start = time_start
        self.time_end = time_end
        self.group_id = group_id
        self.week = week
        self.info = info

    def format_print(self):
        return "{0}, {1}, {2}-{3}, {4}, {5}, {6}".format(self.index, self.day_name,self.time_start, self.time_end, self.group_id, self.info, self.week)
