from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from datetime import datetime

from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException
from app.utils.jwt_helper import get_user_from_token
from app.utils.logger import logger


history_bp = APIRouter(
    prefix="/history",
    tags=["User History"]
)


def serialize_doc(doc):
    """Convert MongoDB document to JSON-safe dict (handles datetime)."""
    result = {}
    for key, value in doc.items():
        if isinstance(value, datetime):
            result[key] = value.isoformat()
        else:
            result[key] = value
    return result


# -----------------------------
# Get ALL activities for logged-in user (reads user from JWT token)
# -----------------------------
@history_bp.get("/activities/me")
async def get_my_activities(request: Request):
    try:
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.replace("Bearer ", "").strip()
        
        logger.info(f"HISTORY DEBUG: Received auth_header='{auth_header}'")
        logger.info(f"HISTORY DEBUG: Extracted token starts with: '{token[:30]}...' (len={len(token)})")
        
        if not token:
            return JSONResponse(status_code=401, content={"success": False, "message": "Authorization token missing"})

        try:
            user_id = get_user_from_token(token)
        except AppException as e:
            return JSONResponse(status_code=401, content={"success": False, "message": e.message})

        db = MongoDB.get_database()
        collection = db["user_activities"]

        activities = list(
            collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort("timestamp", -1).limit(50)
        )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": [serialize_doc(a) for a in activities]
            }
        )

    except Exception as e:
        raise AppException(str(e), 500)



@history_bp.get("/chat/{user_id}")
async def get_chat_history(user_id: str):

    try:

        db = MongoDB.get_database()
        collection = db["chat_history"]

        chats = list(
            collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort("timestamp", -1)
        )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": [serialize_doc(c) for c in chats]
            }
        )

    except Exception as e:
        raise AppException(str(e), 500)


# -----------------------------
# Get Crop History
# -----------------------------
@history_bp.get("/crop/{user_id}")
async def get_crop_history(user_id: str):

    try:

        db = MongoDB.get_database()
        collection = db["crop_recommendations"]

        crops = list(
            collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort("timestamp", -1)
        )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": [serialize_doc(c) for c in crops]
            }
        )

    except Exception as e:
        raise AppException(str(e), 500)


# -----------------------------
# Get Disease History
# -----------------------------
@history_bp.get("/disease/{user_id}")
async def get_disease_history(user_id: str):

    try:

        db = MongoDB.get_database()
        collection = db["disease_predictions"]

        diseases = list(
            collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort("timestamp", -1)
        )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": [serialize_doc(d) for d in diseases]
            }
        )

    except Exception as e:
        raise AppException(str(e), 500)


# -----------------------------
# Get User Activities
# -----------------------------
@history_bp.get("/activities/{user_id}")
async def get_activities(user_id: str):

    try:

        db = MongoDB.get_database()
        collection = db["user_activities"]

        activities = list(
            collection.find(
                {"user_id": user_id},
                {"_id": 0}
            ).sort("timestamp", -1)
        )

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": [serialize_doc(a) for a in activities]
            }
        )

    except Exception as e:
        raise AppException(str(e), 500)
