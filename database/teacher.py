
class Teacher(object):
    id = 0
    name_teacher = ""
    chat_id = ""

    def __init__(self, name_teacher=None, chat_id=None, id=None, data=None):

        if data:
            self.id = data[0]
            self.name_teacher = data[1]
            self.chat_id = data[2]
        else:
            self.id = id
            self.name_teacher = name_teacher
            self.chat_id = chat_id

    def format_print(self):
        return "id: {0}, name_teacher: {1}, chat_id: {2}".format(self.id, self.name_teacher,self.chat_id)
