from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.database.mongo import MongoDB
from app.utils.custom_exception import AppException


history_bp = APIRouter(
    prefix="/history",
    tags=["User History"]
)


# -----------------------------
# Get Chat History
# -----------------------------
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
                "data": chats
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
                "data": crops
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
                "data": diseases
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
                "data": activities
            }
        )

    except Exception as e:
        raise AppException(str(e), 500)