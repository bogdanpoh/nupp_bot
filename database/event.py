class Event(object):
    id = 0
    group_id = ""
    current_week = ""
    chat_id = ""
    send_time = ""
    is_send = 0

    def __init__(self, group_id=None, current_week=None, chat_id=None, send_time=None, is_send=None, id=None, data=None):
        if data:
            self.id = data[0]
            self.group_id = data[1]
            self.current_week = data[2]
            self.chat_id = data[3]
            self.send_time = data[4]
            self.is_send = data[5]
        else:
            self.id = id
            self.group_id = group_id
            self.current_week = current_week
            self.chat_id = chat_id
            self.send_time = send_time
            self.is_send = is_send

    def set_status_send(self, status):
        self.is_send = status

    def format_print(self):
        return "id: {0}, group_id: {1}, current_week: {2}, chat_id: {3}, send_time: {4}, is_send: {5}"\
            .format(str(self.id), self.group_id, self.current_week, self.chat_id, self.send_time, str(bool(self.is_send)))
