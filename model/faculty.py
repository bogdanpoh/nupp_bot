class Faculty(object):
    id = 0
    faculty = ""
    group_id = ""

    def __init__(self, faculty=None, group_id=None, data=None):
        if data:
            self.id = data[0]
            self.faculty = data[1]
            self.group_id = data[2]
        else:
            self.faculty = faculty
            self.group_id = group_id

    def format_print(self):
        return "Faculty: {} - Group: {}".format(self.faculty, self.group_id)