from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException
from datetime import datetime


class AuthService:

    @staticmethod
    def register_user(user_data: dict):

        try:
            db = MongoDB.get_database()
            users = db["users"]

            if users.find_one({"email": user_data["email"]}):
                raise AppException("User already exists", 400)

            user_data["created_at"] = datetime.utcnow()

            users.insert_one(user_data)

            return {"message": "User registered successfully"}

        except Exception as e:
            raise AppException(
                f"Registration failed: {str(e)}",
                500
            )