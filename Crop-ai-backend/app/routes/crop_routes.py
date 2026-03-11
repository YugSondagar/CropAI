from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.crop_service import CropService
from app.utils.custom_exception import AppException
from app.utils.jwt_helper import get_user_from_token


crop_bp = APIRouter(
    prefix="/crop",
    tags=["Crop Recommendation"]
)


@crop_bp.post("/recommend")
async def recommend_crop(request: Request):
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = get_user_from_token(token)

        crop_inputs = await request.json()

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