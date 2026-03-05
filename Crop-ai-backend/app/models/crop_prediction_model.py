from pydantic import BaseModel


class CropPredictionRequest(BaseModel):
    nitrogen: float
    phosphorus: float
    potassium: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


class CropPredictionResponse(BaseModel):
    recommended_crop: str