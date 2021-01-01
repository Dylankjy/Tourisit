class Chat:
    def __init__(self, sender_id, msg_content, is_booking_chat, chat_id):
        self.__sender_id = sender_id
        self.__msg_content = msg_content

    def return_obj(self):
        return {
            "sender_id": self.__sender_id,
            "msg_content": self.__msg_content,
            "is_booking_chat": False,
            "chat_id": self.__chat_id

            # NEED NOT CHECK. THIS IS JUST MERELY A NOTE TO SELF.
            # If is_booking_chat, then chat id is your booking id
            # If NOT is_booking_chat, random string
        }
