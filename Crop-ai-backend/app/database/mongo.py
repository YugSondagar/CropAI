from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config.config import Settings
from app.utils.custom_exception import AppException


class MongoDB:
    """
    MongoDB connection manager
    """

    _client = None
    _database = None

    @classmethod
    def connect(cls):
        """
        Establish MongoDB connection using Settings
        """

        if cls._client is None:
            try:

                # Create client using MONGO_URL from .env
                cls._client = MongoClient(Settings.MONGO_URL)

                # Test connection
                cls._client.admin.command("ping")

                # Select database
                cls._database = cls._client[Settings.DB_NAME]

                print("MongoDB connected successfully.")

            except ConnectionFailure as e:
                raise AppException(
                    f"MongoDB connection failed: {str(e)}",
                    500
                )

        return cls._database

    @classmethod
    def get_database(cls):
        """
        Return database instance
        """

        if cls._database is None:
            return cls.connect()

        return cls._database

    # -----------------------------
    # COLLECTION HELPERS
    # -----------------------------

    @classmethod
    def get_user_collection(cls):
        db = cls.get_database()
        return db["users"]

    @classmethod
    def get_chat_history_collection(cls):
        db = cls.get_database()
        return db["chat_history"]

    @classmethod
    def get_activity_collection(cls):
        db = cls.get_database()
        return db["user_activity"]