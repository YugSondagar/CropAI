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

    @staticmethod
    def get_models_directory():
        """Dynamically resolve: Crop Disease Detection/models"""
        current_file_path = os.path.abspath(__file__)
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


    class ResNet9(nn.Module):
        """EXACT ResNet9 class from training notebook"""
        def __init__(self, in_channels=3, num_diseases=38):
            super().__init__()
            
            self.conv1 = ModelLoader.ConvBlock(in_channels, 64)
            self.conv2 = ModelLoader.ConvBlock(64, 128, pool=True)  # 128 x 64 x 64 
            self.res1 = nn.Sequential(
                ModelLoader.ConvBlock(128, 128), 
                ModelLoader.ConvBlock(128, 128)
            )
            
            self.conv3 = ModelLoader.ConvBlock(128, 256, pool=True)  # 256 x 16 x 16
            self.conv4 = ModelLoader.ConvBlock(256, 512, pool=True)  # 512 x 4 x 4
            self.res2 = nn.Sequential(
                ModelLoader.ConvBlock(512, 512), 
                ModelLoader.ConvBlock(512, 512)
            )
            
            self.classifier = nn.Sequential(
                nn.MaxPool2d(4),
                nn.Flatten(),
                nn.Linear(512, num_diseases)
            )

        def forward(self, xb):
            out = self.conv1(xb)
            out = self.conv2(out)
            out = self.res1(out) + out  # Residual connection
            out = self.conv3(out)
            out = self.conv4(out)
            out = self.res2(out) + out  # Residual connection
            out = self.classifier(out)
            return out


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

                from app.config.class_names import CLASS_NAMES
                num_classes = len(CLASS_NAMES)

                # Create EXACT ResNet9 model matching training
                model = cls.ResNet9(num_diseases=num_classes)
                
                # Load trained state_dict
                state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=False)
                model.load_state_dict(state_dict)
                model.eval()
                
                cls._disease_model = model
                logger.info("✅ Disease ResNet9 model loaded perfectly!")

            except Exception as e:
                logger.exception(f"Disease model load error: {str(e)}")
                raise AppException(f"Disease model loading failed: {str(e)}", 500)

        return cls._disease_model


    @classmethod
    def load_class_mapping(cls):
        if cls._index_to_class is None:
            try:
                models_dir = Settings.MODELS_DIR
                mapping_path = os.path.join(models_dir, "class_indices.json")
                if os.path.exists(mapping_path):
                    with open(mapping_path, "r") as f:
                        class_indices = json.load(f)
                    cls._index_to_class = {
                        int(index): label
                        for label, index in class_indices.items()
                    }
                    logger.info("Class mapping loaded from JSON")
                else:
                    logger.warning("No class_indices.json - using CLASS_NAMES order")
                    cls._index_to_class = None
            except Exception as e:
                logger.exception(f"Class mapping error: {str(e)}")
                cls._index_to_class = None
        return cls._index_to_class


def get_crop_model():
    return ModelLoader.load_crop_model()


def get_disease_model():
    return ModelLoader.load_disease_model()


def get_class_mapping():
    return ModelLoader.load_class_mapping()

