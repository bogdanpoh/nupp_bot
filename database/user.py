class User(object):
    id = 0
    name_user = ""
    group_id = ""
    chat_id = ""
    language = ""

    def __init__(self, name_user=None, chat_id=None, id=None, group_id=None, language="ua", data=None):

        if data:
            self.id = data[0]
            self.name_user = data[1]
            self.group_id = data[2]
            self.chat_id = data[3]
            self.language = data[4]

        else:
            self.id = id
            self.name_user = name_user
            self.group_id = group_id
            self.chat_id = chat_id
            self.language = language

    def format_print(self):
        return "id: {0} \n name_user: {1} \n group_id: {2} \n chat_id: {3} \n language: {4}".format(
            self.id,
            self.name_user,
            self.group_id,
            self.chat_id,
            self.language)
