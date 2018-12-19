from datetime import datetime, timedelta, date
import pandas as pd
import calendar
from Classes.Events import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count, get_medium_time

app = "kc"


@time_count
def new_report(os_list=["Android", "iOS"],
               days_after_install=28,
               period_start=None,
               period_end=None,
               min_version=None,
               max_version=None,
               countries_list=[]):
    if isinstance(period_start, str):
        period_start = datetime.strptime(period_start, "%Y-%m-%d").date()
    if isinstance(period_end, str):
        period_end = datetime.strptime(period_end, "%Y-%m-%d").date()

    for os_str in os_list:
        os = OS.get_os(os_str)

        Report.set_app_data(parser=Parse, event_class=Event, user_class=User, os=os_str, app=app,
                            user_status_check=False)
        Report.set_installs_data(additional_parameters=None,
                                 period_start=period_start,
                                 period_end=period_end,
                                 min_version=min_version,
                                 max_version=max_version,
                                 countries_list=countries_list)

        Report.set_events_data(additional_parameters=None,
                               period_start=period_start,
                               period_end=period_end,
                               min_version=min_version,
                               max_version=max_version,
                               countries_list=[],
                               events_list=[({"tap_cats_ban_mainmenu", "tap_fixiki_ban_mainmenu",
                                              "tap_mashka_ban_mainmenu", "tap_mimi_ban_mainmenu",
                                              "tap_omnom_ban_mainmenu",
                                              "parent_gate_passed", "Tap_present"},),
                                            (["not read\_book\_time%", "read\_book%", "tap_ buy_%", "tap_buy_banner%",
                                              "tap\_%\_games\_%", "tap\_%\_book\_%", "tap\_%\_ban\_%"],)])

        # формируем таблицу отчета
        user_parameters = ["Users"]

        activity_parameters = ["3-4 weeks a month", "1-2 weeks a month", "Average time in app",
                               "Average time in app (regular)", "Max time in app"]
        parameters = user_parameters + activity_parameters

        weeks_list = []
        years = []
        start_date = datetime.strptime("2017-09-01", "%Y-%m-%d").date()
        while start_date < datetime.now().date():
            start_date += timedelta(days=30)
            if start_date.year not in years:
                years.append(start_date.year)
        for year in years:
            for month in range(1, 13):
                mondays = [
                    day.split()[0] for day in calendar.month(year, month).split("\n")[2:-1]
                    if not day.startswith("  ")]
                for monday in mondays:
                    monday_date = date(year, int(month), int(monday))
                    if datetime.now().date() - timedelta(days=90) < monday_date < datetime.now().date():
                        weeks_list.append(monday_date)
        weeks_list = list(reversed(weeks_list))

        # Пользовательские параметры
        user_activity = [0] * len(weeks_list)
        personal_week_list = weeks_list
        play_time = 0
        start_time = None

        # Данные об установках и странах
        countries = {}
        time_in_app = {}
        time_in_app_regular = {}

        # Перемещение данных пользователя в отчет
        def flush_user_info():

            if Report.previous_user.country not in countries:
                countries[Report.previous_user.country] = dict.fromkeys(parameters, 0)
            if Report.previous_user.country not in time_in_app:
                time_in_app[Report.previous_user.country] = []
                time_in_app_regular[Report.previous_user.country] = []

            # перенос данных пользоваетля
            month = 0
            missed_weeks = 0
            regular = True
            semi_regular = True
            for index, week in enumerate(user_activity):
                month = month % 4 + 1
                if week == 0:
                    missed_weeks += 1
                if month == 1:
                    if missed_weeks > 1:
                        regular = False
                    if missed_weeks > 3:
                        semi_regular = False
                    missed_weeks = 0
                if index == 9:
                    if regular:
                        countries[Report.previous_user.country]["3-4 weeks a month"] += 1
                    elif semi_regular:
                        countries[Report.previous_user.country]["1-2 weeks a month"] += 1
            time_in_app[Report.previous_user.country].append(play_time)
            if regular or semi_regular:
                time_in_app_regular[Report.previous_user.country].append(play_time)
            countries[Report.previous_user.country]["Users"] += 1

        print("medium %.10s %.10s" % get_medium_time())
        # ЦИКЛ ОБРАБОТКИ СОБЫТИЙ
        while Report.get_next_event():
            if Report.get_time_since_install(measure="day") < days_after_install:
                Report.skip_current_user()

            if Report.is_new_user():
                flush_user_info()
                personal_week_list = [week for week in weeks_list if week >= Report.current_user.install_date]
                user_activity = [0] * len(personal_week_list)
                play_time = 0

            for index, week in enumerate(personal_week_list):
                if 0 <= (Report.current_event.datetime.date() - week).days < 7:
                    user_activity[index] = 1

            if not start_time:
                start_time = Report.current_event.datetime
            else:
                if Report.get_timediff() > 5:
                    play_time += Report.get_timediff(start_time, Report.previous_event.datetime, measure="min")
                    start_time = Report.current_event.datetime

        flush_user_info()

        df = pd.DataFrame(index=list(countries.keys()), columns=parameters)
        for country in countries:

            for param in parameters:
                df.at[country, param] = countries[country][param]
            avg_time = 0
            avg_time_regular = 0
            for play_time in time_in_app[country]:
                avg_time += play_time / len(time_in_app[country])
            for play_time in time_in_app_regular[country]:
                avg_time_regular += play_time / len(time_in_app_regular[country])
            avg_time = round(avg_time, 1)
            avg_time_regular = round(avg_time_regular, 1)
            max_time = round(max(time_in_app[country]), 1)

            avg_time = str(int(avg_time) // 60) + "h " + str(int(avg_time) % 60) + "min"
            avg_time_regular = str(int(avg_time_regular) // 60) + "h " + str(int(avg_time_regular) % 60) + "min"
            max_time = str(int(max_time) // 60) + "h " + str(int(max_time) % 60) + "min"

            df.at[country, "Average time in app"] = avg_time
            df.at[country, "Average time in app (regular)"] = avg_time_regular
            df.at[country, "Max time in app"] = max_time
        df = df.sort_values(by=["Users"], ascending=False)

        writer = pd.ExcelWriter("Results/ActiveUsers/" + OS.get_os_string(os) + " " + "ActiveUsers.xlsx")
        df.to_excel(writer, " " + str(period_start) + "-" + str(period_end))
        writer.save()

        print(df.to_string())
