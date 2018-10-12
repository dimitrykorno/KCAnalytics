from datetime import datetime
import pandas as pd
from Classes.Events import *
from In_apps.book_names import get_book_category_language
from In_apps.In_apps import get_inapp_language, get_inapp_category
from Classes.Events import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count

app = "kc"


@time_count
def new_report(os_list=["Android", "iOS"],
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
                               events_list=[(["tap\_ buy\_%", "tap\_buy\_banner%"], "%success%"),

                                            (["not read\_book\_time%", "read\_book%"], '{"page":"0"}')

                                            ])


        # формируем таблицу отчета
        parameters = ["Price", "Brand", "Language", "Value 1", "Value 2"]

        # Пользовательские параметры
        user_country = None
        previous_period = None
        period = None
        # Параметры
        countries = {}
        countries_popularity = {}
        periods_list = []
        top3_purchases = []

        # ЦИКЛ ОБРАБОТКИ СОБЫТИЙ
        while Report.get_next_event():

            if Report.is_new_user():
                countries_popularity[user_country][period] += 1
                user_country = None
                previous_period = None
                period = None

            if not user_country:
                user_country = Report.current_user.country
            previous_period = period
            period = Report.current_event.datetime.strftime('%m/%Y')
            if period not in periods_list:
                periods_list.append(period)
            if user_country not in countries.keys():
                countries[user_country] = {}
                countries_popularity[user_country] = {}
            if period not in countries[user_country].keys():
                countries[user_country][period] = {"read": {}, "free": {}, "paying": {}}
                countries_popularity[user_country][period] = 0
            if previous_period and previous_period != period:
                countries_popularity[user_country][previous_period] += 1

            if isinstance(Report.current_event, KC_ReadFree):
                brand, lang = get_book_category_language(Report.current_event.obj_name)
                if None in (brand, lang):
                    continue
                if brand not in countries[user_country][period]["free"]:
                    countries[user_country][period]["free"][brand] = {"rus": 0, "eng": 0}
                countries[user_country][period]["free"][brand][lang] += 1
            elif isinstance(Report.current_event, KC_BuyEvent) or isinstance(Report.current_event, KC_ReadEvent):
                category = ""
                if isinstance(Report.current_event, KC_BuyEvent):
                    brand = get_inapp_category(Report.current_event.obj_name)
                    lang = get_inapp_language(Report.current_event.obj_name)
                    category = "paying"
                elif isinstance(Report.current_event, KC_ReadEvent):
                    brand, lang = get_book_category_language(Report.current_event.obj_name)
                    category = "read"
                if None in (brand, lang):
                    continue
                if brand not in countries[user_country][period][category]:
                    countries[user_country][period][category][brand] = {"rus": {}, "eng": {}}
                if Report.current_event.obj_name not in countries[user_country][period][category][brand][lang].keys():
                    countries[user_country][period][category][brand][lang][Report.current_event.obj_name] = 0
                countries[user_country][period][category][brand][lang][Report.current_event.obj_name] += 1


        periods_list.sort()
        for country in countries.keys():

            writer = pd.ExcelWriter("BooksPopularity/" + OS.get_os_string(os) + " " + country + ".xlsx")
            for period in periods_list:
                if period not in countries_popularity[country].keys() or countries_popularity[country][period] < 100:
                    continue
                df = pd.DataFrame(index=[], columns=parameters)
                df_reading = pd.DataFrame(index=[], columns=["Brand", "Book", "Lang", "Reading"])
                total_events = 0
                for brand in countries[country][period]["free"].keys():
                    for lang in countries[country][period]["free"][brand].keys():
                        total_events += countries[country][period]["free"][brand][lang]
                for brand in countries[country][period]["free"].keys():
                    for lang in countries[country][period]["free"][brand].keys():
                        value_2 = round(countries[country][period]["free"][brand][lang] * 100 / total_events,
                                        1) if total_events > 0 else 0
                        df = df.append({
                            "Price": "Free",
                            "Brand": brand,
                            "Language": lang,
                            "Value 1": str(countries[country][period]["free"][brand][lang]) + " (" + str(value_2) + "%)"
                        }, ignore_index=True)
                total_purchases = 0
                for brand in countries[country][period]["paying"].keys():
                    for lang in countries[country][period]["paying"][brand].keys():
                        for book in countries[country][period]["paying"][brand][lang].keys():
                            total_purchases += countries[country][period]["paying"][brand][lang][book]
                for brand in countries[country][period]["paying"].keys():
                    for lang in countries[country][period]["paying"][brand].keys():
                        max_purchases = 0
                        max_purchases_book = None
                        for book in countries[country][period]["paying"][brand][lang].keys():
                            if countries[country][period]["paying"][brand][lang][book] > max_purchases:
                                max_purchases = countries[country][period]["paying"][brand][lang][book]
                                max_purchases_book = book
                        value_2 = round(max_purchases * 100 / total_purchases, 1) if total_purchases > 0 else 0
                        df = df.append({
                            "Price": "Paying",
                            "Brand": brand,
                            "Language": lang,
                            "Value 1": max_purchases_book,
                            "Value 2": str(max_purchases) + " (" + str(value_2) + "%)"
                        }, ignore_index=True)
                df = df.sort_values(by=["Price", "Brand", "Language"], ascending=False)

                for brand in countries[country][period]["read"].keys():
                    for lang in countries[country][period]["read"][brand].keys():
                        for book in countries[country][period]["read"][brand][lang].keys():
                            df_reading = df_reading.append({
                                "Brand": brand,
                                "Book": book,
                                "Lang": lang,
                                "Reading": countries[country][period]["read"][brand][lang][book]
                            }, ignore_index=True)
                df_reading = df_reading.sort_values(by=["Lang", "Reading"], ascending=False)

                df.to_excel(writer, str(period).replace("/", "."), index=False)
                df_reading.to_excel(writer, str(period).replace("/", "."), index=False, startrow=df.shape[0] + 2)
                writer.save()
                # print(df.to_string(index=False))
        print(OS.get_os_string(os), "done.")

