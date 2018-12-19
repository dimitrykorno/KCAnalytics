from report_api.Menu import Menu
from Reports import InAppSales, ContentActivity, ActiveUsers, CumulativeROI, BooksPopularity, SalesGraphs_TOREMOVE, LifetimeHistogram

# import timeit
#
# print(timeit.timeit("""result='2018-09-20'[:7]""",number=100000))
#
# print(timeit.timeit("""
# spl='2018-09-20'.split('-')
# result=spl[1]+"/"+spl[0]""",number=100000))

reports = [
    ("1. Отчёт по продажам", InAppSales.new_report),
    ("2. Графики спроса", SalesGraphs_TOREMOVE.new_report),
    ("3. Использование контента пользователями", ContentActivity.new_report),
    ("4. Часто заходящие пользователи", ActiveUsers.new_report),
    ("5. Накопительный ROI", CumulativeROI.new_report),
    ("6. Популярность книг", BooksPopularity.new_report),
    ("7. Гистограма лайфтайма", LifetimeHistogram.new_report)
]

if __name__ == '__main__':
    #отчет для ручного исполнения
    Menu.menu_handsmode(reports)


#функции для бота
def get_menu():
    return Menu.get_menu(reports)

def get_reports_number():
    return len(reports)

def get_report_name(rep_num):
    return " ".join(reports[rep_num - 1][0].split(".")[1].split())

def get_settings_str(rep_num, defaults=None):
    return Menu.get_settings_str(reports, rep_num, defaults)


def get_defaults(rep_num):
    return Menu.get_defaults(reports, rep_num)


def parse_value(value, default, type):
    return Menu.parse_value(value, default, type)


def execute_report(user,rep_num, settings):
    return Menu.execute_report(reports, rep_num, settings,user)