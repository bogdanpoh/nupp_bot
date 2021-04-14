
class Session(object):
    id = 0
    group_id = "group_id"
    date = "date"
    time = "time"
    type = "type"
    name = "name"
    teacher_name = "teacher name"
    audience = "audience"

    def __init__(self,
                 id=0,
                 group_id=None,
                 date=None,
                 time=None,
                 type=None,
                 name=None,
                 teacher_name=None,
                 audience=None,
                 data=None):

        if data:
            self.id = data[0]
            self.group_id = data[1]
            self.date = data[2]
            self.time = data[3]
            self.type = data[4]
            self.name = data[5]
            self.teacher_name = data[6]
            self.audience = data[7]
        else:
            self.id = id
            self.group_id = group_id
            self.date = date
            self.time = time
            self.type = type
            self.name = name
            self.teacher_name = teacher_name
            self.audience = audience

    def format_print(self):
        return "group_id: {} id: {}, date: {}, time: {}, type: {}, name: {}, teacher_name: {}, audiunce: {}".format(self.group_id,
                                                                                                                    self.id,
                                                                                                       self.date,
                                                                                                       self.time,
                                                                                                       self.type,
                                                                                                       self.name,
                                                                                                       self.teacher_name,
                                                                                                       self.audience)

    def format_message(self):
        return "<b>{}</b> | {} | {} | <i>{}</i> | {} | {}".format(self.date,
                                                self.time,
                                       self.type,
                                       self.name,
                                       self.teacher_name,
                                       self.audience)
