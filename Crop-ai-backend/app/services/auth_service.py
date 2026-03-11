from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

JWT_SECRET = os.environ.get("JWT_SECRET", "super-secret-key-123")
JWT_ALGORITHM = "HS256"

class AuthService:

    @staticmethod
    def register_user(user):
        try:
            db = MongoDB.get_database()
            users = db["users"]
            
            user_data = user.model_dump()

            if users.find_one({"email": user_data["email"]}):
                raise AppException("User already exists", 400)

            # Hash password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(user_data["password"].encode('utf-8'), salt)
            user_data["password"] = hashed.decode('utf-8')

            user_data["created_at"] = datetime.utcnow()

            users.insert_one(user_data)

            return {"message": "User registered successfully"}

        except AppException:
            raise
        except Exception as e:
            raise AppException(
                f"Registration failed: {str(e)}",
                500
            )

    @staticmethod
    def login_user(user):
        try:
            db = MongoDB.get_database()
            users = db["users"]
            
            user_data = user.model_dump()

            db_user = users.find_one({"email": user_data["email"]})
            if not db_user:
                raise AppException("Invalid credentials", 401)

            # Verify password
            if not bcrypt.checkpw(user_data["password"].encode('utf-8'), db_user["password"].encode('utf-8')):
                raise AppException("Invalid credentials", 401)
                
            # Generate JWT
            payload = {
                "sub": db_user["email"],
                "name": db_user["name"],
                "exp": datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

            return {
                "access_token": token,
                "user": {
                    "name": db_user["name"],
                    "email": db_user["email"]
                }
            }

        except AppException:
            raise
        except Exception as e:
            raise AppException(f"Login failed: {str(e)}", 500)