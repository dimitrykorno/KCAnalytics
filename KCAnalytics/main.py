from report_api.Menu import menu
from Reports import InAppSales, ContentActivity, ActiveUsers, CumulativeROI, BooksPopularity, SalesGraphs, LifetimeHistogram

# import timeit
#
# print(timeit.timeit("""result='2018-09-20'[:7]""",number=100000))
#
# print(timeit.timeit("""
# spl='2018-09-20'.split('-')
# result=spl[1]+"/"+spl[0]""",number=100000))

reports = [
    ("1. Отчёт по продажам", InAppSales.new_report),
    ("2. Графики спроса", SalesGraphs.new_report),
    ("3. Использование контента пользователями", ContentActivity.new_report),
    ("4. Часто заходящие пользователи", ActiveUsers.new_report),
    ("5. Накопительный ROI", CumulativeROI.new_report),
    ("6. Популярность книг", BooksPopularity.new_report),
    ("7. Гистограма лайфтайма", LifetimeHistogram.new_report)
]

menu(reports)
