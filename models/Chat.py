class ChatRoom:
    def __init__(self, participants, chat_type, messages=[]):
        self.__participants = participants
        self.__chat_type = chat_type
        self.__messages = messages

    def return_obj(self):
        return {
            "participants": self.__participants,
            "chat_type": self.__chat_type,
            "messages": self.__messages
        }


class Message:
    def __init__(self, sender_id, timestamp, msg_content):
        self.__sender_id = sender_id
        self.__timestamp = timestamp
        self.__msg_content = msg_content

    def return_obj(self):
        return {
            "sender_id": self.__sender_id,
            "timestamp": self.__timestamp,
            "msg_content": self.__msg_content,
        }
