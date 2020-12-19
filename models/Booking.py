from datetime import datetime
import models.Validation as validation

class Booking:
    def __init__(
        self,
        tg_uid,
        cust_uid,
        listing,
        chat,
        datetime,
        duration,
        info,
        timeline_content,
        process_step,
    ):
        self.__tg_uid = tg_uid
        self.__cust_uid = cust_uid
        self.__listing = listing
        self.__chat = chat
        self.__datetime = datetime
        self.__duration = duration
        self.__info = info
        self.__timeline_content = timeline_content
        self.__process_step = process_step

    def return_obj(self):
        return {
            "tg_uid": self.__tg_uid,
            "cust_uid": self.__cust_uid,
            "listing": self.__listing,
            "chat": self.__chat,
            "datetime": self.__datetime,
            "duration": self.__duration,
            "info": self.__info,
            "timeline_content": self.__timeline_content,
            "process_step": self.__process_step,
        }
