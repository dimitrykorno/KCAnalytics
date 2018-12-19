from report_api.Classes.Events import *


class KCEvent(Event):
    __slots__ = 'obj_name'

    def __init__(self, snum, datetime):
        super().__init__(datetime)
        self.snum = snum


class InitGameState(KCEvent):
    __slots__ = 'mishki_subs', 'fixiki_subs', 'mashka_subs', 'omnom_subs', 'trikota_subs', 'coins_balance', \
                'interface_loc'

    def __init__(self, snum,
                 mishki_subs, fixiki_subs, mashka_subs, omnom_subs, trikota_subs,
                 coins_balance, interface_loc, datetime):
        super().__init__(snum, datetime)
        self.mishki_subs = mishki_subs
        self.fixiki_subs = fixiki_subs
        self.mashka_subs = mashka_subs
        self.omnom_subs = omnom_subs
        self.trikota_subs = trikota_subs
        self.coins_balance = coins_balance
        self.interface_loc = interface_loc


class TapSection(KCEvent):
    __slots__ = 'section', 'brand_subs'

    def __init__(self, section, brand_subs, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand_subs = brand_subs


class EnterSection(KCEvent):
    __slots__ = 'section', 'brand', 'brand_subs'

    def __init__(self, section, brand, brand_subs, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand
        self.brand_subs = brand_subs


class TapShop(KCEvent):
    __slots__ = 'section', 'brand'

    def __init__(self, section, brand, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand


class TapBook(KCEvent):
    __slots__ = 'book_name', 'unlocked', 'downloaded', 'section', 'brand', 'price'

    def __init__(self, book_name, unlocked, downloaded, section, brand, price, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.unlocked = unlocked
        self.downloaded = downloaded
        self.section = section
        self.brand = brand
        self.price = price


class DownloadStart(KCEvent):
    __slots__ = 'book_name', 'unlocked', 'section', 'brand', 'button', 'size'

    def __init__(self, book_name, unlocked, section, brand, button, size, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.unlocked = unlocked
        self.section = section
        self.brand = brand
        self.button = button
        self.size = size


class DownloadFinish(KCEvent):
    __slots__ = 'book_name', 'unlocked', 'brand', 'size'

    def __init__(self, book_name, unlocked, brand, size, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.unlocked = unlocked
        self.brand = brand
        self.size = size


class DownloadCancel(KCEvent):
    __slots__ = 'book_name', 'unlocked', 'brand', 'size'

    def __init__(self, book_name, unlocked, brand, size, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.unlocked = unlocked
        self.brand = brand
        self.size = size


class DeleteBook(KCEvent):
    __slots__ = 'book_name', 'unlocked', 'brand', 'size'

    def __init__(self, book_name, unlocked, brand, size, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.unlocked = unlocked
        self.brand = brand
        self.size = size


class FavouriteAdd(KCEvent):
    __slots__ = 'book_name', 'section', 'brand'

    def __init__(self, book_name, section, brand, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.section = section
        self.brand = brand


class FavouriteDelete(KCEvent):
    __slots__ = 'book_name', 'section', 'brand'

    def __init__(self, book_name, section, brand, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.section = section
        self.brand = brand


class FavouriteShow(KCEvent):
    __slots__ = 'section', 'brand', 'quantity'

    def __init__(self, section, brand, quantity, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand
        self.quantity = quantity


class FavouriteReturn(KCEvent):
    __slots__ = 'section', 'brand', 'quantity'

    def __init__(self, section, brand, quantity, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand
        self.quantity = quantity


class TapSearch(KCEvent):
    __slots__ = 'section', 'brand', 'quantity'

    def __init__(self, section, brand, quantity, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand
        self.quantity = quantity


class TapSearchSuccess(KCEvent):
    __slots__ = 'section', 'brand', 'quantity'

    def __init__(self, section, brand, quantity, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand
        self.quantity = quantity


class TapTryBook(KCEvent):
    __slots__ = 'book_name', 'section', 'brand', 'price_money', 'price_coins', 'coins_balance'

    def __init__(self, book_name, section, brand, price_money, price_coins, coins_balance, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.section = section
        self.brand = brand
        self.price_money = price_money
        self.price_coins = price_coins
        self.coins_balance = coins_balance


class TapAddCoins(KCEvent):
    __slots__ = 'book_name', 'section', 'brand', 'price_money', 'price_coins', 'coins_balance'

    def __init__(self, book_name, section, brand, price_money, price_coins, coins_balance, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name
        self.section = section
        self.brand = brand
        self.price_money = price_money
        self.price_coins = price_coins
        self.coins_balance = coins_balance


class OpenBook(KCEvent):
    __slots__ = 'brand', 'book_name', 'price_money', 'price_coins', 'lang', 'unlocked'

    def __init__(self, brand, book_name, unlocked, price_money, price_coins, lang, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.book_name = book_name
        self.unlocked = unlocked
        self.price_money = price_money
        self.price_coins = price_coins
        self.lang = lang


class EnterPage(KCEvent):
    __slots__ = 'brand', 'book_name', 'unlocked', 'page', 'time', 'lang'

    def __init__(self, brand, book_name, unlocked, page, time, lang, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.book_name = book_name
        self.unlocked = unlocked
        self.page = page
        self.time = time
        self.lang = lang


class EnterGame(KCEvent):
    __slots__ = 'brand', 'book_name', 'unlocked', 'page', 'time', 'lang'

    def __init__(self, brand, book_name, unlocked, page, time, lang, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.book_name = book_name
        self.unlocked = unlocked
        self.page = page
        self.time = time
        self.lang = lang


class ExitGame(KCEvent):
    __slots__ = 'brand', 'book_name', 'unlocked', 'page', 'time', 'errors','lang'

    def __init__(self, brand, book_name, unlocked, page, time, errors, lang,snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.book_name = book_name
        self.unlocked = unlocked
        self.page = page
        self.time = time
        self.errors = errors
        self.lang = lang

class EnterFromSummary(KCEvent):
    __slots__ = 'brand', 'book_name', 'unlocked', 'page','lang'

    def __init__(self, brand, book_name, unlocked, page, lang,snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.book_name = book_name
        self.unlocked = unlocked
        self.page = page
        self.lang = lang


class TapLike(KCEvent):
    __slots__ = 'brand', 'book_name','lang'

    def __init__(self, brand, book_name, lang,snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.book_name = book_name
        self.lang = lang


class TapBuyCoins(PurchaseEvent):
    __slots__ = 'section', 'brand', 'coins_balance', 'book_name', 'price_money', 'lang','snum'

    def __init__(self, purchase, section, brand, coins_balance, book_name, price_money, lang,status, snum, datetime):
        super().__init__(purchase, status, price_money, datetime)
        self.section = section
        self.brand = brand
        self.coins_balance = coins_balance
        self.price_money = price_money
        self.book_name = book_name
        self.lang = lang
        self.snum = snum


class TapBuyBookForMoney(PurchaseEvent):
    __slots__ = 'brand', 'book_name', 'price_money', 'price_coins', 'section', 'coins_balance','lang', 'snum'

    def __init__(self, brand, purchase, book_name, price_money, price_coins, section, coins_balance, lang, status, snum,
                 datetime):
        super().__init__(purchase, status, price_money, datetime)
        self.brand = brand
        self.coins_balance = coins_balance
        self.book_name = book_name
        self.price_money = price_money
        self.price_coins = price_coins
        self.section = section
        self.lang = lang
        self.snum = snum


class TapBuyBookForCoins(PurchaseEvent):
    __slots__ = 'brand', 'book_name', 'price_money', 'price_coins', 'section', 'coins_balance','lang', 'snum'

    def __init__(self, brand, purchase, book_name, price_money, price_coins, section, coins_balance,lang, status, snum,
                 datetime):
        super().__init__(purchase, status, price_coins, datetime)
        self.brand = brand
        self.coins_balance = coins_balance
        self.book_name = book_name
        self.price_money = price_money
        self.price_coins = price_coins
        self.section = section
        self.lang = lang
        self.snum = snum


class TapBuyStore(PurchaseEvent):
    __slots__ = 'brand', 'price_money','lang', 'snum'

    def __init__(self, brand, purchase, price_money, lang, status, snum, datetime):
        super().__init__(purchase, status, price_money, datetime)
        self.brand = brand
        self.price_money = price_money
        self.lang = lang
        self.snum = snum


class TapSubscribe(KCEvent):
    __slots__ = 'brand', 'subscription', 'trial', 'price_money', 'lang','status', 'snum'

    def __init__(self, brand, subscription, trial, price_money, lang,status, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.subcription = subscription
        self.trial = trial
        self.price_money = price_money
        self.lang = lang
        self.status = status


class SubscriptionPaymentFromServer(PurchaseEvent):
    __slots__ = 'brand', 'subscription', 'price_money', 'history', 'snum'

    def __init__(self, brand, subscription, price_money, history, snum, datetime):
        super().__init__(subscription, "success", price_money, datetime)
        self.brand = brand
        self.snum = snum
        self.price_money = price_money
        self.history = history


class SubscriptionDiscardFromServer(KCEvent):
    __slots__ = 'brand', 'subscription', 'price_money', 'history', 'snum'

    def __init__(self, brand, subscription, price_money, history, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.subcription = subscription
        self.price_money = price_money
        self.history = history


class EnterShopBrand(KCEvent):
    __slots__ = 'brand'

    def __init__(self, brand, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand


class TapInApp(KCEvent):
    __slots__ = 'brand', 'inapp', 'price'

    def __init__(self, brand, inapp, price, snum, datetime):
        super().__init__(snum, datetime)
        self.brand = brand
        self.inapp = inapp
        self.price = price


class TapTrialFromBook(KCEvent):
    __slots__ = 'book_name'

    def __init__(self, book_name, snum, datetime):
        super().__init__(snum, datetime)
        self.book_name = book_name


class TapTrialFromShop(KCEvent):
    __slots__ = 'section', 'brand'

    def __init__(self, section, brand, snum, datetime):
        super().__init__(snum, datetime)
        self.section = section
        self.brand = brand


class EnterSubscriptions(KCEvent):
    __slots__ = 'from_par', 'brand'

    def __init__(self, from_par, brand, snum, datetime):
        super().__init__(snum, datetime)
        self.from_par = from_par
        self.brand = brand


class TapTrialFromAirship(KCEvent):
    __slots__ = ''

    def __init__(self, snum, datetime):
        super().__init__(snum, datetime)


class SettingsEnterSubscriptions(KCEvent):
    __slots__ = 'mishki_subs', 'fixiki_subs', 'mashka_subs', 'omnom_subs', 'from_par'

    def __init__(self, mishki_subs, fixiki_subs, mashka_subs, omnom_subs, from_par, snum, datetime):
        super().__init__(snum, datetime)
        self.mishki_subs = mishki_subs
        self.fixiki_subs = fixiki_subs
        self.mashka_subs = mashka_subs
        self.omnom_subs = omnom_subs
        self.from_par = from_par


class SettingsChangeSubscription(KCEvent):
    __slots__ = 'sub', 'from_par', 'to_par'

    def __init__(self, sub, from_par, to_par, snum, datetime):
        super().__init__(snum, datetime)
        self.sub = sub
        self.from_par = from_par
        self.to_par = to_par


class SettingsChangeLoc(KCEvent):
    __slots__ = 'interface_loc'

    def __init__(self, interface_loc, snum, datetime):
        super().__init__(snum, datetime)
        self.interface_loc = interface_loc


class SettingsTapRestore(KCEvent):
    __slots__ = ''

    def __init__(self, snum, datetime):
        super().__init__(snum, datetime)


class SettingsRestore(KCEvent):
    __slots__ = 'status'

    def __init__(self, status, snum, datetime):
        super().__init__(snum, datetime)
        self.status = status


class SettingsShowQuestion(KCEvent):
    __slots__ = 'num'

    def __init__(self, num, snum, datetime):
        super().__init__(snum, datetime)
        self.num = num


class SettingsTapLike(KCEvent):
    __slots__ = ''

    def __init__(self, snum, datetime):
        super().__init__(snum, datetime)


class ParentGatePassed(KCEvent):
    __slots__ = ''

    def __init__(self, snum, datetime):
        super().__init__(snum, datetime)


class SettingsTapAuthorization(KCEvent):
    __slots__ = ''

    def __init__(self, snum, datetime):
        super().__init__(snum, datetime)


class SettingsTryLogIn(KCEvent):
    __slots__ = 'status'

    def __init__(self, status, snum, datetime):
        super().__init__(snum, datetime)
        self.status = status


class SettingsTryRegister(KCEvent):
    __slots__ = 'status'

    def __init__(self, status, snum, datetime):
        super().__init__(snum, datetime)
        self.status = status
