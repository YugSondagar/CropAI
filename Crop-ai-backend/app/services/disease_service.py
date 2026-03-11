import torch
import torch.nn.functional as F
from datetime import datetime

from app.config.class_names import CLASS_NAMES
from app.utils.model_loader import get_disease_model
from app.utils.image_processing import ImageProcessor
from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException
from app.utils.logger import logger


class DiseaseService:

    @staticmethod
    def predict_disease(image_bytes: bytes):

        try:
            # -------------------------
            # 1️⃣ Preprocess Image
            # -------------------------
            image_tensor = ImageProcessor.preprocess_image(image_bytes)

            # -------------------------
            # 2️⃣ Load Model
            # -------------------------
            model = get_disease_model()
            
            # Ensure model is in evaluation mode (already set in loader, but double check)
            model.eval()

            # -------------------------
            # 3️⃣ Predict
            # -------------------------
            with torch.no_grad():

                output = model(image_tensor)

                probabilities = F.softmax(output, dim=1)

                pred = torch.argmax(probabilities, dim=1).item()

                confidence = probabilities[0][pred].item()

            # -------------------------
            # 4️⃣ Get Disease Name
            # -------------------------
            disease_name = CLASS_NAMES[pred]

            confidence_percent = round(confidence * 100, 2)

            # -------------------------
            # 5️⃣ Save to MongoDB
            # -------------------------
            db = MongoDB.get_database()

            collection = db["disease_predictions"]

            record = {
                "disease": disease_name,
                "confidence": confidence_percent,
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(record)

            logger.info(f"Disease predicted: {disease_name} ({confidence_percent}%)")

            # -------------------------
            # 6️⃣ Return Response
            # -------------------------
            return {
                "disease": disease_name,
                "confidence": confidence_percent
            }

        except Exception as e:

            logger.error(f"Disease prediction error: {str(e)}")

            raise AppException(
                f"Disease prediction failed: {str(e)}",
                500
            )
