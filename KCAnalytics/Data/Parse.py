from Classes.Events import *
import re
from In_apps.Shop import is_free_book, get_price
from report_api.Report import Report


# @time_medium
def parse_event(event_name, event_json=None, datetime=None):
    # парсинг событий чтения
    if re.match(r'^read_book_.+', event_name):
        if is_free_book(event_name[10:]):
            return KCReadFree(event_name[10:], datetime)
        return KCReadEvent(event_name[10:], datetime)

        # парсинг событий входа на полку
    elif re.match(r'.+_ban_mainmenu', event_name):
        return KCTapShelf(event_name[4:-13], datetime)

    # парсинг событий тапа по книге
    elif re.match(r'^tap_.+_ban_.+', event_name):
        return KCTapBook(event_name[4:-7], datetime)
    elif re.match(r'tap_.+_book_.+', event_name):
        return KCTapBook(event_name[4:-8], datetime)
    elif re.match(r'tap_.+_games_.+', event_name):
        return KCTapBook(event_name[4:-9], datetime)



    # парсинг событий покупки с баннера
    elif re.match(r'^tap_buy_banner_.+', event_name):

        if not event_json:
            return KCBuyEvent(purchase=event_name[15:], datetime=datetime, status="NoJSON",
                              price=get_price(event_name[15:]))
        elif re.match(r'.*cancel.*', event_json):
            return KCBuyCancel(purchase=event_name[15:], datetime=datetime, status="NoJSON",
                               price=get_price(event_name[15:]))
        elif re.match(r'.*failed.*', event_json):
            return KCBuyFailed(purchase=event_name[15:], datetime=datetime, status="NoJSON",
                               price=get_price(event_name[15:]))
        elif re.match(r'.*tap.*', event_json):
            return KCBuyTap(bought_object=event_name[15:], datetime=datetime)
        elif re.match(r'.*success.*', event_json):
            return KCBuyEvent(purchase=event_name[15:], datetime=datetime, status="NoJSON",
                              price=get_price(event_name[15:]))

    # парсинг событий покупки
    elif re.match(r'^tap_ buy_.+', event_name):

        if not event_json:
            return KCBuyEvent(purchase=event_name[9:], datetime=datetime, status="NoJSON",
                              price=get_price(event_name[9:]))
        elif re.match(r'.*cancel.*', event_json):
            return KCBuyCancel(purchase=event_name[9:], datetime=datetime, status="NoJSON",
                               price=get_price(event_name[9:]))
        elif re.match(r'.*failed.*', event_json):
            return KCBuyFailed(purchase=event_name[9:], datetime=datetime, status="NoJSON",
                               price=get_price(event_name[9:]))
        elif re.match(r'.*tap.*', event_json):
            return KCBuyTap(bought_object=event_name[9:], datetime=datetime)
        elif re.match(r'.*success.*', event_json):
            return KCBuyEvent(purchase=event_name[9:], datetime=datetime, status="NoJSON",
                              price=get_price(event_name[9:]))

    elif event_name == 'parent_gate_passed':
        return KCParentGate(datetime)

    # парсинг событий сбора подарка
    elif re.match(r'^Tap_present', event_name):
        return KCTapPresent(datetime)

    else:
        if event_name in ("enter_mishki_from_Mult", "enter_mashka_from_JamDay"):
            return KCEvent(event_name, datetime)
        Report.Report.not_found.add("Event not found: " + event_name + " json: " + event_json)
        return KCEvent(event_name, datetime)
