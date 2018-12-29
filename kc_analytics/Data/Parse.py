from Classes.Events import *
from In_apps.Shop import is_free_book, get_price
from report_api.Report import Report
from report_api.Utilities.Utils import time_medium_2


@time_medium_2
def parse_event(event_name, event_json=None, datetime=None):
    # парсинг событий чтения
    # if re.match(r'^read_book_.+', event_name):
    if event_name.startswith('read_book_'):
        book = event_name[10:]
        if is_free_book(book):
            return KCReadFree(book, datetime)
        return KCReadEvent(book, datetime)

    elif "subscription" in event_name:
        return KCSubStart(sub_name=event_name[30:], datetime=datetime)

        # парсинг событий входа на полку
    # elif re.match(r'.+_ban_mainmenu', event_name):
    elif event_name.endswith('_ban_mainmenu'):
        return KCTapShelf(event_name[4:-13], datetime)

    # парсинг событий тапа по книге
    elif event_name[-7:] in ("_ban_ru", "_ban_en"):
        return KCTapBook(event_name[4:-7], datetime)
    elif event_name[-8:] in ("_book_ru", "_book_en"):
        return KCTapBook(event_name[4:-8], datetime)
    elif event_name[-9:] in ("_games_ru", "_games_en"):
        return KCTapBook(event_name[4:-9], datetime)

    # парсинг событий покупки
    elif event_name.startswith('tap_ buy_'):

        if event_json == '{"status":"success"}':
            return KCBuyEvent(purchase=event_name[9:], datetime=datetime, status="Success",
                              price=get_price(event_name[9:]))
        elif event_json == '{"status":"canceled"}':
            return KCBuyCancel(purchase=event_name[9:], datetime=datetime, status="Cancel",
                               price=get_price(event_name[9:]))
        elif event_json == '{"status":"failed"}':
            return KCBuyFailed(purchase=event_name[9:], datetime=datetime, status="Fail",
                               price=get_price(event_name[9:]))
        elif event_json == '{"status":"tap"}':
            return KCBuyTap(bought_object=event_name[9:], datetime=datetime)
        elif not event_json:
            return KCBuyEvent(purchase=event_name[9:], datetime=datetime, status="NoJSON",
                              price=get_price(event_name[9:]))

    # парсинг событий покупки с баннера
    elif event_name.startswith('tap_buy_banner_'):

        if not event_json:
            return KCBuyEvent(purchase=event_name[15:], datetime=datetime, status="NoJSON",
                              price=get_price(event_name[15:]))
        elif event_json == '{"status":"canceled"}':
            return KCBuyCancel(purchase=event_name[15:], datetime=datetime, status="Cancel",
                               price=get_price(event_name[15:]))
        elif event_json == '{"status":"failed"}':
            return KCBuyFailed(purchase=event_name[15:], datetime=datetime, status="Fail",
                               price=get_price(event_name[15:]))
        elif event_json == '{"status":"tap"}':
            return KCBuyTap(bought_object=event_name[15:], datetime=datetime)
        elif event_json == '{"status":"success"}':
            return KCBuyEvent(purchase=event_name[15:], datetime=datetime, status="Success",
                              price=get_price(event_name[15:]))

    elif event_name == 'parent_gate_passed':
        return KCParentGate(datetime)



    # парсинг событий сбора подарка
    elif event_name == "Tap_present":
        return KCTapPresent(datetime)

    else:
        if event_name in ("enter_mishki_from_Mult", "enter_mashka_from_JamDay"):
            return KCEvent(event_name, datetime)
        Report.Report.not_found.add("Event not found: " + event_name + " json: " + event_json)
        return KCEvent(event_name, datetime)
