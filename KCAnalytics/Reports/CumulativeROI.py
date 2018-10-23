from report_api.CommonReports import CumulativeROI
from report_api.Utilities.Utils import time_count
from Data import Parse
from Classes.User import User
import os


@time_count
def new_report(os_list=["iOS","Android"],
               days_since_install=28,
               period_start="2018-08-01",
               period_end=None,
               min_version=None,
               max_version=None,
               countries_list=[]):
    dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)).replace("\\", "/")
    events_list = [(["tap\_ buy\_%", "tap\_buy\_banner%"], "%success%")]
    CumulativeROI.new_report(parser=Parse,
                             user_class=User,
                             app="kc",
                             folder_dest=dir + "/Results/Отчёт по трафику/",
                             events_list=events_list,
                             os_list=os_list,
                             days_since_install=days_since_install,
                             period_start=period_start,
                             period_end=period_end,
                             min_version=min_version,
                             max_version=max_version,
                             countries_list=countries_list)