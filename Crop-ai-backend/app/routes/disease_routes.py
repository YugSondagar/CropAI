from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
import logging

from app.services.disease_service import DiseaseService
from app.utils.custom_exception import AppException
from app.utils.jwt_helper import get_user_from_token

logger = logging.getLogger(__name__)

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
        # Get token from header
        auth_header = request.headers.get("Authorization", "")
        logger.info(f"Disease auth header: {auth_header}")
        
        token = auth_header.replace("Bearer ", "").strip()
        
        # Make token optional for debugging - use a default user if not provided
        if not token:
            user_id = "anonymous_user"
            logger.warning("No token provided for disease prediction, using anonymous user")
        else:
            try:
                user_id = get_user_from_token(token)
            except AppException as e:
                logger.warning(f"Disease token validation failed: {e.message}, using anonymous user")
                user_id = "anonymous_user"

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
                "data": {
                    "disease": result["disease"],
                    "confidence": result["confidence"],
                    "predicted_index": result["predicted_index"],
                    "cause": result["cause"],
                    "prevention": result["prevention"],
                    "top_probabilities": result["top_probabilities"]
                }
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
    except Exception as e:
        logger.error(f"Disease prediction error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal error: {str(e)}"
            }
        )

