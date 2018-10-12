from Classes.Events import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count, daterange, draw_plot, week_of_month
from datetime import datetime
from In_apps.In_apps import *
import pandas as pd
from dateutil import rrule
app = "kc"

@time_count
def new_report(os_list=[ "iOS","Android"],
               after_release_months_graphs=None,
               period_start="2018-06-19",
               period_end=None,
               min_version=None,
               max_version=None,
               countries_list=[]):
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
                               events_list=[(["tap\_ buy\_%", "tap\_buy\_banner%"], "%success%")])

        # общие продажи по дням недели
        def get_week(my_date):
            '''
            Разница между датой и началом периода в неделях
            :param my_date: дата, недели до которой нужно посчитать
            :return:
            '''
            weeks = rrule.rrule(rrule.WEEKLY, dtstart=period_start, until=my_date)
            return weeks.count()

        def get_week_after_first_purchase(my_date, first_purchase_date):
            '''
            Разница между датой и началом периода в неделях
            :param my_date: дата, недели до которой нужно посчитать
            :return:
            '''
            weeks = rrule.rrule(rrule.WEEKLY, dtstart=first_purchase_date, until=my_date).count()
            if weeks < after_release_months_graphs * 4:
                return weeks
            else:
                return

        X_days_sales = []
        X_weeks_sales = [0]
        X_week_labels = []
        if after_release_months_graphs:
            X_weeks_after_first_purchase = list(range(after_release_months_graphs * 4))
        previous_week = 1
        week_added = False

        for d in daterange(period_start, period_end):
            X_days_sales.append(str(d.day) + "." + str(d.month))
            week = get_week(d)
            month = d.strftime("%m/%y")
            if previous_week and week != previous_week:
                week_added = False
            #if previous_month and month != previous_month:
            #    week_label = 1
            #previous_month = month
            previous_week = week
            week_label=week_of_month(d)

            week_month = str(week_label) + "." + str(month)
            if not week_added and week_month not in X_week_labels:
                X_week_labels.append(week_month)
                week_added = True
            if week not in X_weeks_sales:
                X_weeks_sales.append(week)
        Y_past_sales = [0] * len(X_days_sales)
        Y_past_money = [0] * len(X_days_sales)

        # уникальные инаппы (исправленные названия)
        unique_inapps_rus = get_in_apps_list(language="rus")
        unique_inapps_eng = get_in_apps_list(language="eng")
        in_app_locales = {"rus": unique_inapps_rus, "eng": unique_inapps_eng}

        # день первой покупки каждого инаппа
        first_purchase_rus = dict.fromkeys(unique_inapps_rus, None)
        first_purchase_eng = dict.fromkeys(unique_inapps_eng, None)
        first_purchase_locales = {"rus": first_purchase_rus, "eng": first_purchase_eng}

        # формируем таблицу отчета
        parameters = ["Brand", "First purchase", "Price", "Revenue", "Sales"]
        df_rus = pd.DataFrame(index=unique_inapps_rus, columns=parameters)
        df_eng = pd.DataFrame(index=unique_inapps_eng, columns=parameters)
        df_locales = {"rus": df_rus, "eng": df_eng}

        # заполняем таблицы инфой об инаппах
        for locale in df_locales.keys():
            for in_app in in_app_locales[locale]:
                df_locales[locale].at[in_app, "Brand"] = get_inapp_category(in_app)
                df_locales[locale].at[in_app, "Price"] = get_price(in_app)
                df_locales[locale].fillna(0, inplace=True)

        months_list = []
        brands_list = get_brands_list()
        if after_release_months_graphs:
            Y_inapps_this_period = {}
            Y_inapps_after_start = {}
            for X, Y in zip([X_weeks_sales, X_weeks_after_first_purchase],
                            [Y_inapps_this_period, Y_inapps_after_start]):
                for brand in brands_list:
                    for pack in (True, False):
                        for lang in ("rus", "eng"):
                            in_app_list = get_in_apps_list(brand=brand, pack=pack, language=lang)
                            if in_app_list:
                                Y[(brand, pack, lang)] = dict.fromkeys(in_app_list)
                                for in_app in in_app_list:
                                    Y[(brand, pack, lang)][in_app] = [0] * len(X)

        while Report.get_next_event():

            in_app = check_inapp_name(Report.current_event.obj_name)
            purchase_date = Report.current_event.datetime.date()
            month = Report.current_event.datetime.strftime("%m/%y")
            brand = get_inapp_category(in_app)
            pack = is_pack(in_app)
            lang = get_inapp_language(in_app)

            unique_inapps, first_purchase, df = in_app_locales[lang], first_purchase_locales[lang], df_locales[lang]

            if str(df.at[in_app, "First purchase"]) == "nan":
                df.at[in_app, "First purchase"] = purchase_date

            if month not in list(df):
                for loc in df_locales.keys():
                    if month not in list(df_locales[loc]):
                        df_locales[loc].insert(loc=len(list(df_locales[loc])), column=month,
                                               value=[0] * len(in_app_locales[loc]))
                if month not in months_list:
                    months_list.append(month)

            df.at[in_app, month] += 1

            if after_release_months_graphs:
                # Графики
                # график спроса на инаппы по неделям
                Y_inapps_this_period[(brand, pack, lang)][in_app][get_week(purchase_date)] += 1
                # график спроса на инаппы по неделям с момента выхода
                week = get_week_after_first_purchase(purchase_date, df.at[in_app, "First purchase"])
                if week:
                    Y_inapps_after_start[(brand, pack, lang)][in_app][week] += 1
                # график общего спроса и дохода по дням
                Y_past_sales[X_days_sales.index(str(purchase_date.day) + "." + str(purchase_date.month))] += 1
                Y_past_money[X_days_sales.index(str(purchase_date.day) + "." + str(purchase_date.month))] += get_price(in_app)

        writer = pd.ExcelWriter("Result_Sales/Sales"+os_str+".xlsx")
        months_list=sorted(months_list)
        # по каждой таблице
        for locale in df_locales.keys():
            df = df_locales[locale]
            df["First purchase"].fillna(0, inplace=True)
            df["First purchase"].replace(0, "", inplace=True)
            # считаем общие продажи и выручку и сортируем
            print(locale)
            df["Sales"] = df[months_list].sum(axis=1)
            df["Revenue"] = df["Sales"] * df["Price"]
            df.sort_values(by=["Brand", "Sales"], ascending=False, inplace=True)
            df=df[parameters+months_list]
            print(df.to_string() + "\n")

            # Сохраняем в Excel
            df.to_excel(writer, sheet_name= locale.upper())
        writer.save()

        if after_release_months_graphs:
            for X, Y, labels in zip([X_weeks_sales, X_weeks_after_first_purchase],
                                    [Y_inapps_this_period, Y_inapps_after_start],
                                    [X_week_labels, None]):
                folder = "Result_AfterRelease/" if Y == Y_inapps_after_start else "Result_Sales/"

                for brand in brands_list:
                    for pack in (True, False):
                        for lang in ("rus", "eng"):
                            if (brand, pack, lang) in Y.keys():
                                p = "pack" if pack else "solo"
                                title = str(OS.get_os_string(Report.os)) + "." + lang + "." + brand + "." + p
                                xticks_move = 0 if labels else 1
                                draw_plot(X, Y[(brand, pack, lang)], xtick_steps=1, xticks_move=xticks_move,
                                          x_ticks_labels=labels, title=title, folder=folder)
