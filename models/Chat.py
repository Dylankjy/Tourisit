        self.__sender_id = sender_id
        self.__msg_content = msg_content

    def return_obj(self):
        return {
            "sender_id": self.__sender_id,
            "msg_content": self.__msg_content,
        }
