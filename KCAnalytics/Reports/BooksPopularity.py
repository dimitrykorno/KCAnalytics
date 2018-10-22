from datetime import datetime
import pandas as pd
from In_apps.Shop import get_brand_lang_inapp,get_brand_lang_book,get_brand_lang_free_book,is_free_book, is_inapp
from Classes.Events import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count,get_medium_time,get_medium_time_2

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
                               events_list=[#(["tap\_ buy\_%", "tap\_buy\_banner%"], "%success%"),

                                            (["not read\_book\_time%", "read\_book%"], '{"page":"0"}')

                                            ])


        # формируем таблицу отчета
        parameters = ["Price", "Brand", "Language", "Value 1", "Value 2"]

        # Пользовательские параметры
        user_country = None
        period = None
        # Параметры
        countries = {}
        countries_popularity = {}
        periods_list = []
        previous_book=None
        top3_purchases = []
        brand_lang_buffer={}
        # ЦИКЛ ОБРАБОТКИ СОБЫТИЙ
        while Report.get_next_event():

            if Report.is_new_user():
                #print("new user",Report.current_user.user_id)
                countries_popularity[user_country][period] += 1
                user_country = None
                period = None

            if not user_country:
                user_country = Report.current_user.country
            previous_period = period
            period = Report.current_event.datetime.strftime('%m/%Y')
            if period not in periods_list:
                periods_list.append(period)
            if user_country not in countries:
                countries[user_country] = {}
                countries_popularity[user_country] = {}
            if period not in countries[user_country]:
                '''
                countries[user_country][period] = {"read": {}, "free": {}, "paying": {}}
                countries_popularity[user_country][period] = 0
                '''
                countries_popularity[user_country][period] = 0
                countries[user_country][period]={}
            if previous_period and previous_period != period:
                countries_popularity[user_country][previous_period] += 1



            if isinstance(Report.current_event, KCReadFree) or isinstance(Report.current_event, KCReadEvent):

                '''
                brand, lang = get_brand_lang_free_book(Report.current_event.obj_name)
                if "None" in {brand, lang}:
                    continue
                category = "free"
                if brand not in countries[user_country][period][category]:
                    countries[user_country][period][category][brand] = {"rus": 0, "eng": 0}
                countries[user_country][period][category][brand][lang] += 1
                '''
                if Report.current_event.obj_name not in countries[user_country][period]:
                  countries[user_country][period][Report.current_event.obj_name]=0
                countries[user_country][period][Report.current_event.obj_name]+=1
            elif isinstance(Report.current_event, KCBuyEvent): #or isinstance(Report.current_event, KCReadEvent):
                '''
                category = ""
                if isinstance(Report.current_event, KCBuyEvent):
                    brand, lang = get_brand_lang_inapp(Report.current_event.purchase)
                    book=Report.current_event.purchase
                    category = "paying"

                elif isinstance(Report.current_event, KCReadEvent):
                    brand, lang = get_brand_lang_book(Report.current_event.obj_name)
                    category = "read"
                    book=Report.current_event.obj_name
                if "None" in {brand, lang}:
                    continue
                if brand not in countries[user_country][period][category]:
                    countries[user_country][period][category][brand] = {"rus": {}, "eng": {}}

                #print(Report.current_event.obj_name, user_country,period,category,brand,lang)
                if book not in countries[user_country][period][category][brand][lang]:
                    countries[user_country][period][category][brand][lang][book] = 0
                countries[user_country][period][category][brand][lang][book] += 1
                '''
                if Report.current_event.purchase not in countries[user_country][period]:
                  countries[user_country][period][Report.current_event.purchase]=0
                countries[user_country][period][Report.current_event.purchase]+=1
        print("fetch end")
        print("medium {0:.10f} {0:.10f}".format(get_medium_time(), get_medium_time_2()))
        periods_list.sort()
        for country in countries:
            #print(country)
            writer = pd.ExcelWriter("Results/BooksPopularity/" + OS.get_os_string(os) + " " + country + ".xlsx")
            for period in periods_list:
                #print(period)
                if period not in countries_popularity[country].keys() or countries_popularity[country][period] < 100:
                    continue
                df = pd.DataFrame(index=[], columns=parameters)
                df_reading = pd.DataFrame(index=[], columns=["Brand", "Book", "Lang", "Reading"])
                total_events = 0
                '''
                for brand in countries[country][period]["free"]:
                    for lang in countries[country][period]["free"][brand]:
                        total_events += countries[country][period]["free"][brand][lang]
                for brand in countries[country][period]["free"]:
                    for lang in countries[country][period]["free"][brand]:
                        value_2 = round(countries[country][period]["free"][brand][lang] * 100 / total_events,
                                        1) if total_events > 0 else 0
                        df = df.append({
                            "Price": "Free",
                            "Brand": brand,
                            "Language": lang,
                            "Value 1": str(countries[country][period]["free"][brand][lang]) + " (" + str(value_2) + "%)"
                        }, ignore_index=True)
                total_purchases = 0
                for brand in countries[country][period]["paying"]:
                    for lang in countries[country][period]["paying"][brand]:
                        for book in countries[country][period]["paying"][brand][lang]:
                            total_purchases += countries[country][period]["paying"][brand][lang][book]
                for brand in countries[country][period]["paying"]:
                    for lang in countries[country][period]["paying"][brand]:
                        max_purchases = 0
                        max_purchases_book = None
                        for book in countries[country][period]["paying"][brand][lang]:
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

                for brand in countries[country][period]["read"]:
                    for lang in countries[country][period]["read"][brand]:
                        for book in countries[country][period]["read"][brand][lang]:
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
                '''
                for book in [book for book in countries[country][period] if is_free_book(book)]:
                        total_events += countries[country][period][book]
                for book in [book for book in countries[country][period] if is_free_book(book)]:
                        lang, brand = get_brand_lang_free_book(book)
                        value_2 = round(countries[country][period][book] * 100 / total_events,
                                        1) if total_events > 0 else 0
                        df = df.append({
                            "Price": "Free",
                            "Brand": brand,
                            "Language": lang,
                            "Value 1": str(book) + " (" + str(value_2) + "%)"
                        }, ignore_index=True)

                df = df.sort_values(by=["Price", "Brand", "Language"], ascending=False)
                '''
                total_purchases = 0
                for in_app in [in_app for in_app in countries[country][period] if is_inapp(in_app)]:
                            total_purchases += countries[country][period][in_app]
                for in_app in [in_app for in_app in countries[country][period] if is_inapp(in_app)]:
                        max_purchases = 0
                        max_purchases_book = None
                        for book in countries[country][period]["paying"][brand][lang]:
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
                '''
                #print("free done")
                for book in [book for book in countries[country][period] if not is_free_book(book)]:
                    brand, lang = get_brand_lang_book(book)
                    df_reading = df_reading.append({
                        "Brand": brand,
                        "Book": book,
                        "Lang": lang,
                        "Reading": countries[country][period][book]
                    }, ignore_index=True)
                df_reading = df_reading.sort_values(by=["Lang", "Reading"], ascending=False)
                #print("read done")
                df.to_excel(writer, str(period).replace("/", "."), index=False)
                df_reading.to_excel(writer, str(period).replace("/", "."), index=False, startrow=df.shape[0] + 2)
                writer.save()
                # print(df.to_string(index=False))
        print(OS.get_os_string(os), "done.")
