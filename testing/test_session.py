from database import db_manager
from database.lesson import Lesson
from database.faculty import Faculty
from excel import read_session
import tools
import os


root_path = "../../../For bot/Sessions"

list_files = os.listdir(root_path)

def print_session(sessions):
    for session in sessions:
        print(session.format_print())


for file in list_files:
    if file != ".DS_Store" and file != 'format_file_to_session.py':

        abs_path = os.path.join(root_path, file)

        if os.path.isfile(abs_path):
            sessions = read_session.read_session(abs_path)

            print_session(sessions)