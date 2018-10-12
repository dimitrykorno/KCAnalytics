from datetime import datetime
import pandas as pd
from Classes.Events import *
from In_apps.In_apps import get_collection_category_language
from In_apps.book_names import get_book_category_language
from Classes.Events import *
from Data import Parse
from Classes.User import User
from report_api.Report import Report
from report_api.OS import OS
from report_api.Utilities.Utils import time_count

app = "kc"


@time_count
def new_report(os_list=["iOS", "Android"],
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
                               period_end=period_end,
                               min_version=min_version,
                               max_version=max_version,
                               countries_list=[],
                               events_list=[(["tap\_ buy\_%", "tap\_buy\_banner%"], "%success%"),
                                            ({"read_book_Bebebears Mimigames 1", "read_book_Bebebears Star Story",
                                              "read_book_Masha's Spooky Stories About Superstitious Girl",
                                              "read_book_Masha's Spooky Stories Games 1",
                                              "read_book_Om Nom Stories Christmas Story",
                                              "read_book_Om Nom Stories Games 1",
                                              "read_book_The Fixies Books - The Cell Phone",
                                              "read_book_The Fixies Games 1",

                                              "read_book_Ам Ням Мини-Игры 1", "read_book_Ам Ням Рождественский Выпуск",
                                              "read_book_Машкины Страшилки - Про Суеверную Девочку",
                                              "read_book_Машкины Страшилки Игры 1",
                                              "read_book_МимиМишки - Звёздное небо",
                                              "read_book_МимиМишки Игры 1",
                                              "read_book_Фиксики МиниИгры - Сотовый Телефон",
                                              "read_book_ФиксиКнижки - Сотовый Телефон",
                                              "read_book_Три Кота Игры Варенье", "read_book_Три Кота Варенье",

                                              "tap_cats_ban_mainmenu", "tap_fixiki_ban_mainmenu",
                                              "tap_mashka_ban_mainmenu", "tap_mimi_ban_mainmenu",
                                              "tap_omnom_ban_mainmenu",
                                              "tap_cellphone_ban_ru", "tap_cellphone_book_ru", "tap_cellphone_games_ru",
                                              "tap_fixies.cellphone_ban_en", "tap_fixies.cellphone_ban_ru",
                                              "tap_fixies.cellphone_book_ru",
                                              "tap_fixies.cellphone_eng_ban_en", "tap_fixies.cellphone_eng_book_en",
                                              "tap_fixies.cellphone_eng_games_en", "tap_fixies.cellphone_games_ru",
                                              "tap_mishki.starrysky_ban_en", "tap_mishki.starrysky_ban_ru",
                                              "tap_mishki.starrysky_book_en", "tap_mishki.starrysky_book_ru",
                                              "tap_mishki.starrysky_eng_ban_en",
                                              "tap_mishki.starrysky_eng_book_en", "tap_mishki.starrysky_eng_games_en",
                                              "tap_mishki.starrysky_games_en", "tap_mishki.starrysky_games_ru",
                                              "tap_omnom.christmas_ban_en", "tap_omnom.christmas_ban_ru",
                                              "tap_omnom.christmas_book_ru", "tap_omnom.christmas_eng_ban_en",
                                              "tap_omnom.christmas_eng_ban_ru", "tap_omnom.christmas_eng_book_en",
                                              "tap_omnom.christmas_eng_book_ru", "tap_omnom.christmas_eng_games_en",
                                              "tap_omnom.christmas_games_en", "tap_omnom.christmas_games_ru",
                                              "tap_spookystories.superstitiousgirl_ban_en",
                                              "tap_spookystories.superstitiousgirl_ban_ru",
                                              "tap_spookystories.superstitiousgirl_book_ru",
                                              "tap_spookystories.superstitiousgirl_eng_ban_en",
                                              "tap_spookystories.superstitiousgirl_eng_ban_ru",
                                              "tap_spookystories.superstitiousgirl_eng_book_en",
                                              "tap_spookystories.superstitiousgirl_eng_games_en",
                                              "tap_spookystories.superstitiousgirl_games_ru",
                                              "tap_starrysky_ban_ru", "tap_starrysky_book_ru",
                                              "tap_starrysky_eng_ban_en", "tap_starrysky_eng_book_en",
                                              "tap_starrysky_eng_games_en", "tap_starrysky_games_ru",
                                              "tap_superstitiousgirl_ban_ru", "tap_superstitiousgirl_book_ru",
                                              "tap_superstitiousgirl_games_ru", "tap_trikota.varenie_ban_ru",
                                              "tap_trikota.varenie_book_ru", "tap_trikota.varenie_games_ru"},)]
                               )
        # формируем таблицу отчета
        user_parameters = ["Users"]

        activity_parameters = \
            ["Read free", "Paying", "Empty 0",
             "Enter shelf mimi", "Tap mishki rus", "Read mishki rus", "Tap mishki eng", "Read mishki eng",
             "Empty 1",
             "Enter shelf mashka", "Tap spookystories rus", "Read spookystories rus", "Tap spookystories eng",
             "Read spookystories eng",
             "Empty 2",
             "Enter shelf fixiki", "Tap fixies rus", "Read fixies rus", "Tap fixies eng", "Read fixies eng",
             "Empty 3",
             "Enter shelf omnom", "Tap omnom rus", "Read omnom rus", "Tap omnom eng", "Read omnom eng",
             "Empty 4",
             "Enter shelf cats", "Tap trikota rus", "Read trikota rus"  # , "Tap trikota eng", "Read trikota eng"
             ]
        parameters = user_parameters + activity_parameters

        # Пользовательские параметры
        user_activity = dict.fromkeys(activity_parameters, 0)
        countries = {}

        # Перемещение данных пользователя в отчет
        def flush_user_info():
            if previous_country not in countries.keys():
                countries[previous_country] = dict.fromkeys(user_parameters + activity_parameters, 0)
            for param in activity_parameters:
                countries[previous_country][param] += user_activity[param]

        while Report.get_next_event():
            previous_country = Report.previous_user.country

            if Report.is_new_user():
                flush_user_info()
                user_activity = dict.fromkeys(activity_parameters, 0)

            if Report.current_event.__class__ is KC_TapShelf:
                user_activity[Report.current_event.to_string()] = 1

            elif Report.current_event.__class__ is KC_TapBook:
                brand, lang = get_collection_category_language(Report.current_event.obj_name)
                user_activity["Tap " + brand + " " + lang] = 1

            elif Report.current_event.__class__ is KC_ReadFree:
                brand, lang = get_book_category_language(Report.current_event.obj_name)
                user_activity["Read " + brand + " " + lang] = 1
                user_activity["Read free"] = 1

            elif Report.current_event.__class__ is KC_BuyEvent:
                user_activity["Paying"] = 1

        flush_user_info()

        for country in countries.keys():
            for install in Report.get_installs():
                if install["country_iso_code"]==country:
                    countries[country]["Users"]+=1

        df = pd.DataFrame(index=list(countries.keys()), columns=parameters)
        old_percent = 0
        enter_shelf_percent = 0
        # рисуем проценты
        for country in countries.keys():
            df.at[country, "Users"] = countries[country]["Users"]
            for param in activity_parameters:
                new_percent = round(countries[country][ param] * 100 / df.at[country, "Users"], 1)
                if "Enter" in param:
                    enter_shelf_percent = new_percent
                if "Tap" in param:
                    old_percent = enter_shelf_percent
                difference = ""
                if not ("Enter" in param or "free" in param or "Paying" in param):
                    difference = " (-" + str(round(abs(old_percent - new_percent), 1)) + "%)"
                df.at[country, param] = str(countries[country][ param]) + " (" + str(
                    round(countries[country][ param] * 100 / df.at[country, "Users"], 1)) + "%)" + difference
                old_percent = new_percent
                if "Empty" in param:
                    df.loc[country, param] = " " * 5
        df = df.sort_values(by=["Users"], ascending=False)
        writer = pd.ExcelWriter("UserActivity/" + OS.get_os_string(os) + " " + "UserActivity.xlsx")
        df.to_excel(writer, str(period_start) + "-" + str(period_end))
        writer.save()

        print(df.to_string())
