try:
    import ujson as json
except ImportError:
    print("No ujson found. Using json.")
    import json
from Classes.Events_2 import *
from report_api.Report import Report
from report_api.Utilities.Utils import time_medium_2
import traceback
from report_api import Report


def parse_event(event_name, event_json, datetime):
    try:
        parameters = json.loads(event_json)
    except ValueError:
        Report.Report.not_found.add("Json error:" + event_name + " " + event_json)
        return None
    except Exception as er:
        print("parse error", er.args)
        print(event_name, event_json)

        return None
    try:
        # попытка парсинга события
        new_event = start_parse(event_name, parameters, datetime)
        # найденная ошибка в событии/неправильно сформулированное событие
        if new_event is False:
            return None
            # В KIDS CORNER ПОКА НЕТ АБ-ТЕСТОВ И НЕИЗВЕСТНО В КАКОЙ ФОРМЕ ОНИ БУДУТ ПРОХОДИТЬ
            # if new_event is None:
            #     # Если имя события неизвестно, то это тест.
            #     test_name = event_name
            #     event_name = list(parameters)[0]
            #     parameters = parameters[event_name]
            #     new_event = start_parse(event_name, parameters, datetime)
            #     if new_event is False:
            #         return None
            #     if not new_event:
            #         raise ValueError("Event parse: Unknown event name:", event_name, datetime, " May be a test:", test_name)
            #     new_event.set_ab_test_name(test_name)

    except Exception as er:

        Report.Report.not_found.add(str(er.args) + " Error: " + event_name + " Json: " + event_json)
        Report.Report.not_found.add(str(traceback.extract_stack()))
        print(er.args)
        return

    return new_event


def start_parse(event_name, parameters, datetime):
    if event_name == "InitGameState":
        return parse_InitGameState(parameters, datetime)
    elif event_name == "TapSection":
        return parse_TapSection(parameters, datetime)
    elif event_name == "EnterSection":
        return parse_EnterSection(parameters, datetime)
    elif event_name == "TapShop":
        return parse_TapShop(parameters, datetime)
    elif event_name == "TapBook":
        return parse_TapBook(parameters, datetime)
    elif event_name == "DownloadStart":
        return parse_DownloadStart(parameters, datetime)
    elif event_name == "DownloadFinish":
        return parse_DownloadFinish(parameters, datetime)
    elif event_name == "DownloadCancel":
        return parse_DownloadCancel(parameters, datetime)
    elif event_name == "DeleteBook":
        return parse_DeleteBook(parameters, datetime)
    elif event_name == "FavouriteAdd":
        return parse_FavouriteAdd(parameters, datetime)
    elif event_name == "FavouriteDelete":
        return parse_FavouriteDelete(parameters, datetime)
    elif event_name == "FavouriteShow":
        return parse_FavouriteShow(parameters, datetime)
    elif event_name == "FavouriteReturn":
        return parse_FavouriteReturn(parameters, datetime)
    elif event_name == "TapSearch":
        return parse_TapSearch(parameters, datetime)
    elif event_name == "TapSearchSuccess":
        return parse_TapSearchSuccess(parameters, datetime)
    elif event_name == "TapTryBook":
        return parse_TapTryBook(parameters, datetime)
    elif event_name == "TapAddCoins":
        return parse_TapAddCoins(parameters, datetime)
    elif event_name == "OpenBook":
        return parse_OpenBook(parameters, datetime)
    elif event_name == "EnterPage":
        return parse_EnterPage(parameters, datetime)
    elif event_name == "EnterGame":
        return parse_EnterGame(parameters, datetime)
    elif event_name == "ExitGame":
        return parse_ExitGame(parameters, datetime)
    elif event_name == "EnterFromSummary":
        return parse_EnterFromSummary(parameters, datetime)
    elif event_name == "TapLike":
        return parse_TapLike(parameters, datetime)
    elif event_name == "TapBuyCoins":
        return parse_TapBuyCoins(parameters, datetime)
    elif event_name == "TapBuyBookForMoney":
        return parse_TapBuyBookForMoney(parameters, datetime)
    elif event_name == "TapBuyBookForCoins":
        return parse_TapBuyBookForCoins(parameters, datetime)
    elif event_name == "TapBuyStore":
        return parse_TapBuyStore(parameters, datetime)
    elif event_name == "TapSubscribe":
        return parse_TapSubscribe(parameters, datetime)
    elif event_name == "SubscriptionPaymentFromServer":
        return parse_SubscriptionPaymentFromServer(parameters, datetime)
    elif event_name == "SubscriptionDiscardFromServer":
        return parse_SubscriptionDiscardFromServer(parameters, datetime)
    elif event_name == "EnterShopBrand":
        return parse_EnterShopBrand(parameters, datetime)
    elif event_name == "TapInApp":
        return parse_TapInApp(parameters, datetime)
    elif event_name == "TapTrialFromBook":
        return parse_TapTrialFromBook(parameters, datetime)
    elif event_name == "TapTrialFromShop":
        return parse_TapTrialFromShop(parameters, datetime)
    elif event_name == "EnterSubscriptions":
        return parse_EnterSubscriptions(parameters, datetime)
    elif event_name == "TapTrialFromAirship":
        return parse_TapTrialFromAirship(parameters, datetime)
    elif event_name == "SettingsEnterSubscriptions":
        return parse_SettingsEnterSubscriptions(parameters, datetime)
    elif event_name == "SettingsChangeSubscription":
        return parse_SettingsChangeSubscription(parameters, datetime)
    elif event_name == "SettingsChangeLoc":
        return parse_SettingsChangeLoc(parameters, datetime)
    elif event_name == "SettingsTapRestore":
        return parse_SettingsTapRestore(parameters, datetime)
    elif event_name == "SettingsRestore":
        return parse_SettingsRestore(parameters, datetime)
    elif event_name == "SettingsShowQuestion":
        return parse_SettingsShowQuestion(parameters, datetime)
    elif event_name == "SettingsTapLike":
        return parse_SettingsTapLike(parameters, datetime)
    elif event_name == "ParentGatePassed":
        return parse_ParentGatePassed(parameters, datetime)
    elif event_name == "SettingsTapAuthorization":
        return parse_SettingsTapAuthorization(parameters, datetime)
    elif event_name == "SettingsTryLogIn":
        return parse_SettingsTryLogIn(parameters, datetime)
    elif event_name == "SettingsTryRegister":
        return parse_SettingsTryRegister(parameters, datetime)
    else:
        return None


def parse_InitGameState(parameters, datetime):
    return InitGameState(
        snum=int(parameters["snum"]),
        mishki_subs=parameters["mishki_subs"],
        fixiki_subs=parameters["fixiki_subs"],
        mashka_subs=parameters["mashka_subs"],
        omnom_subs=parameters["omnom_subs"],
        trikota_subs=parameters["trikota_subs"],
        coins_balance=int(parameters["coins_balance"]),
        interface_loc=parameters["interface_loc"],
        datetime=datetime
    )


def parse_TapSection(parameters, datetime):
    return TapSection(
        section=parameters["section"],
        brand_subs=parameters["brand_subs"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_EnterSection(parameters, datetime):
    return EnterSection(
        section=parameters["section"],
        brand=parameters["brand"],
        brand_subs=parameters["brand_subs"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapShop(parameters, datetime):
    return TapShop(
        section=parameters["section"],
        brand=parameters["brand"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapBook(parameters, datetime):
    return TapBook(
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        downloaded=parameters["downloaded"],
        section=parameters["section"],
        brand=parameters["brand"],
        price=parameters["price"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_DownloadStart(parameters, datetime):
    return DownloadStart(
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        section=parameters["section"],
        brand=parameters["brand"],
        button=parameters["button"],
        size=parameters["size"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_DownloadFinish(parameters, datetime):
    return DownloadFinish(
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        brand=parameters["brand"],
        size=parameters["size"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_DownloadCancel(parameters, datetime):
    return DownloadCancel(
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        brand=parameters["brand"],
        size=parameters["size"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_DeleteBook(parameters, datetime):
    return DeleteBook(
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        brand=parameters["brand"],
        size=parameters["size"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_FavouriteAdd(parameters, datetime):
    return FavouriteAdd(
        book_name=parameters["book_name"],
        section=parameters["section"],
        brand=parameters["brand"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_FavouriteDelete(parameters, datetime):
    return FavouriteDelete(
        book_name=parameters["book_name"],
        section=parameters["section"],
        brand=parameters["brand"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_FavouriteShow(parameters, datetime):
    return FavouriteShow(
        section=parameters["section"],
        brand=parameters["brand"],
        quantity=int(parameters["quantity"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_FavouriteReturn(parameters, datetime):
    return FavouriteReturn(
        section=parameters["section"],
        brand=parameters["brand"],
        quantity=int(parameters["quantity"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapSearch(parameters, datetime):
    return TapSearch(
        section=parameters["section"],
        brand=parameters["brand"],
        quantity=int(parameters["quantity"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapSearchSuccess(parameters, datetime):
    return TapSearchSuccess(
        section=parameters["section"],
        brand=parameters["brand"],
        quantity=int(parameters["quantity"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapTryBook(parameters, datetime):
    return TapTryBook(
        book_name=parameters["book_name"],
        section=parameters["section"],
        brand=parameters["brand"],
        price_money=parameters["price_money"],
        price_coins=parameters["price_coins"],
        coins_balance=int(parameters["coins_balance"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapAddCoins(parameters, datetime):
    return TapAddCoins(
        book_name=parameters["book_name"],
        section=parameters["section"],
        brand=parameters["brand"],
        price_money=parameters["price_money"],
        price_coins=parameters["price_coins"],
        coins_balance=int(parameters["coins_balance"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_OpenBook(parameters, datetime):
    return OpenBook(
        brand=parameters["brand"],
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        snum=int(parameters["snum"]),
        price_money=parameters["price_money"],
        price_coins=parameters["price_coins"],
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_EnterPage(parameters, datetime):
    return EnterPage(
        brand=parameters["brand"],
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        page=int(parameters["page"]),
        time=int(parameters["time"]),
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_EnterGame(parameters, datetime):
    return EnterGame(
        brand=parameters["brand"],
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        page=int(parameters["page"]),
        time=int(parameters["time"]),
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_ExitGame(parameters, datetime):
    return ExitGame(
        brand=parameters["brand"],
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        page=int(parameters["page"]),
        time=int(parameters["time"]),
        errors=parameters["errors"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_EnterFromSummary(parameters, datetime):
    return EnterFromSummary(
        brand=parameters["brand"],
        book_name=parameters["book_name"],
        unlocked=parameters["unlocked"],
        page=int(parameters["page"]),
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_TapLike(parameters, datetime):
    return TapLike(
        brand=parameters["brand"],
        book_name=parameters["book_name"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_TapBuyCoins(parameters, datetime):
    return TapBuyCoins(
        purchase=parameters["purchase"],
        section=parameters["section"],
        brand=parameters["brand"],
        coins_balance=int(parameters["coins_balance"]),
        book_name=parameters["book_name"],
        price_money=parameters["price_money"],
        status=parameters["status"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_TapBuyBookForMoney(parameters, datetime):
    return TapBuyBookForMoney(
        brand=parameters["brand"],
        purchase=parameters["purchase"],
        book_name=parameters["book_name"],
        price_money=parameters["price_money"],
        price_coins=parameters["price_coins"],
        section=parameters["section"],
        coins_balance=int(parameters["coins_balance"]),
        status=parameters["status"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_TapBuyBookForCoins(parameters, datetime):
    return TapBuyBookForCoins(
        brand=parameters["brand"],
        purchase=parameters["purchase"],
        book_name=parameters["book_name"],
        price_money=parameters["price_money"],
        price_coins=parameters["price_coins"],
        section=parameters["section"],
        coins_balance=int(parameters["coins_balance"]),
        status=parameters["status"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_TapBuyStore(parameters, datetime):
    return TapBuyStore(
        brand=parameters["brand"],
        purchase=parameters["purchase"],
        price_money=parameters["price_money"],
        status=parameters["status"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_TapSubscribe(parameters, datetime):
    return TapSubscribe(
        brand=parameters["brand"],
        subscription=parameters["subscription"],
        trial=int(parameters["trial"]),
        price_money=parameters["price_money"],
        status=parameters["status"],
        snum=int(parameters["snum"]),
        lang=parameters["lang"],
        datetime=datetime
    )


def parse_SubscriptionPaymentFromServer(parameters, datetime):
    return SubscriptionPaymentFromServer(
        brand=parameters["brand"],
        subscription=parameters["subscription"],
        price_money=parameters["price_money"],
        history=int(parameters["history"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SubscriptionDiscardFromServer(parameters, datetime):
    return SubscriptionDiscardFromServer(
        brand=parameters["brand"],
        subscription=parameters["subscription"],
        price_money=parameters["price_money"],
        history=int(parameters["history"]),
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_EnterShopBrand(parameters, datetime):
    return EnterShopBrand(
        brand=parameters["brand"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapInApp(parameters, datetime):
    return TapInApp(
        brand=parameters["brand"],
        inapp=parameters["inapp"],
        price=parameters["price"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapTrialFromBook(parameters, datetime):
    return TapTrialFromBook(
        book_name=parameters["book_name"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapTrialFromShop(parameters, datetime):
    return TapTrialFromShop(
        section=parameters["section"],
        brand=parameters["brand"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_EnterSubscriptions(parameters, datetime):
    return EnterSubscriptions(
        from_par=parameters["from_par"],
        brand=parameters["brand"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_TapTrialFromAirship(parameters, datetime):
    return TapTrialFromAirship(
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsEnterSubscriptions(parameters, datetime):
    return SettingsEnterSubscriptions(
        mishki_subs=parameters["mishki_subs"],
        fixiki_subs=parameters["fixiki_subs"],
        mashka_subs=parameters["mashka_subs"],
        omnom_subs=parameters["omnom_subs"],
        from_par=parameters["from_par"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsChangeSubscription(parameters, datetime):
    return SettingsChangeSubscription(
        sub=parameters["sub"],
        from_par=parameters["from_par"],
        to_par=parameters["to_par"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsChangeLoc(parameters, datetime):
    return SettingsChangeLoc(
        interface_loc=parameters["interface_loc"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsTapRestore(parameters, datetime):
    return SettingsTapRestore(
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsRestore(parameters, datetime):
    return SettingsRestore(
        status=parameters["status"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsShowQuestion(parameters, datetime):
    return SettingsShowQuestion(
        num=parameters["num"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsTapLike(parameters, datetime):
    return SettingsTapLike(
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_ParentGatePassed(parameters, datetime):
    return ParentGatePassed(
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsTapAuthorization(parameters, datetime):
    return SettingsTapAuthorization(
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsTryLogIn(parameters, datetime):
    return SettingsTryLogIn(
        status=parameters["status"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )


def parse_SettingsTryRegister(parameters, datetime):
    return SettingsTryRegister(
        status=parameters["status"],
        snum=int(parameters["snum"]),
        datetime=datetime
    )
