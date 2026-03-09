from datetime import datetime
from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException


class ActivityService:

    collection_name = "user_activities"

    @staticmethod
    def log_activity(user_id: str, activity: str, details: str = ""):
        """
        Store user activity in MongoDB
        """

        try:

            db = MongoDB.get_database()
            collection = db[ActivityService.collection_name]

            activity_data = {
                "user_id": user_id,
                "activity": activity,
                "details": details,
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(activity_data)

        except Exception as e:
            raise AppException(
                f"Error saving activity: {str(e)}",
                500
            )

    @staticmethod
    def get_user_activities(user_id: str, limit: int = 20):
        """
        Fetch recent user activities
        """

        try:

            db = MongoDB.get_database()
            collection = db[ActivityService.collection_name]

            activities = list(
                collection
                .find({"user_id": user_id}, {"_id": 0})
                .sort("timestamp", -1)
                .limit(limit)
            )

            return activities

        except Exception as e:
            raise AppException(
                f"Error fetching activities: {str(e)}",
                500
            )