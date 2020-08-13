import emoji

# bot token
token = "1006676969:AAG_FJZoRIO65lqBNfKOs8MCjSQzNjBaJeU"

# database info
db_name = "telegram_bot.db"

# host = "localhost"
# db_name = "bogdanpoh"
# user = "bogdanpoh"
# password = "none"
# port = "5432"


# database names
table_users = "users"
table_teachers = "teachers"
table_lessons = "lessons"
table_week = "week"
table_events = "events"

# for operation with time
format_time = "%H:%M"

# commands answer
start_answer = """Ласкаво просимо \U00002757

\U00002699 Доступні групи:
"""

settings_answer = """
Будь ласка, виберіть дію:

/change_group - змінити групу

/enable_reminders - ввімкнути нагадування про розклад занять за 20 хвилин до початку

/disable_reminders - вимкнути нагадування про розклад занять за 20 хвилин до початку 

/about - детальніше про нас

Для отримання розкладу іншої групи, просто відправ її номер
<b>(Наприклад 101ЕМ, де ЕМ - російськими або українськими літерами)</b>

З питань підтримки, допомоги, пропозицій писати - @nupp_help
"""

about_anser = """
Дизайнер аватара для бота - https://www.instagram.com/your_death_404/
Програмний код - https://www.instagram.com/bogdan.poh/

<b>З питань підтримки, допомоги, пропозицій</b> –– @nupp_help
"""

# other answers
not_found_answer = "\U0001F648 Команда не знайдена"
pick_your_group = """Будь ласка, надішліть свою групу \U0001F64F 
<b>(Наприклад 101ЕМ, де ЕМ - російськими або українськими літерами)</b>"""
you_is_register = "Ви вже зареєстровані \U00002757"
no_lessons_today = "Сьогодні занять немає \U0001F601"
no_lessons_tomorrow = "Завтра занять немає \U0001F601"
thanks_for_a_registration = "Дякуємо за реєстрацію \U0001F60B"
file_not_found = "Файл не знайдено \U0001F614"
change_group = "Ваша група обновлена \U0001F970"

# keyboard buttons
keyboard_setting = "Налаштування"
keyboard_current_lessons = "Заняття на сьогодні"
keyboard_tomorrow_lessons = "Заняття на завтра"
keyboard_week_lessons = "Заняття на тиждень"

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

# paths
documents_directory = "documents"
excel_file = "excel_file"
excel_file_type = "xlsx"
excel_file_type_a = "xls"

# admin
admin_chat_id = 330926012
admin_log = -1001357315497
