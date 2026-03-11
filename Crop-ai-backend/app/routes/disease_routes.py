from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse

from app.services.disease_service import DiseaseService
from app.utils.custom_exception import AppException
from app.utils.jwt_helper import get_user_from_token


disease_bp = APIRouter(
    prefix="/disease",
    tags=["Plant Disease Detection"]
)


@disease_bp.post("/predict")
async def predict_disease(
    request: Request,
    file: UploadFile = File(...)
):
    try:
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_id = get_user_from_token(token)

        # Read image bytes
        image_bytes = await file.read()

        # Call service
        result = DiseaseService.predict_disease(
            image_bytes=image_bytes
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