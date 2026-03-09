from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse

from app.services.disease_service import DiseaseService
from app.utils.custom_exception import AppException


disease_bp = APIRouter(
    prefix="/disease",
    tags=["Plant Disease Detection"]
)


@disease_bp.post("/predict")
async def predict_disease(
    user_id: str = Form(...),
    file: UploadFile = File(...)
):

    try:

        # Read image bytes
        image_bytes = await file.read()

        # Call service
        result = DiseaseService.predict_disease(
            user_id=user_id,
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