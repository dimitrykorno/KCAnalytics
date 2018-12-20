from datetime import datetime
import pandas as pd
from In_apps.Shop import get_brand_lang_book
from Classes.Events_2 import *
from Data import Parse_2
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count, get_medium_time, try_save_writer, check_folder, check_arguments
import os
app = "kc"


@time_count
def new_report(os_list=["iOS", "Android"],
               period_start="2018-08-01",
               period_end=None,
               min_version=None,
               max_version=None,
               countries_list=[]):
    errors = check_arguments(locals())
    result_files = []
    folder_dest = "Results/UserActivity/"
    check_folder(folder_dest)

    if errors:
        return errors,result_files

    if hasattr(new_report,'user'):
        folder_dest+=str(new_report.user)+"/"

    if isinstance(period_start, str):
        period_start = datetime.strptime(period_start, "%Y-%m-%d").date()
    if isinstance(period_end, str):
        period_end = datetime.strptime(period_end, "%Y-%m-%d").date()

    for os_str in os_list:

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
                               events_list=[(["TapBuyStore", "TapBuyBookForMoney", "TapBuyBookForCoins", "TapBuyCoins"],
                                             "%success%"),
                                            ("SubscriptionPaymentFromServer",),
                                            (
                                                {"TapBook", "TapSection", "EnterSection", "DownloadStart",
                                                 "DownloadFinish",
                                                 "DownloadCancel", "DeleteBook", "OpenBook", "TapLike"},)]
                               )
        # формируем таблицу отчета
        islands = ["Mishki", "Fixiki", "Mashka", "Spookystories", "OmNom", "Trikota", "MyBooks", "Tales"]
        cumulative_parameters = ["Users", "Paying",
                                 "Enter isle 0", "Enter isle 1", "Enter isle 2", "Enter isle 3",
                                 "Enter isle 4", "Enter isle 5", "Enter isle 6", "Enter isle 7", "Enter isle 8",
                                 "Read free 0", "Read free 1", "Read free 2", "Read free 3", "Read free 4",
                                 "Read free 5"
                                 ]
        activity_parameters = [
            "Tap island", "Enter island", "Tap book", "Read book",
        ]
        countries = {}
        cumulative_data = {}
        countries["total"] = {}
        cumulative_data["total"] = {}
        cumulative_data["total"] = dict.fromkeys(cumulative_parameters, 0)
        user_activity = {}
        for isle in islands:
            countries["total"][isle] = dict.fromkeys(activity_parameters, 0)
            user_activity[isle] = dict.fromkeys(activity_parameters, 0)
        user_activity["shelf"] = set()
        user_activity["read free"] = set()
        user_activity["paying"] = 0

        # Перемещение данных пользователя в отчет
        def flush_user_info():
            if country not in countries:
                countries[country] = {}
                for isle in islands:
                    countries[country][isle] = dict.fromkeys(activity_parameters, 0)
                cumulative_data[country] = dict.fromkeys(cumulative_parameters, 0)
            for isle in islands:
                for param in activity_parameters:
                    countries[country][isle][param] += user_activity[isle][param]
                    countries["total"][isle][param] += user_activity[isle][param]
            for c in (country, "total"):
                cumulative_data[c]["Users"] += 1
                cumulative_data[c]["Read free " + str(len(user_activity["read free"]))] += 1
                cumulative_data[c]["Enter isle " + str(len(user_activity["isles"]))] += 1
                cumulative_data[c]["Paying"] += user_activity["paying"]

        while Report.get_next_event():
            country = Report.current_user.country
            # проверяем на появление неизвестных островов
            if hasattr(Report.current_event, "section") and Report.current_event.section not in islands:
                Report.not_found("Unknown section " + Report.current_event.section)
                errors+="В код отчёта не добавлен новый остров: "+Report.current_event.section
                continue

            if Report.is_new_user():
                flush_user_info()
                user_activity = {}
                for isle in islands:
                    user_activity[isle] = dict.fromkeys(activity_parameters, 0)
                user_activity["isles"] = set()
                user_activity["read free"] = set()
                user_activity["paying"] = 0

            if isinstance(Report.current_event, TapSection):
                user_activity[Report.current_event.section]["Tap island"] = 1
                user_activity["isles"].add(Report.current_event.section)

            elif isinstance(Report.current_event, EnterSection):
                user_activity[Report.current_event.section]["Enter island"] = 1
                user_activity["isles"].add(Report.current_event.section)

            elif isinstance(Report.current_event, TapBook):
                user_activity[Report.current_event.section]["Tap Book"] = 1
            elif isinstance(Report.current_event, OpenBook):
                user_activity[Report.current_event.brand]["Read Book"] = 1
                if Report.current_event.price_money == 0:
                    user_activity[country]["read free"].add(Report.current_event.book_name)
            elif isinstance(Report.current_event, TapBuyStore) \
                    or isinstance(Report.current_event, TapBuyBookForMoney) \
                    or isinstance(Report.current_event, TapBuyCoins) \
                    or isinstance(Report.current_event, SubscriptionPaymentFromServer):
                user_activity["paying"] = 1

        flush_user_info()

        for country in countries:
            cumulative_parameters[country]["Users"] = len(
                [inst for inst in Report.get_installs() if inst["country_iso_code"] == country])

        sorted_countries = ["total"]
        if "RU" in countries:
            sorted_countries.append("RU")
        sorted_countries += [c for c in countries.keys() if c not in ("total", "RU")]

        filename = folder_dest + os_str + " Total Funnel.xlsx"
        writer = pd.ExcelWriter(filename)
        # рисуем проценты и записываем в таблицы
        for country in sorted_countries:
            df_sections = pd.DataFrame(index=islands, columns=activity_parameters)
            df_cumulative = pd.DataFrame(index=[country], columns=cumulative_parameters)

            df_cumulative.at[country, "Users"] = cumulative_data[country]["Users"]
            df_cumulative.at[country, "Paying"] = cumulative_data[country]["Paying"]

            for isle in islands:
                old_percent = 100
                for param in activity_parameters:
                    new_percent = round(countries[country][isle][param] * 100 / cumulative_data[country]["Users"], 1)
                    difference = " (-" + str(round(abs(old_percent - new_percent), 1)) + "%)"
                    df_sections.at[isle, param] = str(countries[country][isle][param]) + " (" + str(
                        new_percent) + "%)" + difference
                    old_percent = new_percent

            old_percent = 100
            for param in [par for par in cumulative_parameters if "Enter" in par]:
                new_percent = round(cumulative_data[country][param] * 100 / cumulative_data[country]["Users"], 1)
                difference = " (-" + str(round(abs(old_percent - new_percent), 1)) + "%)"
                df_cumulative.at[country, param] = str(cumulative_data[country][param]) + " (" + str(
                    new_percent) + "%)" + difference
                old_percent = new_percent

            old_percent = 100
            for param in [par for par in cumulative_parameters if "Read" in par]:
                new_percent = round(cumulative_data[country][param] * 100 / cumulative_data[country]["Users"], 1)
                difference = " (-" + str(round(abs(old_percent - new_percent), 1)) + "%)"
                df_cumulative.at[country, param] = str(cumulative_data[country][param]) + " (" + str(
                    new_percent) + "%)" + difference
                old_percent = new_percent

            df_cumulative.to_excel(writer, sheet_name=country)
            df_sections.to_excel(writer, sheet_name=country, startrow=4)
        try_save_writer(writer, filename)
        result_files.append(os.path.abspath(filename))

    return result_files
