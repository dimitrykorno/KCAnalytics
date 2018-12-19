from report_api.CommonReports import InAppSales
from report_api.Utilities.Utils import time_count
from In_apps import Shop
from Data import Parse
from Classes.User import User
import os

@time_count
def new_report(os_list=["iOS","Android"],
               after_release_months_graphs=False,
               period_start="2018-08-19",
               period_end=None,
               min_version=None,
               max_version=None,
               countries_list=[]):
    dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)).replace("\\","/")
    events_list=[("TapBuyBookForCoins", "%success%")]
    InAppSales.new_report(shop=Shop,
                          parser=Parse,
                          user_class=User,
                          app="kc",
                          folder_dest=dir + "/Results/Продажи in-app'ов COINS",
                          events_list=events_list,
                          os_list=os_list,
                          after_release_months_graphs=after_release_months_graphs,
                          period_start=period_start,
                          period_end=period_end,
                          min_version=min_version,
                          max_version=max_version,
                          countries_list=countries_list)
