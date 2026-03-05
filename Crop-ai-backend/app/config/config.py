import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """
    Central configuration for the application
    """

    # ==========================
    # MongoDB
    # ==========================
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    DB_NAME = os.getenv("DB_NAME", "crop_ai_db")

    # ==========================
    # Image Config
    # ==========================
    IMAGE_SIZE = (224, 224)

    # ==========================
    # Models Directory
    # ==========================
    BASE_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../")
    )

    MODELS_DIR = os.path.join(BASE_DIR, "models")