from In_apps.Shop import check_inapp_name, get_price
from report_api.Classes.Events import *


class KCEvent(Event):
    __slots__ = 'obj_name'

    def __init__(self, obj_name, datetime):
        super().__init__(datetime)
        self.obj_name = obj_name

    def to_string(self):
        return "Other event: " + str(self.obj_name)


class KCReadEvent(KCEvent):
    def __init__(self, book_name, datetime):
        super().__init__(book_name, datetime)

    def to_string(self):
        return "Read Event:  " + self.obj_name


class KCReadFree(KCEvent):
    def __init__(self, book_name, datetime):
        super().__init__(book_name, datetime)

    def to_string(self):
        return "Read Free:   " + self.obj_name


class KCBuyEvent(PurchaseEvent):
    def __init__(self, purchase, price, status, datetime):
        super().__init__(check_inapp_name(purchase), status, price, datetime)

    def to_string(self):
        return "Buy Event:   " + self.purchase


class KCBuyCancel(PurchaseEvent):
    def __init__(self, purchase, price, status, datetime):
        super().__init__(check_inapp_name(purchase), status, price, datetime)

    def to_string(self):
        return "Buy Cancel:  " + self.purchase


class KCBuyFailed(PurchaseEvent):
    def __init__(self, purchase, price, status, datetime):
        super().__init__(check_inapp_name(purchase), status, price, datetime)

    def to_string(self):
        return "Buy Failed:  " + self.purchase


class KCBuyTap(KCEvent):
    def __init__(self, bought_object, datetime):
        super().__init__(check_inapp_name(bought_object), datetime)

    def to_string(self):
        return "Buy Tap:     " + self.obj_name


class KCTapShelf(KCEvent):
    def __init__(self, shelf, datetime):
        super().__init__(shelf, datetime)

    def to_string(self):
        return "Enter shelf " + self.obj_name


class KCTapPresent(Event):
    def __init__(self, datetime):
        super().__init__(datetime)

    def to_string(self):
        return "Tap Present"


class KCTapBook(KCEvent):
    def __init__(self, book_name, datetime):
        super().__init__(check_inapp_name(book_name), datetime)

    def to_string(self):
        return "Tap Book:    " + self.obj_name


class KCParentGate(Event):
    def __init__(self, datetime):
        super().__init__(datetime)

    def to_string(self):
        return "Parent gate"


class KCCRASH(Event):
    def __init__(self, datetime):
        super().__init__(datetime)
