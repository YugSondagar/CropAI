from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException


class HistoryService:

    @staticmethod
    def get_chat_history(user_id: str):

        try:
            db = MongoDB.get_database()
            collection = db["chat_history"]

            chats = list(
                collection.find(
                    {"user_id": user_id},
                    {"_id": 0}
                ).sort("timestamp", -1)
            )

            return chats

        except Exception as e:
            raise AppException(
                f"Failed to fetch chat history: {str(e)}",
                500
            )

    @staticmethod
    def get_crop_history(user_id: str):

        try:
            db = MongoDB.get_database()
            collection = db["crop_recommendations"]

            crops = list(
                collection.find(
                    {"user_id": user_id},
                    {"_id": 0}
                ).sort("timestamp", -1)
            )

            return crops

        except Exception as e:
            raise AppException(
                f"Failed to fetch crop history: {str(e)}",
                500
            )

    @staticmethod
    def get_activity_history(user_id: str):

        try:
            db = MongoDB.get_database()
            collection = db["user_activities"]

            activities = list(
                collection.find(
                    {"user_id": user_id},
                    {"_id": 0}
                ).sort("timestamp", -1)
            )

            return activities

        except Exception as e:
            raise AppException(
                f"Failed to fetch activity history: {str(e)}",
                500
            )