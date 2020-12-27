class Support:
    def __init__(self, uid, support_type, content, status):
        self.__uid = uid
        self.__support_type = support_type
        self.__content = content
        self.__status = status

    def return_obj(self):
        return {
            "uid": self.__uid,
            "support_type": self.__support_type,
            "content": self.__content,
            "status": self.__status,
        }
