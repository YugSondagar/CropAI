import os
import json
import logging
import joblib
from tensorflow.keras.models import load_model
from app.utils.custom_exception import AppException
from app.config.config import Settings

logger = logging.getLogger(__name__)


class ModelLoader:

    _crop_model = None
    _disease_model = None
    _index_to_class = None

    # ==========================================
    # Get Absolute Models Directory Path
    # ==========================================
    @staticmethod
    def get_models_directory():
        """
        Dynamically resolve:
        Crop Disease Detection/models
        """

        current_file_path = os.path.abspath(__file__)

        # Go up:
        # utils → app → Crop-ai-backend → Crop Disease Detection
        project_root = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(current_file_path)
                )
            )
        )

        models_path = os.path.join(project_root, "models")

        if not os.path.exists(models_path):
            raise AppException(
                f"Models directory not found at {models_path}",
                500
            )

        return models_path


    # ==========================================
    # Load Crop Model
    # ==========================================
    @classmethod
    def load_crop_model(cls):

        if cls._crop_model is None:
            try:
                models_dir = Settings.MODELS_DIR
                model_path = os.path.join(models_dir, "RandomForest.pkl")

                if not os.path.exists(model_path):
                    raise AppException(
                        f"Crop model not found at {model_path}",
                        500
                    )

                cls._crop_model = joblib.load(model_path)
                logger.info("Crop model loaded successfully.")

            except Exception:
                logger.exception("Failed to load crop model.")
                raise AppException("Crop model loading failed", 500)

        return cls._crop_model


    # ==========================================
    # Load Disease Model
    # ==========================================
    @classmethod
    def load_disease_model(cls):

        if cls._disease_model is None:
            try:
                models_dir = Settings.MODELS_DIR
                model_path = os.path.join(models_dir, "plant_disease_model.h5")

                if not os.path.exists(model_path):
                    raise AppException(
                        f"Disease model not found at {model_path}",
                        500
                    )

                cls._disease_model = load_model(model_path)
                logger.info("Disease model loaded successfully.")

            except Exception:
                logger.exception("Failed to load disease model.")
                raise AppException("Disease model loading failed", 500)

        return cls._disease_model


    # ==========================================
    # Load Class Mapping
    # ==========================================
    @classmethod
    def load_class_mapping(cls):

        if cls._index_to_class is None:
            try:
                models_dir = Settings.MODELS_DIR
                mapping_path = os.path.join(models_dir, "class_indices.json")

                if not os.path.exists(mapping_path):
                    raise AppException(
                        f"class_indices.json not found at {mapping_path}",
                        500
                    )

                with open(mapping_path, "r") as f:
                    class_indices = json.load(f)

                cls._index_to_class = {
                    int(index): label
                    for label, index in class_indices.items()
                }

                logger.info("Class mapping loaded successfully.")

            except Exception:
                logger.exception("Failed to load class mapping.")
                raise AppException("Class mapping loading failed", 500)

        return cls._index_to_class


# Cleaner access functions
def get_crop_model():
    return ModelLoader.load_crop_model()


def get_disease_model():
    return ModelLoader.load_disease_model()


def get_class_mapping():
    return ModelLoader.load_class_mapping()