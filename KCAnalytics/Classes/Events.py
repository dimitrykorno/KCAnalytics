from In_apps.In_apps import check_inapp_name, get_price


class Event:
    not_found = set()

    def __init__(self, obj_name, datetime):
        self.obj_name = obj_name
        self.datetime = datetime

    def to_string(self):
        return "Other event: " + str(self.obj_name)


class KC_ReadEvent(Event):
    def __init__(self, book_name, datetime):
        Event.__init__(self, book_name, datetime)

    def to_string(self):
        return "Read Event:  " + self.obj_name


class KC_ReadFree(Event):
    def __init__(self, book_name, datetime):
        Event.__init__(self, book_name, datetime)

    def to_string(self):
        return "Read Free:   " + self.obj_name


class KC_BuyEvent(Event):
    def __init__(self, bought_object, datetime):
        Event.__init__(self, check_inapp_name(bought_object), datetime)

    @property
    def price(self):
        return get_price(self.obj_name)

    def to_string(self):
        return "Buy Event:   " + self.obj_name


class KC_BuyCancel(Event):
    def __init__(self, bought_object, datetime):
        Event.__init__(self, check_inapp_name(bought_object), datetime)

    @property
    def price(self):
        return get_price(self.obj_name)

    def to_string(self):
        return "Buy Cancel:  " + self.obj_name


class KC_BuyFailed(Event):
    def __init__(self, bought_object, datetime):
        Event.__init__(self, check_inapp_name(bought_object), datetime)

    @property
    def price(self):
        return get_price(self.obj_name)

    def to_string(self):
        return "Buy Failed:  " + self.obj_name


class KC_BuyTap(Event):
    def __init__(self, bought_object, datetime):
        Event.__init__(self, check_inapp_name(bought_object), datetime)

    def to_string(self):
        return "Buy Tap:     " + self.obj_name


class KC_TapShelf(Event):
    def __init__(self, shelf, datetime):
        Event.__init__(self, shelf, datetime)

    def to_string(self):
        return "Enter shelf " + self.obj_name


class KC_TapPresent(Event):
    def __init__(self, datetime):
        Event.__init__(self, "Tap_present", datetime)

    def to_string(self):
        return "Get Present: " + self.obj_name


class KC_TapBook(Event):
    def __init__(self, book_name, datetime):
        Event.__init__(self, check_inapp_name(book_name), datetime)

    def to_string(self):
        return "Tap Book:    " + self.obj_name


class KC_ParentGate(Event):
    def __init__(self, datetime):
        Event.__init__(self, "Parent_gate", datetime)

    def to_string(self):
        return "Parent gate: " + self.obj_name


class KC_CRASH(Event):
    def __init__(self, datetime):
        Event.__init__(self, "CRASH EVENT", datetime)
