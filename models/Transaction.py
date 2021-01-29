from datetime import datetime


class Transaction:
    def __init__(self, tg_uid, cust_uid, earnings, booking, tour_name):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        # self.__pay_id = pay_id
        self.__earnings = earnings
        self.__booking = booking
        self.__tour_name = tour_name
        self.__date_paid = ''
        self.__month_paid = ''
        self.__year_paid = ''
        self.__pay_status = 0
        self.__rating = ''

    def payment_made(self):
        self.__date_paid = datetime.now().isoformat()
        self.__month_paid = datetime.now().month
        self.__year_paid = datetime.now().year
        self.__pay_status = 1

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            # "pay_id": self.__pay_id,
            "earnings": self.__earnings,
            "booking": self.__booking,
            "date_paid": self.__date_paid,
            "month_paid": self.__month_paid,
            "year_paid": self.__year_paid,
            "pay_status": self.__pay_status,
            "rating": self.__rating,
            "tour_name": self.__tour_name
        }
