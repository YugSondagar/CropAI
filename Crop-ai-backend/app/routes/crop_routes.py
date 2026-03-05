from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.crop_service import CropService
from app.utils.custom_exception import AppException
from app.models.crop_prediction_model import CropPredictionRequest


crop_bp = APIRouter(
    prefix="/crop",
    tags=["Crop Recommendation"]
)


@crop_bp.post("/recommend")
async def recommend_crop(input_data: CropPredictionRequest):
    try:
        result = CropService.recommend_crop(input_data)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": result
            }
        )

    except AppException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "message": e.message
            }
        )