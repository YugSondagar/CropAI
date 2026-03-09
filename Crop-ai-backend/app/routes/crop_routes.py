from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.crop_service import CropService
from app.utils.custom_exception import AppException


crop_bp = APIRouter(
    prefix="/crop",
    tags=["Crop Recommendation"]
)


@crop_bp.post("/recommend")
async def recommend_crop(data: dict):

    try:

        user_id = data.get("user_id")

        if not user_id:
            raise AppException("User ID is required", 400)

        # remove user_id from crop inputs
        crop_inputs = {k: v for k, v in data.items() if k != "user_id"}

        result = CropService.recommend_crop(
            user_id=user_id,
            input_data=crop_inputs
        )

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