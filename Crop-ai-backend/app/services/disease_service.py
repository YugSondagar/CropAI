import torch
import torch.nn.functional as F
from datetime import datetime

import json
import os
from app.config.class_names import CLASS_NAMES
from app.utils.model_loader import get_disease_model, get_class_mapping
from app.utils.image_processing import ImageProcessor
from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException
from app.utils.logger import logger


from app.services.activity_service import ActivityService


class DiseaseService:

    @staticmethod
    def predict_disease(user_id: str, image_bytes: bytes):

        try:
            # ------------------------- 
            # 1️⃣ Preprocess Image
            # -------------------------
            image_tensor = ImageProcessor.preprocess_image(image_bytes)

            # -------------------------
            # 2️⃣ Load Model
            # -------------------------
            model = get_disease_model()
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
            # 4️⃣ Get Disease Name - TRY JSON MAPPING FIRST
            # -------------------------
            class_mapping = get_class_mapping()
            
            if class_mapping and pred in class_mapping:
                disease_name = class_mapping[pred]
                disease_name_clean = CLASS_NAMES[pred]
                logger.info(f"Using JSON class mapping: index {pred} -> {disease_name} -> CLEAN: {disease_name_clean}")
            else:
                disease_name = CLASS_NAMES[pred]
                disease_name_clean = disease_name
                logger.info(f"Using CLASS_NAMES fallback: index {pred} -> {disease_name}")

            logger.info(f"PREDICTED DISEASE NAME: '{disease_name}' CLEAN: '{disease_name_clean}'")

            confidence_percent = round(confidence * 100, 2)

            # -------------------------
            # 5️⃣ Save to MongoDB
            # -------------------------
            db = MongoDB.get_database()
            collection = db["disease_predictions"]
            record = {
                "disease": disease_name,
                "confidence": confidence_percent,
                "predicted_index": pred,
                "timestamp": datetime.utcnow()
            }
            collection.insert_one(record)

            logger.info(f"✅ Disease predicted: {disease_name} (index: {pred}, confidence: {confidence_percent}%)")

            # -------------------------
            # 6️⃣ Save User Activity
            # -------------------------
            ActivityService.log_activity(
                user_id=user_id,
                activity="Disease Detection",
                details=f"Detected disease: {disease_name}"
            )

            # ------------------------- 
            # 7️⃣ Load Disease Information
            # ------------------------- 
            try:
                # Get absolute path to disease_info.json (from project root)
                # Simple relative path from project root
                disease_info_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'Crop-ai-backend', 'app', 'config', 'disease_info.json')
                logger.info(f'Looking for disease_info at: {disease_info_path}')
                logger.info(f'File exists: {os.path.exists(disease_info_path)}')
                
                with open(disease_info_path, 'r', encoding='utf-8') as f:
                    disease_info = json.load(f)
                logger.info(f'Disease info loaded, keys: {list(disease_info.keys())[:3]}')
                logger.info(f"Looking for disease '{disease_name_clean}' in JSON - FOUND: {disease_name_clean in disease_info}")
                
                info = disease_info.get(disease_name_clean, {})
                cause = info.get('cause', 'Information not available')
                prevention = info.get('prevention', 'Consult local agricultural expert')
                logger.info(f"CAUSE: '{cause[:50]}...'")
                logger.info(f"PREVENTION: '{prevention[:50]}...'")
            except FileNotFoundError:
                logger.warning("disease_info.json not found, using default info")
                cause = "Consult local agricultural expert"
                prevention = "Follow standard disease management practices"

            # ------------------------- 
            # 8️⃣ Return Enhanced Response
            # ------------------------- 
            return {
                "disease": disease_name,
                "confidence": confidence_percent,
                "predicted_index": pred,
                "top_probabilities": probabilities[0].topk(3).values.tolist(),
                "cause": cause,
                "prevention": prevention
            }

        except Exception as e:
            logger.error(f"Disease prediction error: {str(e)}")
            raise AppException(
                f"Disease prediction failed: {str(e)}",
                500
            )

