from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.services.disease_service import DiseaseService
from app.utils.custom_exception import AppException


disease_bp = APIRouter(
    prefix="/disease",
    tags=["Disease Prediction"]
)


@disease_bp.post("/predict")
async def predict_disease(file: UploadFile = File(...)):
    try:

        if not file.content_type.startswith("image/"):
            raise AppException("Uploaded file must be an image", 400)

        image_bytes = await file.read()

        result = DiseaseService.predict_disease(image_bytes)

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

    except Exception:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error"
            }
        )