from datetime import datetime
import pandas as pd
from In_apps.Shop import get_brand_lang_inapp, get_brand_lang_book, get_brand_lang_free_book, is_free_book, is_inapp
from Classes.Events_2 import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count, get_medium_time, get_medium_time_2, check_arguments, check_folder, \
    try_save_writer
import os

app = "kc"


@time_count
def new_report(os_list=["Android"],
               period_start="2018-08-01",
               period_end=None,
               min_version=None,
               max_version=None,
               countries_list=[]):
    errors = check_arguments(locals())
    result_files = []
    folder_dest = "Results/BooksPopularity/"
    check_folder(folder_dest)

    if errors:
        return errors, result_files

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
                               period_end=None,
                               min_version=min_version,
                               max_version=max_version,
                               countries_list=[],
                               events_list=[("OpenBook",)],
                               order=False)

        # формируем таблицу отчета
        parameters = ["Brand", "Lang", "Book", "Reading"]

        # Пользовательские параметры
        countries = {}
        countries_free = {}
        countries_popularity = {}
        min_popularity = 100
        periods_list = set()

        free_books = set()
        # ЦИКЛ ОБРАБОТКИ СОБЫТИЙ
        while Report.get_next_event():
            if isinstance(Report.current_event, OpenBook):
                brand = Report.current_event.brand
                lang = Report.current_event.lang
                book = Report.current_event.book_name
                period = str(Report.current_event.datetime)[:7]
                periods_list.add(period)
                user_country = Report.current_user.country

                if user_country not in countries:
                    countries[user_country] = {}
                    countries_free[user_country] = {}
                    countries_popularity[user_country] = {}
                if period not in countries[user_country]:
                    countries[user_country][period] = {}
                    countries_free[user_country][period] = {}
                    countries_popularity[user_country][period] = set()
                countries_popularity[user_country][period].add(Report.current_user.user_id)

                if Report.current_event.price_money == 0:
                    free_books.add((book, brand, lang))

                if Report.current_event.book_name not in countries[user_country][period]:
                    countries[user_country][period][(book, brand, lang)] = 0
                countries[user_country][period][(book, brand, lang)] += 1

        periods_list = list(periods_list)
        periods_list.sort()
        for country in countries:
            filename = folder_dest + os_str + " " + country + ".xlsx"
            writer = pd.ExcelWriter(filename)
            for period in periods_list:
                if period not in countries_popularity[country] or len(
                        countries_popularity[country][period]) < min_popularity:
                    continue
                df_free = pd.DataFrame(index=[], columns=parameters)
                df_reading = pd.DataFrame(index=[], columns=parameters)
                total_events = 0

                for book_tuple in [book_tuple for book_tuple in countries[country][period] if book_tuple in free_books]:
                    total_events += countries[country][period][book_tuple]
                for book, brand, lang in [book_tuple for book_tuple in countries[country][period] if
                                          book_tuple in free_books]:
                    reading = round(countries[country][period][(book, brand, lang)] * 100 / total_events,
                                    1) if total_events > 0 else 0
                    df_free = df_free.append({
                        "Brand": brand + " free",
                        "Lang": lang,
                        "Book": book,
                        "Reading": str(reading) + "%"
                    }, ignore_index=True)

                df_free = df_free.sort_values(by=["Brand", "Lang"], ascending=False)

                for book, brand, lang in [book_tuple for book_tuple in countries[country][period] if
                                          book_tuple in free_books]:
                    df_reading = df_reading.append({
                        "Brand": brand,
                        "Lang": lang,
                        "Book": book,
                        "Reading": countries[country][period][(book, brand, lang)]
                    }, ignore_index=True)
                df_reading = df_reading.sort_values(by=["Lang", "Reading"], ascending=False)

                df_free.to_excel(writer, str(period).replace("/", "."), index=False)
                df_reading.to_excel(writer, str(period).replace("/", "."), index=False, startrow=df_free.shape[0] + 2)
                try_save_writer(writer, filename)
                result_files.append(os.path.abspath(filename))
        if len(result_files) > 5 and countries_list==[]:
            result_files = [file for file in result_files if "total" in file or "RU" in file]
        return errors, result_files
