class User(object):
    id = 0
    name_user = ''
    group_id = ''
    chat_id = ''

    def __init__(self, name_user=None, chat_id=None, id=None, group_id=None, data=None):

        if data:
            self.id = data[0]
            self.name_user = data[1]
            self.group_id = data[2]
            self.chat_id = data[3]
        else:
            self.id = id
            self.name_user = name_user
            self.group_id = group_id
            self.chat_id = chat_id

    def format_print(self):
        return "id: {0}, name_user: {1}, group_id: {2}, chat_id: {3}".format(self.id, self.name_user, self.group_id, self.chat_id)