from database import db_manager
from database.lesson import Lesson
from database.faculty import Faculty
import tools
import os

# root_path = "../../../Downloads/1-5"
root_path = "../../../Downloads/New"
# root_path = "../../../Downloads/1-5/ННІФЕтаМ/201ЕМ.xlsx"

read_faculty = False
read_one_file = False
show_only_group_id = False
show_only_group_id_and_info = False

if read_faculty:
    info = tools.read_faculty(root_path)

    lessons = db_manager.get_lessons()

    for lesson in lessons:
        for el in info:
            if str(el.group_id) == str(lesson.group_id):
                print("{} {}".format(lesson.group_id, el.faculty))

elif read_one_file:
    lessons = tools.read_lessons(root_path, testing=True)

    for lesson in lessons:
        if show_only_group_id:
            print("{} {} {}".format(lesson.week, lesson.day_name, lesson.group_id))
        else:
            print(lesson.format_print())

else:
    directories = os.listdir(root_path)

    all_files_count = 0

    for directory in directories:

        fakultet = os.path.join(root_path, directory)

        if os.path.isfile(fakultet) and str(fakultet).split("/")[-1] != ".DS_Store":
            lessons = tools.read_lessons(fakultet)

            print(fakultet)
            print()

            for lesson in lessons:
                if show_only_group_id:
                    print("{} {} {}".format(lesson.week, lesson.day_name, lesson.group_id))
                elif show_only_group_id_and_info:
                    print("{} {} {} {}".format(lesson.week, lesson.day_name, lesson.group_id, lesson.info))
                else:
                    print(lesson.format_print())

            print("------------------------------\n")
            all_files_count += 1

        elif os.path.isdir(fakultet):

            lessons_files = os.listdir(fakultet)

            all_files_count += len(lessons_files)

            groups = set()

            print(directory + " {}".format(len(os.listdir(fakultet))))
            print("------------------------------------------")

            for file in lessons_files:
                if str(file) == ".DS_Store":
                    all_files_count -= 1
                else:
                    if show_only_group_id is False:
                        print(file + " " + str(lessons_files.index(file)))

                    file_path = os.path.join(fakultet, file)

                    if show_only_group_id is False:
                        print(file_path)

                    if os.path.isfile(file_path):
                        lessons = tools.read_lessons(file_path, testing=True)

                        for lesson in lessons:

                            if show_only_group_id:
                                groups.add(lesson.group_id)
                            else:
                                print(lesson.format_print())

            print(groups)

    print("Всего: " + str(all_files_count))