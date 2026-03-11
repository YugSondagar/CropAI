import os
import json
import logging
import joblib
import torch
import torch.nn as nn
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
    # ConvBlock for ResNet9
    # ==========================================
    @staticmethod
    def ConvBlock(in_channels, out_channels, pool=False):
        layers = [
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        ]
        if pool:
            layers.append(nn.MaxPool2d(4))
        return nn.Sequential(*layers)


    # ==========================================
    # Custom ResNet9 Architecture
    # ==========================================
    @staticmethod
    def ResNet9(num_classes):
        """
        Custom ResNet9 model architecture as per the notebook
        """
        model = nn.Sequential(
            # conv1: 3 -> 64, 256x256
            ModelLoader.ConvBlock(3, 64),
            # conv2: 64 -> 128, pool, 64x64
            ModelLoader.ConvBlock(64, 128, pool=True),
            # res1: 128 -> 128
            nn.Sequential(
                ModelLoader.ConvBlock(128, 128),
                ModelLoader.ConvBlock(128, 128)
            ),
            # conv3: 128 -> 256, pool, 16x16
            ModelLoader.ConvBlock(128, 256, pool=True),
            # conv4: 256 -> 512, pool, 4x4
            ModelLoader.ConvBlock(256, 512, pool=True),
            # res2: 512 -> 512
            nn.Sequential(
                ModelLoader.ConvBlock(512, 512),
                ModelLoader.ConvBlock(512, 512)
            ),
            # classifier
            nn.Sequential(
                nn.MaxPool2d(4),
                nn.Flatten(),
                nn.Linear(512, num_classes)
            )
        )
        return model


    # ==========================================
    # Load Disease Model (PyTorch ResNet9)
    # ==========================================
    @classmethod
    def load_disease_model(cls):

        if cls._disease_model is None:
            try:
                models_dir = Settings.MODELS_DIR
                model_path = os.path.join(models_dir, "plant_disease_model.pth")

                if not os.path.exists(model_path):
                    raise AppException(
                        f"Disease model not found at {model_path}",
                        500
                    )

                # Get number of classes
                from app.config.class_names import CLASS_NAMES
                num_classes = len(CLASS_NAMES)

                # Create ResNet9 model architecture
                model = cls.ResNet9(num_classes)
                
                # Load the state dict (weights_only=False for full state dict)
                state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=False)
                
                # Load state dict
                model.load_state_dict(state_dict)
                
                # Set to evaluation mode
                model.eval()
                
                cls._disease_model = model
                logger.info("Disease model loaded successfully.")

            except Exception as e:
                logger.exception(f"Failed to load disease model: {str(e)}")
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
                    # Use default class names from config
                    logger.warning("class_indices.json not found, using default CLASS_NAMES")
                    cls._index_to_class = None
                    return cls._index_to_class

                with open(mapping_path, "r") as f:
                    class_indices = json.load(f)

                cls._index_to_class = {
                    int(index): label
                    for label, index in class_indices.items()
                }

                logger.info("Class mapping loaded successfully.")

            except Exception:
                logger.exception("Failed to load class mapping.")
                cls._index_to_class = None

        return cls._index_to_class


# Cleaner access functions
def get_crop_model():
    return ModelLoader.load_crop_model()


def get_disease_model():
    return ModelLoader.load_disease_model()


def get_class_mapping():
    return ModelLoader.load_class_mapping()
