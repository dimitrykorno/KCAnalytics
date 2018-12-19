from report_api.CommonReports import LifetimeHistogram
from report_api.Utilities.Utils import time_count
import os


@time_count
def new_report(os_list=["iOS"],
               max_days=100,
               app_versions=['1.0'],
               users_limit=10000):
    dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)).replace("\\", "/")
    return LifetimeHistogram.new_report(app="kc",
                                 folder_dest=dir + "/Results/Гистограма отвалов по lifetime/",
                                 os_list=os_list,
                                 app_versions=app_versions,
                                 users_limit=users_limit,
                                 max_days=max_days,
                                 app_entry_event_check="event_name='InitGameState'")