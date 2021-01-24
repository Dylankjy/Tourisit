class DashboardIndexEntry:
    def __init__(self, uid, earnings_month=[]):
        self.__uid = uid
        self.__earnings_month = earnings_month

    def return_obj(self):
        return {
            "uid": self.__uid,
            "earnings": self.__earnings_month,
        }

    def add_new_data(self, new_data):
        return self.__earnings_month.append(new_data)
