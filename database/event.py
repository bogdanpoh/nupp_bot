class Event(object):
    id = 0
    group_id = ""
    day_name = ""
    week = ""
    chat_id = ""
    send_time = ""
    is_send = False

    def __init__(self, group_id=None, week=None, day_name=None, chat_id=None, send_time=None, is_send=None, id=None, data=None):
        if data:
            self.id = data[0]
            self.group_id = data[1]
            self.day_name = data[2]
            self.week = data[3]
            self.chat_id = data[4]
            self.send_time = data[5]
            self.is_send = data[6]
        else:
            self.id = id
            self.group_id = group_id
            self.day_name = day_name
            self.week = week
            self.chat_id = chat_id
            self.send_time = send_time
            self.is_send = is_send

    def set_day_name(self, day_name):
        self.day_name = day_name

    def set_week(self, week):
        self.week = week

    def set_send_time(self, send_time):
        self.send_time = send_time

    def set_status_send(self, status):
        self.is_send = status

    def get_status_send(self):
        return self.is_send

    def format_print(self):
        return "id: {0}, group_id: {1}, day_name: {2}, week: {3}, chat_id: {4}, send_time: {5}, is_send: {6}".format(
            str(self.id),
            self.group_id,
            self.day_name,
            self.week,
            self.chat_id,
            self.send_time,
            str(self.is_send))
