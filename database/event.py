class Event(object):
    id = 0
    group_id = ""
    day_name = ""
    current_week = ""
    chat_id = ""
    send_time = ""
    is_send = 0

    def __init__(self, group_id=None, current_week=None, day_name=None, chat_id=None, send_time=None, is_send=None, id=None, data=None):
        if data:
            self.id = data[0]
            self.group_id = data[1]
            self.day_name = data[2]
            self.current_week = data[3]
            self.chat_id = data[4]
            self.send_time = data[5]
            self.is_send = data[6]
        else:
            self.id = id
            self.group_id = group_id
            self.day_name = day_name
            self.current_week = current_week
            self.chat_id = chat_id
            self.send_time = send_time
            self.is_send = is_send

    def set_status_send(self, status):
        self.is_send = int(status)

    def get_status_send(self):
        return bool(self.is_send)

    def format_print(self):
        return "id: {0}, group_id: {1}, day_name: {2}, current_week: {3}, chat_id: {4}, send_time: {5}, is_send: {6}".format(
            str(self.id),
            self.group_id,
            self.day_name,
            self.current_week,
            self.chat_id,
            self.send_time,
            str(bool(self.is_send)))
