from report_api.Menu import menu
from Reports import InAppSales, UserActivity, ActiveUsers, AccumulativeROI, BooksPopularity
#import timeit
# event="tap_mishki.starrysky_book_ru"
# print(timeit.timeit("""import re
# re.match(r'^tap_.+_ban_.+', 'tap_bookname_ban_rus')""",number=10000))
#
# print(timeit.timeit("""import re
# 'tap_bookname_ban_rus'.startswith('tap')""",number=10000))

reports = {
    "1. Отчёт по продажам": InAppSales.new_report,
    "2. Активность пользователей по странам": UserActivity.new_report,
    "3. Часто заходящие пользователи": ActiveUsers.new_report,
    "4. Накопительный ROI": AccumulativeROI.new_report,
    "5. Популярность книг": BooksPopularity.new_report
}

menu(reports)
