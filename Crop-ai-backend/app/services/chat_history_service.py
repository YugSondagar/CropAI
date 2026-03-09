from datetime import datetime
from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException


class ChatHistoryService:

    collection_name = "chat_history"

    @staticmethod
    def save_chat(user_message: str, bot_reply: str):
        """
        Save chat message and bot response in MongoDB
        """

        try:

            db = MongoDB.get_database()
            collection = db[ChatHistoryService.collection_name]

            chat_data = {
                "user_message": user_message,
                "bot_reply": bot_reply,
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(chat_data)

        except Exception as e:
            raise AppException(
                f"Error saving chat history: {str(e)}",
                500
            )

    @staticmethod
    def get_chat_history(limit: int = 20):
        """
        Get last N chat messages
        """

        try:

            db = MongoDB.get_database()
            collection = db[ChatHistoryService.collection_name]

            chats = list(
                collection
                .find({}, {"_id": 0})
                .sort("timestamp", -1)
                .limit(limit)
            )

            return chats

        except Exception as e:
            raise AppException(
                f"Error fetching chat history: {str(e)}",
                500
            )