from report_api.Menu import menu
from Reports import InAppSales, UserActivity, ActiveUsers, AccumulativeROI, BooksPopularity

reports = {
    "1. Отчёт по продажам": InAppSales.new_report,
    "2. Активность пользователей по странам": UserActivity.new_report,
    "3. Часто заходящие пользователи": ActiveUsers.new_report,
    "4. Накопительный ROI": AccumulativeROI.new_report,
    "5. Популярность книг": BooksPopularity.new_report
}

menu(reports)
