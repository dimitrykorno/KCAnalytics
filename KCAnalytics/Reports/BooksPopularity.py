from datetime import datetime
import pandas as pd
from In_apps.Shop import get_brand_lang_inapp, get_brand_lang_book, get_brand_lang_free_book, is_free_book, is_inapp
from Classes.Events import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count, get_medium_time, get_medium_time_2
import time

app = "kc"


@time_count
def new_report(os_list=["Android"],
               period_start="2018-08-01",
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
                               period_end=None,
                               min_version=min_version,
                               max_version=max_version,
                               countries_list=[],
                               events_list=[(["not read\_book\_time%", "read\_book%"], '{"page":"0"}')],
                               order=False)

        # формируем таблицу отчета
        parameters = ["Brand", "Lang", "Book", "Reading"]

        # Пользовательские параметры
        countries = {}
        countries_popularity = {}
        periods_list = set()

        # ЦИКЛ ОБРАБОТКИ СОБЫТИЙ
        while Report.get_next_event():

            period = str(Report.current_event.datetime)[:7]
            periods_list.add(period)
            user_country = Report.current_user.country
            if user_country not in countries:
                countries[user_country] = {}
                countries_popularity[user_country] = {}
            if period not in countries[user_country]:
                countries_popularity[user_country][period] = set()
                countries[user_country][period] = {}

            countries_popularity[user_country][period].add(Report.current_user.user_id)

            if Report.current_event.obj_name not in countries[user_country][period]:
                countries[user_country][period][Report.current_event.obj_name] = 0
            countries[user_country][period][Report.current_event.obj_name] += 1

        periods_list = list(periods_list)
        periods_list.sort()
        for country in countries:
            # print(country)
            writer = pd.ExcelWriter("Results/BooksPopularity/" + OS.get_os_string(os) + " " + country + ".xlsx")
            for period in periods_list:
                # print(period)
                if period not in countries_popularity[country] or len(countries_popularity[country][period]) < 100:
                    continue
                df_free = pd.DataFrame(index=[], columns=parameters)
                df_reading = pd.DataFrame(index=[], columns=parameters)
                total_events = 0

                for book in [book for book in countries[country][period] if is_free_book(book)]:
                    total_events += countries[country][period][book]
                for book in [book for book in countries[country][period] if is_free_book(book)]:
                    brand,lang = get_brand_lang_free_book(book)
                    reading = round(countries[country][period][book] * 100 / total_events,
                                    1) if total_events > 0 else 0
                    df_free = df_free.append({
                        "Brand": brand+" free",
                        "Lang": lang,
                        "Book": book,
                        "Reading": str(reading) + "%"
                    }, ignore_index=True)

                df_free = df_free.sort_values(by=[ "Brand", "Lang"], ascending=False)

                # print("free done")
                for book in [book for book in countries[country][period] if not is_free_book(book)]:
                    brand, lang = get_brand_lang_book(book)
                    df_reading = df_reading.append({
                        "Brand": brand,
                        "Lang": lang,
                        "Book": book,
                        "Reading": countries[country][period][book]
                    }, ignore_index=True)
                df_reading = df_reading.sort_values(by=["Lang", "Reading"], ascending=False)
                # print("read done")
                df_free.to_excel(writer, str(period).replace("/", "."), index=False)
                df_reading.to_excel(writer, str(period).replace("/", "."), index=False, startrow=df_free.shape[0] + 2)
                writer.save()
                # print(df_free.to_string(index=False))
        print(OS.get_os_string(os), "done.")
