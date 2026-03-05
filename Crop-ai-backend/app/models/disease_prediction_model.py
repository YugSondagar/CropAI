from pydantic import BaseModel


class DiseasePredictionResponse(BaseModel):
    predicted_label: str
    confidence: float