class DashboardIndexEntry:
    def __init__(self, uid, earnings_month):
        self.__uid = uid
        self.__earnings_month = [earnings_month]

    def return_obj(self):
        return {
            "uid": self.__uid,
            "earnings": self.__earnings_month,
        }
