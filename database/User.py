class User(object):
    id = 0
    name_user = ''
    group_id = ''
    chat_id = ''

    def __init__(self, name_user, group_id, chat_id, id=0):
        self.id = id
        self.name_user = name_user
        self.group_id = group_id
        self.chat_id = chat_id
