from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging

from app.services.crop_service import CropService
from app.utils.custom_exception import AppException
from app.utils.jwt_helper import get_user_from_token

logger = logging.getLogger(__name__)

crop_bp = APIRouter(
    prefix="/crop",
    tags=["Crop Recommendation"]
)


@crop_bp.post("/recommend")
async def recommend_crop(request: Request):
    try:
        # Get token from header
        auth_header = request.headers.get("Authorization", "")
        logger.info(f"Crop auth header: {auth_header}")
        
        token = auth_header.replace("Bearer ", "").strip()
        
        # Make token optional for debugging - use a default user if not provided
        if not token:
            user_id = "anonymous_user"
            logger.warning("No token provided for crop recommendation, using anonymous user")
        else:
            try:
                user_id = get_user_from_token(token)
            except AppException as e:
                logger.warning(f"Crop token validation failed: {e.message}, using anonymous user")
                user_id = "anonymous_user"

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
    except Exception as e:
        logger.error(f"Crop recommendation error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal error: {str(e)}"
            }
        )

