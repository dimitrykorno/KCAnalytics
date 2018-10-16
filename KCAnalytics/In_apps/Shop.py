import re
from report_api.Report import Report
from In_apps.book_names import books, free_books


def get_price(in_app):
    TAX1 = 0.18
    TAX2 = 0.3
    in_app = check_inapp_name(in_app)
    if in_app in _in_apps.keys():
        if _in_apps[in_app][Report.os.value]:
            price_type = Report.os.value % 2
            # return round((in_apps[obj_name][price_type] * ((1 - TAX1))) * (1 - TAX2), 1)
            return _in_apps[check_inapp_name(in_app)][price_type]

    else:

        Report.not_found.add("Error: No '", check_inapp_name(in_app), "' in in-apps list.")
    return 0


def get_brand(book):
    if book in _in_apps.keys():
        return _in_apps[book][2]
    else:
        for books_group in (books, _collections):
            for brand, languages in books_group.items():
                for lang, books_list in languages.items():
                    if book in books_list:
                        return brand

    Report.not_found.add("Error getting category: No '" + book + "' in list.")
    return None


def get_lang(book):
    if book in _in_apps.keys():
        if re.match(r'.*\.eng$', book) or re.match(r'.*\_eng$', book):
            return "eng"
        else:
            return "rus"
    else:
        for books_group in (books, _collections):
            for brand, languages in books_group.items():
                for lang, books_list in languages.items():
                    if book in books_list:
                        return lang

    Report.not_found.add("Error getting language: No '" + book + "' in list.")
    return None


def get_brand_lang(book):
    if book in _in_apps.keys():
        return _in_apps[book][2], get_lang(book)
    else:
        for books_group in (books, _collections):
            for brand, languages in books_group.items():
                for lang, books_list in languages.items():
                    if book in books_list:
                        return brand, lang

    Report.not_found.add("Error getting brand/lang: No '" + book + "' in list.")
    return "None", "None"


def check_inapp_name(in_app):
    cat = get_brand(in_app)
    if not cat:
        cat = get_brand_lang(in_app)[0]
    if not cat:
        Report.not_found.add("Error getting category: No '", in_app, "' in in-apps/collection list.")
    if re.match(r'.*\.eng$', in_app):
        in_app = in_app[:len(in_app) - 4] + "_eng"
    if cat and cat != "coins" and not re.match(r'^' + cat + '.', in_app):
        return cat + '.' + in_app
    if cat is None:
        Report.not_found.add("Check_in_app_name. Cat is None: " + cat + " " + in_app)
    return in_app


def get_in_apps_list(brand=None, language=None, pack=None):
    unique_inapps = set()
    for in_app in _in_apps.keys():
        in_app = check_inapp_name(in_app)
        if len(_in_apps[in_app]) > 3 and _in_apps[in_app][3] == "tap":
            continue
        if brand and _in_apps[in_app][2] != brand.lower():
            continue
        if (pack is True and not is_pack(in_app)) or (pack is False and is_pack(in_app)):
            continue

        if language:
            if language.lower() in ("eng", "english") and re.match(r'.*_eng$', in_app):
                unique_inapps.add(in_app)
            elif language.lower() in ("rus", "russian") and not re.match(r'.*_eng$', in_app):
                unique_inapps.add(in_app)
        else:
            unique_inapps.add(in_app)
    return unique_inapps


def get_brands_list():
    brands = set()
    for in_app in _in_apps.keys():
        brands.add(_in_apps[in_app][2])
    return brands


def is_pack(in_app):
    if in_app in _in_apps.keys():
        return len(_in_apps[in_app]) >= 4 and _in_apps[in_app][3] == "pack"
    else:
        Report.not_found.add("Error checking for pack. Not in in-apps list. " + in_app)
        return False


def is_free_book(book):
    for brand, languages in free_books.items():
        for lang, books_list in languages.items():
            if book in books_list:
                return True
    return False


# "brand.in_app name" : (price google play, price itunes)
_in_apps = {
    # ////////////////////// FIXIKI //////////////////////
    "lift": (85, 75, "fixies"),
    "fixies.lift": (85, 75, "fixies"),
    "fixies.refrigerator": (85, 75, "fixies"),
    "refrigerator": (85, 75, "fixies"),
    "fixies.team": (85, 75, "fixies"),
    "fixies.washingmachine": (85, 75, "fixies"),
    "washingmachine": (85, 75, "fixies"),
    "fixies.cellphone": (85, 75, "fixies"),
    "cellphone": (85, 75, "fixies"),
    "fixies.solarbattery": (85, 75, "fixies"),
    "solarbattery": (85, 75, "fixies"),
    "fixies.reflexes": (85, 75, "fixies"),
    "reflexes": (85, 75, "fixies"),
    "fixies.compass": (85, 75, "fixies"),
    "compass": (85, 75, "fixies"),
    "shortcircuit": (85, 75, "fixies"),
    "fixies.flashlight": (85, 75, "fixies"),
    "flashlight": (85, 75, "fixies"),
    "stapler": (85, 75, "fixies"),
    "fixies.stapler": (85, 75, "fixies"),

    # "fixies.lift.eng": (119, 149, "fixies"),
    "fixies.lift_eng": (139, 149, "fixies"),
    "lift_eng": (139, 149, "fixies"),
    # "fixies.refrigerator.eng": (119, 149, "fixies"),
    "fixies.refrigerator_eng": (139, 149, "fixies"),
    # "fixies.washingmachine.eng": (119, 149, "fixies"),
    "fixies.washingmachine_eng": (139, 149, "fixies"),
    "fixies.stapler_eng": (139, 149, "fixies"),
    "fixies.compass_eng": (139, 149, "fixies"),
    "fixies.shortcircuit_eng": (139, 149, "fixies"),
    "fixies.flashlight_eng": (139, 149, "fixies"),
    "fixies.reflexes_eng": (139, 149, "fixies"),
    "fixies.solarbattery_eng": (139, 149, "fixies"),
    # "": (, , "fixies"),
    # "": (, , "fixies"),

    # //////////////////// FIXIKI Packs ///////////////////
    "fixies.liftnrefrigerator": (169, 149, "fixies", "pack"),
    "fixies.staplerncellphone": (179, 149, "fixies", "pack"),
    "fixies.washingmachinensolarbattery": (169, 149, "fixies", "pack"),
    "fixies.shortcircuitnflashlight": (179, 149, "fixies", "pack"),
    "fixies.reflexesncompass": (179, 149, "fixies", "pack"),
    "fixies.shortcircuit": (85, 75, "fixies"),
    "fixies.3in1": (269, 229, "fixies", "pack"),
    "fixies.3in1.promo1": (169, 149, "fixies", "pack"),
    "fixies.3in1_discount": (169, 149, "fixies", "pack"),
    "fixies.3in1.withoutElevator": (259, 229, "fixies", "pack"),
    "fixies.small.3in1": (169, 149, "fixies", "pack"),
    "fixies.4in1": (359, 299, "fixies", "pack"),
    "fixies.small.4in1": (169, 149, "fixies", "pack"),
    "fixies.5in1": (429, 379, "fixies", "pack"),
    "fixies.6in1": (499, 459, "fixies", "pack"),
    "fixies.6in1_discount": (269, 229, "fixies", "pack"),
    "fixies.big.6in1": (259, 229, "fixies", "pack"),
    "fixies.6in1.withoutElevator": (499, 459, "fixies", "pack"),
    "fixies.6in1.akciya": (359, 299, "fixies", "pack"),
    "fixies.7in1": (590, 529, "fixies", "pack"),
    "fixies.big.7in1": (359, 299, "fixies", "pack"),
    "fixies.9in1": (690, 699, "fixies", "pack"),
    "fixies.9in1_discount": (499, 529, "fixies", "pack"),
    "fixies.10in1": (699, 699, "fixies", "pack"),
    # "": (, , "fixies", "pack"),

    "fixies.reflexesncompass_eng": (279, 299, "fixies", "pack"),
    "fixies.shortcircuitnflashlight_eng": (279, 299, "fixies", "pack"),
    "fixies.washingmachinensolarbattery_eng": (279, 299, "fixies", "pack"),
    # "fixies.liftnrefrigerator.eng": (239, 299, "fixies", "pack"),
    "fixies.liftnrefrigerator_eng": (279, 299, "fixies", "pack"),
    # "fixies.3in1.eng": (299, 379, "fixies", "pack"),
    "fixies.3in1_eng": (439, 379, "fixies", "pack"),
    "fixies.4in1_eng": (599, 459, "fixies", "pack"),
    "fixies.5in1_eng": (690, 529, "fixies", "pack"),
    "fixies.6in1_eng": (799, 599, "fixies", "pack"),
    "fixies.7in1_eng": (990, 699, "fixies", "pack"),
    "fixies.9in1_eng": (1099, None, "fixies", "pack"),  #######???????

    # "": (, , "fixies", "pack"),



    # ////////////////////// MISHKI //////////////////////
    "mushroomsnleaves": (75, 75, "mishki"),
    "mishki.mushroomsnleaves": (75, 75, "mishki"),
    "photohunt": (75, 75, "mishki"),
    "mishki.photohunt": (75, 75, "mishki"),
    "travel": (75, 75, "mishki"),
    "mishki.travel": (75, 75, "mishki"),
    "reminder": (75, 75, "mishki"),
    "mishki.reminder": (75, 75, "mishki"),
    "oldfood": (75, 75, "mishki"),
    "mishki.oldfood": (75, 75, "mishki"),
    "harvestfight": (75, 75, "mishki"),
    "mishki.harvestfight": (75, 75, "mishki"),
    "cureoftrees": (75, 75, "mishki"),
    "mishki.cureoftrees": (75, 75, "mishki"),
    "domovoy": (75, 75, "mishki"),
    "mishki.domovoy": (75, 75, "mishki"),
    "insomnia": (75, 75, "mishki"),
    "mishki.insomnia": (75, 75, "mishki"),
    "warming": (75, 75, "mishki"),
    "mishki.warming": (75, 75, "mishki"),
    "gardeners": (85, 75, "mishki"),
    "mishki.gardeners": (85, 75, "mishki"),
    "honeystory": (85, 75, "mishki"),
    "mishki.honeystory": (85, 75, "mishki"),
    # "mishki.weatherforecast": (85, 75, "mishki"), #пока нет, проверить цену
    # "mishki.snakеontree": (85, 75, "mishki"),
    # "mishki.finish": (85, 75, "mishki"),
    # "mishki.piratestory": (85, 75, "mishki"),

    # "mishki.mushroomsleaves.eng": (139, 149, "mishki"),
    "mishki.mushroomsleaves_eng": (139, 149, "mishki"),
    "mushroomsnleaves_eng": (139, 149, "mishki"),
    "mishki.mushroomsnleaves_eng": (139, 149, "mishki"),
    # "mishki.photohunt.eng": (139, 149, "mishki"),
    "photohunt_eng": (139, 149, "mishki"),
    "mishki.photohunt_eng": (139, 149, "mishki"),
    # "mishki.travel.eng": (139, 149, "mishki"),
    "travel_eng": (139, 149, "mishki"),
    "mishki.travel_eng": (139, 149, "mishki"),
    "reminder_eng": (139, 149, "mishki"),
    # "mishki.reminder.eng": (139, 149, "mishki"),
    "mishki.reminder_eng": (139, 149, "mishki"),
    "oldfood_eng": (139, 149, "mishki"),
    # "mishki.oldfood.eng": (139, 149, "mishki"),
    "mishki.oldfood_eng": (139, 149, "mishki"),
    "harvestfight_eng": (139, 149, "mishki"),
    # "mishki.harvestfight.eng": (139, 149, "mishki"),
    "mishki.harvestfight_eng": (139, 149, "mishki"),
    "cureoftrees_eng": (139, 149, "mishki"),
    # "mishki.cureoftrees.eng": (139, 149, "mishki"),
    "mishki.cureoftrees_eng": (139, 149, "mishki"),
    "domovoy_eng": (139, 149, "mishki"),
    # "mishki.domovoy.eng": (139, 149, "mishki"),
    "mishki.domovoy_eng": (139, 149, "mishki"),
    "insomnia_eng": (139, 149, "mishki"),
    # "mishki.insomnia.eng": (139, 149, "mishki"),
    "mishki.insomnia_eng": (139, 149, "mishki"),

    # "": (, , "mishki"),
    # "": (, , "mishki"),

    # ///////////////////// MISHKI Packs /////////////////////
    "mushroomsnleavesnphotohunt": (179, 149, "mishki", "pack"),
    "mushroomsnleavesntravel": (179, 149, "mishki", "pack"),
    "mishki.gardenersnhoney": (179, 149, "mishki", "pack"),
    "gardenersnhoney": (179, 149, "mishki", "pack"),
    "photohuntntravel": (179, 149, "mishki", "pack"),
    "oldfoodnharvestfight": (179, 149, "mishki", "pack"),
    "curetreendomovoy": (179, 149, "mishki", "pack"),
    "insomnianwarming": (179, 149, "mishki", "pack"),
    "mishki.insomnianwarming": (179, 149, "mishki", "pack"),
    "mishki.oldfoodnharvestfight": (179, 149, "mishki", "pack"),
    "mishki.curetreendomovoy": (179, 149, "mishki", "pack"),
    "mishki.mushroomsnleavesnphotohunt": (179, 149, "mishki", "pack"),
    "mishki.mushroomsnleavesntravel": (179, 149, "mishki", "pack"),
    "mishki.photohuntntravel": (179, 149, "mishki", "pack"),
    "3in1": (209, 169, "mishki", "pack"),
    "mishki.3in1": (209, 169, "mishki", "pack"),
    "mishki.4in1": (299, 229, "mishki", "pack"),
    "mishki.4in1.promo1": (209, 149, "mishki", "pack"),
    "4in1_discount": (209, 149, "mishki", "pack"),
    "mishki.4in1_discount": (209, 149, "mishki", "pack"),
    "4in1": (299, 229, "mishki", "pack"),
    "4in1.promo1": (209, 149, "mishki", "pack"),
    "6in1": (429, 379, "mishki", "pack"),
    "mishki.6in1": (429, 379, "mishki", "pack"),
    "mishki.7in1": (499, 459, "mishki", "pack"),
    "mishki.7in1.promo1": (359, 299, "mishki", "pack"),
    "mishki.small.7in1": (359, 299, "mishki", "pack"),
    "7in1_discount": (359, 299, "mishki", "pack"),
    "mishki.7in1_discount": (359, 299, "mishki", "pack"),
    "7in1": (498, 459, "mishki", "pack"),
    "7in1.promo1": (359, 299, "mishki", "pack"),
    "8in1": (590, 529, "mishki", "pack"),
    "mishki.8in1": (590, 529, "mishki", "pack"),
    "9in1": (599, 599, "mishki", "pack"),
    "mishki.9in1": (599, 599, "mishki", "pack"),
    "10in1": (699, 699, "mishki", "pack"),
    "10in1_discount": (419, 379, "mishki", "pack"),
    "mishki.10in1_discount": (419, 379, "mishki", "pack"),
    "mishki.10in1": (699, 699, "mishki", "pack"),
    "mishki.10in1.akciya": (499, 459, "mishki", "pack"),
    "mishki.big.10in1": (419, 379, "mishki", "pack"),

    # "mishki.mushroomsnleavesnphotohunt.eng": (279, 299, "mishki", "pack"),
    "mishki.mushroomsnleavesnphotohunt_eng": (279, 299, "mishki", "pack"),
    "mushroomsnleavesnphotohunt_eng": (279, 299, "mishki", "pack"),
    "travelandreminder_eng": (279, 299, "mishki", "pack"),
    "mishki.travelandreminder_eng": (279, 299, "mishki", "pack"),
    # "mishki.travelandreminder.eng": (279, 299, "mishki", "pack"),
    "oldfoodandharvestfight_eng": (279, 299, "mishki", "pack"),
    # "mishki.oldfoodandharverstfight.eng": (279, 299, "mishki", "pack"),
    "mishki.oldfoodandharvestfight_eng": (279, 299, "mishki", "pack"),
    "mishki.oldfoodandharverstfight_eng": (279, 299, "mishki", "pack"),
    "cureoftreesndomovoy_eng": (279, 299, "mishki", "pack"),
    # "mishki.cureoftreesndomovoy.eng": (279, 299, "mishki", "pack"),
    "mishki.cureoftreesndomovoy_eng": (279, 299, "mishki", "pack"),
    # "mishki.3in1.eng": (349, 379, "mishki", "pack"),
    "mishki.3in1_eng": (449, 379, "mishki", "pack"),
    "3in1_eng": (449, 379, "mishki", "pack"),
    "5in1_eng": (690, 529, "mishki", "pack"),
    "mishki.5in1_eng": (690, 529, "mishki", "pack"),
    "7in1_eng": (899, 899, "mishki", "pack"),
    "mishki.7in1_eng": (899, 899, "mishki", "pack"),
    "9in1_eng": (1099, 1090, "mishki", "pack"),
    "mishki.9in1_eng": (1099, 1090, "mishki", "pack"),
    "9in1_discount_eng": (899, 899, "mishki", "pack"),
    "mishki.9in1_discount_eng": (899, 899, "mishki", "pack"),

    # "": (, , "mishki", "pack"),
    # "": (, , "mishki", "pack"),

    # ////////////////////// MASHA //////////////////////
    "spookystories.aboutbug": (85, 75, "spookystories"),
    "aboutbug": (85, 75, "spookystories"),
    "spookystories.boyandwater": (85, 75, "spookystories"),
    "boyandwater": (85, 75, "spookystories"),
    "spookystories.plantmonsters": (85, 75, "spookystories"),
    "spookystories.kitten": (85, 75, "spookystories"),
    "kitten": (85, 75, "spookystories"),
    "spookystories.newyear": (75, 75, "spookystories"),
    "newyear": (75, 75, "spookystories"),
    "spookystories.superstitiousgirl": (85, 75, "spookystories"),
    "superstitiousgirl": (85, 75, "spookystories"),
    "spookystories.snottyboy": (85, 75, "spookystories"),

    # "spookystories.aboutbug.eng": (139, 149, "spookystories"),
    "spookystories.aboutbug_eng": (139, 149, "spookystories"),
    "aboutbug_eng": (139, 149, "spookystories"),

    # "spookystories.boyandwater.eng": (139, 149, "spookystories"),
    "spookystories.boyandwater_eng": (139, 149, "spookystories"),
    # "spookystories.plantmonsters.eng": (139, 149, "spookystories"),
    "spookystories.plantmonsters_eng": (139, 149, "spookystories"),
    "spookystories.kitten_eng": (139, 149, "spookystories"),
    "spookystories.newyear_eng": (139, 149, "spookystories"),

    # "": (,,"spookystories"),
    # "": (,,"spookystories"),

    # //////////////////// MASHA Packs ///////////////////
    "spookystories.mashka.small.3in1": (179, 149, "spookystories", "pack"),
    "spookystories.bugandboy": (179, 149, "spookystories", "pack"),
    "spookystories.plantmonstersnkitten": (179, 149, "spookystories", "pack"),
    "spookystories.girlnsnottyboy": (179, 149, "spookystories", "pack"),
    "spookystories.3in1": (269, 229, "spookystories", "pack"),
    "mashka.small.3in1": (179, 149, "spookystories", "pack"),
    "spookystories.4in1": (359, 299, "spookystories", "pack"),
    "spookystories.5in1": (429, 379, "spookystories", "pack"),
    "mashka.big.5in1": (259, 229, "spookystories", "pack"),
    "spookystories.mashka.big.5in1": (259, 229, "spookystories", "pack"),
    "spookystories.6in1": (499, 379, "spookystories", "pack"),

    "spookystories.plantmonstersnkitten_eng": (279, 299, "spookystories", "pack"),
    # "spookystories.bugandboy.eng": (279, 299, "spookystories", "pack"),
    "spookystories.bugandboy_eng": (279, 299, "spookystories", "pack"),
    # "spookystories.3in1.eng": (349, 579, "spookystories", "pack"),
    "spookystories.3in1_eng": (439, 379, "spookystories", "pack"),
    "spookystories.4in1_eng": (590, 459, "spookystories", "pack"),
    "spookystories.5in1_eng": (690, 529, "spookystories", "pack"),

    # "": (,,"spookystories", "pack"),
    # "": (,,"spookystories", "pack"),


    # ////////////////////// OMNOM //////////////////////
    "omnom.yarmarka": (75, 75, "omnom"),
    "omnom.australia": (75, 75, "omnom"),
    "omnom.brazil": (75, 75, "omnom"),
    "omnom.shopping": (75, 75, "omnom"),
    "omnom.velogonka": (75, 75, "omnom"),
    "omnom.sport": (75, 75, "omnom"),
    "omnom.tea": (75, 75, "omnom"),
    "omnom.mexico": (75, 75, "omnom"),
    "omnom.receipt": (75, 75, "omnom"),
    "omnom.usa": (75, 75, "omnom"),
    "omnom.christmas": (75, 75, "omnom"),
    # "": (,,"omnom"),
    # "": (,,"omnom"),
    "omnom.yarmarka_eng": (139, 149, "omnom"),
    "omnom.australia_eng": (139, 149, "omnom"),
    "omnom.brazil_eng": (139, 149, "omnom"),

    # "": (,,"omnom"),
    # "": (,,"omnom"),

    # //////////////////// OMNOM Packs////////////////////
    "omnom.christmas.yarmarka": (179, 149, "omnom", "pack"),
    "omnom.australianbrazil": (179, 149, "omnom", "pack"),
    "omnom.velogonkareceipt": (159, 149, "omnom", "pack"),
    "omnom.mexiconusa": (159, 149, "omnom", "pack"),
    "omnom.3in1": (299, 229, "omnom", "pack"),
    "omnom.4in1": (359, 299, "omnom", "pack"),
    "omnom.10in1": (699, 699, "omnom", "pack"),
    "omnom.sportshopping": (159, 149, "omnom", "pack"),
    # "": (,,"omnom", "pack"),
    # "": (,,"omnom", "pack"),


    "omnom.3in1_eng": (439, 379, "omnom", "pack"),
    "omnom.australianbrazil_eng": (279, 299, "omnom", "pack"),
    # "": (,,"omnom", "pack"),


    # ////////////////////// TRI KOTA //////////////////////
    "trikota.velosiped": (75, 75, "trikota",),
    "trikota.otkritka": (75, 75, "trikota"),
    "trikota.kinoshedevr": (75, 75, "trikota"),
    "trikota.varenie": (75, 75, "trikota"),
    # "": (,,"trikota"),

    # /////////////////// TRI KOTA Packs ////////////////////
    "trikota.otkritkankino": (149, 149, "trikota", "pack"),
    "trikota.3in1": (219, 229, "trikota", "pack"),

    # "": (,,"trikota", "pack"),
    # "": (,,"trikota", "pack"),


    # ////////////////////// COINS //////////////////////
    "1800coins": (69, 75, "coins"),
    "1800": (69, 75, "coins"),
    "4500coins": (149, 169, "coins"),
    "4500": (149, 169, "coins"),
    "7200coins": (219, 229, "coins"),
    "7200": (219, 229, "coins"),
    "18000coins": (429, 459, "coins"),
    "18000": (429, 459, "coins"),
    "18000coins.ny17.sale": (259, 249, "coins"),
    "29000": (590, 599, "coins"),
    "29000coins": (590, 599, "coins"),
    "29000coins.ny17.sale": (409, 379, "coins"),
    "coins.29000.ny": (409, 379, "coins"),
    "44000coins": (899, 999, "coins"),
    "44000": (899, 999, "coins"),
    "coins.44000.ny": (459, 459, "coins")}

# ____________________ ////////////////////// Коллекции //////////////////////_________________________
_collections = {"mishki": {
    "eng": {  # "cureoftreesndomovoy_eng", "oldfoodandharvestfight_eng", "travelandreminder_eng",
        # "mushroomsnleavesnphotohunt_eng", "bebebears_soon_eng", " mishki.insomnia_eng",
        # "3in1_eng", "5in1_eng", "7in1_eng",
        # "9in1_eng",
        "mishki.domovoy_eng", "mishki.cureoftrees_eng",
        "mishki.harvestfight_eng", "mishki.oldfood_eng", "mishki.reminder_eng",
        "mishki.travel_eng", "mishki.photohunt_eng", "mishki.mushroomsnleaves_eng",
        "mishki.starrysky_eng", "starrysky_eng", },
    "rus": {"mishki.starrysky", "starrysky", "mishki.mushroomsnleaves", "mishki.photohunt",
            "mishki.travel", "mishki.bestreminder", "bestreminder", "mishki.oldfood",
            "mishki.harvestfight", " mishki.cureoftrees", "mishki.brownie", "brownie",
            "mishki.insomnia", "mishki.warming", "mishki.gardeners",
            "mishki.honeystory", "soon",
            # "10in1",
            # "9in1", "8in1", "7in1",
            # "6in1", "4in1", "3in1",
            # "mushroomsnleavesnphotohunt", "mushroomsnleavesntravel", "photohuntntravel",
            # "oldfoodnharvestfight", "curetreendomovoy", "insomnianwarming",
            # "gardenersnhoney"
            }},
    "fixies": {
        "eng": {  # "shortcircuitnflashlight_eng", "reflexesncompass_eng", "washingmachinensolarbattery_eng",
            # "fixies.3in1_eng", "fixies.4in1_eng", "fixies.5in1_eng",
            # "fixies.6in1_eng", "fixies.7in1_eng", "fixies.9in1_eng",
            "fixies_soon_eng", "fixies.stapler_eng", "fixies.flashlight_eng",
            "fixies.shortcircuit_eng", "fixies.compass_eng", "fixies.reflexes_eng",
            "fixies.solarbattery_eng", "fixies.washingmachine_eng", "washingmachine_eng", "fixies.holodilnik_eng",
            "holodilnik_eng",
            "fixies.lift_eng", "fixies.cellphone_eng"},
        "rus": {  # "fixies.10in1", "fixies.9in1", "fixies.7in1",
            # "fixies.6in1", "fixies.6in1.withoutElevator", "fixies.5in1",
            # "fixies.4in1", "fixies.3in1", "fixies.3in1.withoutElevator",
            # "staplerncellphone", "shortcircuitnflashlight", "reflexesncompass",
            # "washingmachinensolarbattery", "liftnrefrigerator",
            "soon",
            "fixies.stapler", "fixies.flashlight", "fixies.shortcircuit",
            "fixies.compass", "fixies.reflexes", "fixies.solarbattery",
            "fixies.washingmachine", "fixies.holodilnik", "holodilnik", "fixies.lift", "fixies.cellphone"}},

    "spookystories": {
        "eng": {  # "plantmonstersnkitten_eng", "spookystories.3in1_eng", "spookystories.4in1_eng",
            # "spookystories.5in1_eng",
            "masha_soon_eng", "spookystories.newyear_eng",
            "spookystories.kitten_eng", "spookystories.aboutmonsters_eng", "aboutmonsters_eng",
            "spookystories.boyandwater_eng", "boyandwater_eng",
            "spookystories.aboutbug_eng", "spookystories.superstitiousgirl_eng"},
        "rus": {  # "spookystories.6in1", "spookystories.5in1", "spookystories.4in1",
            # "spookystories.3in1", "plantmonstersnkitten",
            "bugandboy",
            "soon", "spookystories.superstitiousgirl", "spookystories.newyear",
            "spookystories.kitten", "spookystories.aboutmonsters", "aboutmonsters", "spookystories.boyandwater",
            "spookystories.aboutbug", "aboutbug"}},

    "omnom": {"eng": {"omnom_soon", "omnom.yarmarka_eng", "omnom.christmas_eng",
                      "omnom.australia_eng", "omnom.brazil_eng",
                      # "omnom.3in1_eng", "omnom.australianbrazil_eng"
                      },

              "rus": {  # "omnom.3in1", "omnom.australianbrazil", "omnom.10in1",
                  # "omnom.mexiconusa","omnom.sportshopping"
                  "christmas.yarmarka",
                  "soon", "omnom.brazil", "omnom.australia",
                  "omnom.yarmarka", "omnom.christmas", "omnom.tea",
                  "omnom.sport", "omnom.velogonka", "omnom.receipt",
                  "omnom.shopping", "omnom.mexico"
                                    "omnom.usa"}},

    "trikota": {"eng": {},
                "rus": {  # "trikota.3in1", "trikota.otkritkankino",
                    "soon",
                    "trikota.velosiped", "trikota.kinoshedevr", "trikota.otkritka",
                    "trikota.varenie"}},

}

_free_collections = {"mishki": {"rus": "mishki.starrysky", "eng": "mishki.starrysky_eng"},
                     "fixies": {"rus": "fixies.cellphone", "eng": "fixies.cellphone_eng"},
                     "spookystories": {"rus": "spookystories.superstitiousgirl",
                                       "eng": "spookystories.superstitiousgirl_eng"},
                     "trikota": {"rus": "trikota.varenie"},
                     "omnom": {"rus": "omnom.christmas", "eng": "omnom.christmas_eng"}}


def is_collection(book):
    for brand, languages in _collections.items():
        for language, collections in languages.items():
            if book in collections:
                return True
    # Report.Report.not_found.add("No collection item found:" + book)
    return False


def get_free_collections():
    return _free_collections


def is_free_collection(book):
    for brand, languages in _free_collections.items():
        for language, collection in languages.items():
            if collection == book:
                return True
    return False


# только в своих
# "fixistore.3in1.part1": (259, 229, "fixies", "pack"),
# "fixistore.3in1.part2": (259, 229, "fixies", "pack"),
# "fixistore.6in1": (489, 459, "fixies", "pack"),
# "fixies.fixistore.3in1.part1": (259, 229, "fixies", "pack"),
# "fixies.fixistore.3in1.part2": (259, 229, "fixies", "pack"),
# "fixies.fixistore.6in1": (489, 459, "fixies", "pack"),

# "mimistore.5in1.part1": (349, 299, "mishki", "pack"),
# "mimistore.5in1.part2": (349, 299, "mishki", "pack"),
# "mimistore.10in1": (690, 599, "mishki", "pack"),
# "mishki.mimistore.5in1.part1": (349, 299, "mishki", "pack"),  ##
# "mishki.mimistore.5in1.part2": (349, 299, "mishki", "pack"),  ## чтобы парсилось
# "mishki.mimistore.10in1": (690, 599, "mishki", "pack"),  ##

def get_categories(in_app):
    brand, lang = get_brand_lang(in_app)
    pack = "pack" if is_pack(in_app) else "solo"
    return brand, lang, pack
