import models.Validation as validation

class Chat:
    def __init__(self, sender_id, receiver_id, msg_content):
        self.__sender_id = sender_id
        self.__receiver_id = receiver_id
        self.__msg_content = msg_content

    def return_obj(self):
        return {
            "sender_id": self.__sender_id,
            "receiver_id": self.__receiver_id,
            "msg_content": self.__msg_content,
        }