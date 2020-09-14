import emoji

# database info
db_name = "telegram_bot.db"

# tables names
table_users = "users"
table_teachers = "teachers"
table_lessons = "lessons"
table_week = "week"
table_events = "events"
table_faculty = "faculty"

# for operation with time
format_time = "%H:%M"

# commands answer
start_answer = """Ласкаво просимо \U00002757

\U00002699 Доступні групи:
"""

start_answer_en = """
Welcome \U00002757

\U00002699 Available groups:
"""

settings_answer = """
Будь ласка, виберіть дію:

/change_group - змінити групу
/change_lang - змінити мову на англійську
/groups - отримати список доступних груп
/about - детальніше про нас

/enable_reminders - ввімкнути нагадування про розклад занять за 20 хвилин до початку
/disable_reminders - вимкнути нагадування про розклад занять за 20 хвилин до початку 

Для отримання розкладу іншої групи, просто відправ її номер
<b>(Наприклад 101ЕМ, де ЕМ - українськими літерами)</b>

<a href="https://telegra.ph/Tvіj-nadіjnij-pomіchnik-v-navchannі-08-31">Ознайомитися детально:</a>

З питань підтримки, допомоги, пропозицій писати - @nupp_help
"""

settings_answer_en = """
Please select an action:

/change_group - change the group
/change_lang - change the language to Ukrainian
/groups - get a list of available groups
/about - more about us

/enable_reminders - enable class reminders 20 minutes before the start
/disable_reminders - Disable class schedule reminders 20 minutes before the start

To get another group's schedule, just send her number
<b> (For example, 101EM, where EM is in Ukrainian letters) </b>

<a href="https://telegra.ph/Your-reliable-learning-assistant-09-10">Help:</a>

For support, help, suggestions write - @nupp_help
"""

about_answer = """
Дизайнер аватара для бота - https://www.instagram.com/your_death_404/
Програмний код - https://www.instagram.com/bogdan.poh/

<b>З питань підтримки, допомоги, пропозицій</b> –– @nupp_help
"""

about_answer_en = """
Avatar designer for a bot - https://www.instagram.com/your_death_404/
Program code - https://www.instagram.com/bogdan.poh/

<b>On issues of support, assistance, suggestions</b> –– @nupp_help
"""

# other answers
warning = "Увага\U00002757"
warning_en = "Warning\U00002757"
not_register = "Будь ласка, відправте команду /start"
not_register_en = "Please send a command /start"
not_found_answer = "\U0001F648 Команда не знайдена"
not_found_answer_en = "\U0001F648 Command not found"
pick_your_group = """Будь ласка, надішліть свою групу \U0001F64F
<b>(Наприклад 101ЕМ, де ЕМ - українськими літерами)</b>

/en - продовжити на англійській мові"""

pick_your_group_en = """Please send your group \U0001F64F
<b>(For example 101EM, where EM - in Ukrainian letters)</b>

/ua - continue in Ukrainian"""

you_is_register = "Ви вже зареєстровані \U00002757"
no_lessons_today = "Сьогодні занять немає \U0001F601"
no_lessons_today_en = "There are no classes today \U0001F601"
no_lessons_tomorrow = "Завтра занять немає \U0001F601"
no_lessons_tomorrow_en = "There are no classes tomorrow \U0001F601"
thanks_for_a_registration = "Дякуємо за реєстрацію \U0001F60B"
thanks_for_a_registration_en = "Thank you for registering \U0001F60B"
file_not_found = "Файл не знайдено \U0001F614"
change_group = "Ваша група обновлена \U0001F970"
change_group_en = "Your group has been updated \U0001F970"
dont_found_group = "Вашої групи наразі немає, повідомте про це нам @nupp_help"

# keyboard buttons
keyboard_setting = "Налаштування"
keyboard_current_lessons = "Заняття на сьогодні"
keyboard_tomorrow_lessons = "Заняття на завтра"
keyboard_week_lessons = "Заняття на тиждень"

keyboard_setting_en = "Settings"
keyboard_current_lessons_en = "Classes for today"
keyboard_tomorrow_lessons_en = "Classes for tomorrow"
keyboard_week_lessons_en = "Classes for a week"

# day names
monday = "Понеділок"
tuesday = "Вівторок"
wednesday = "Середа"
thursday = "Четвер"
friday = "П\'ятниця"

const_sorted_days = ["monday", "tuesday", "wednesday", "thursday", "friday"]

# emoji numbers
one_number = emoji.emojize(":keycap_digit_one:", use_aliases=True)
two_number = emoji.emojize(":keycap_digit_two:", use_aliases=True)
three_number = emoji.emojize(":keycap_digit_three:", use_aliases=True)
four_number = emoji.emojize(":keycap_digit_four:", use_aliases=True)
five_number = emoji.emojize(":keycap_digit_five:", use_aliases=True)
six_number = emoji.emojize(":keycap_digit_six:", use_aliases=True)

# weeks
first_week = "first_week"
second_week = "second_week"
change_week_time = "07:00"

# remindes
reminders_enable = "Нагадування ввімкнено \U00002705"
reminders_disable = "Нагадування вимкнено \U0000274C"
reminders_is_enable = "Нагадування уже ввімкнено \U0001F609"

# language
lang_ua = "ua"
lang_en = "en"

# paths
documents_directory = "documents"
excel_file = "excel_file"
excel_file_faculty = "faculty_file"
excel_file_type = "xlsx"
excel_file_type_a = "xls"
txt_file = "info.txt"

# admin
admin_chat_id = 330926012
admin_log = -1001357315497
