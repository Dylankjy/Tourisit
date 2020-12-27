class Transaction:
    def __init__(self, tg_uid, cust_uid, pay_id, cost, booking):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        self.__pay_id = pay_id
        self.__cost = cost
        self.__booking = booking

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            "pay_id": self.__pay_id,
            "cost": self.__cost,
            "booking": self.__booking,
        }
