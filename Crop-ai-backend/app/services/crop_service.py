from datetime import datetime
import numpy as np

from app.utils.model_loader import get_crop_model
from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException


class CropService:

    @staticmethod
    def recommend_crop(input_data: dict):

        """
        input_data example:
        {
            "nitrogen": 90,
            "phosphorus": 42,
            "potassium": 43,
            "temperature": 20,
            "humidity": 80,
            "ph": 6.5,
            "rainfall": 200
        }
        """

        try:
            model = get_crop_model()

            features = np.array([[
                input_data["nitrogen"],
                input_data["phosphorus"],
                input_data["potassium"],
                input_data["temperature"],
                input_data["humidity"],
                input_data["ph"],
                input_data["rainfall"]
            ]])

            prediction = model.predict(features)[0]

            # Save to DB
            db = MongoDB.get_database()
            collection = db["crop_recommendations"]

            record = {
                "input": input_data,
                "recommended_crop": prediction,
                "timestamp": datetime.utcnow()
            }

            collection.insert_one(record)

            return {
                "recommended_crop": prediction
            }

        except Exception as e:
            raise AppException(
                f"Crop recommendation failed: {str(e)}",
                500
            )