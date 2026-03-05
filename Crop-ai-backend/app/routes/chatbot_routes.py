from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.chatbot_service import ChatbotService
from app.utils.custom_exception import AppException


chatbot_bp = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"]
)


@chatbot_bp.post("/message")
async def chat(message: dict):
    try:

        user_message = message.get("message")

        if not user_message:
            raise AppException("Message is required", 400)

        result = ChatbotService.get_response(user_message)

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