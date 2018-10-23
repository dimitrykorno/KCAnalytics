from report_api.Report import get_timediff


class User:
    def __init__(self, id_2, id_1=None):

        self.user_id = id_1 if id_1 else id_2
        self.first_session = True
        self.install_date = None
        self.publisher = None
        self.source = None
        self.entries = []
        self.last_enter = None
        self.country = None

        self.installed_app_version = None
        self.skipped = False

    def is_skipped(self):
        return self.skipped

    @staticmethod
    def is_new_session( previous_event, current_event):
        if not previous_event:
            return False
        if get_timediff(current_event.datetime, previous_event.datetime, measure="min") > 20:
            return True

    def user_status_update(self, current_event, previous_event):
        '''
        обновление статуса игрока
        для корректной работы необходимо включить в запрос события, включающие данные о валюте, покупках, жизнях и тд
        :return:
        '''
        pass

    def get_status(self):
        return str("Final status:")
