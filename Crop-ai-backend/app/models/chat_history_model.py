from datetime import datetime
from bson import ObjectId


class ChatHistoryModel:
    """
    Chat History Schema
    """

    def __init__(self, user_id, message, response):
        self.user_id = user_id
        self.message = message
        self.response = response
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "message": self.message,
            "response": self.response,
            "timestamp": self.timestamp
        }