from app.utils.custom_exception import AppException
from app.services.chat_history_service import ChatHistoryService
from app.services.activity_service import ActivityService


class ChatbotService:

    @staticmethod
    def get_response(user_id: str, message: str):
        """
        Process chatbot message, store chat history
        and log user activity
        """

        try:

            # Basic placeholder response (can replace with LLM later)
            reply = f"You said: {message}"

            # Save chat history
            ChatHistoryService.save_chat(
                user_id=user_id,
                message=message,
                response=reply
            )

            # Save user activity
            ActivityService.log_activity(
                user_id=user_id,
                activity="chatbot_interaction",
                details="User interacted with AI chatbot"
            )

            return {
                "reply": reply
            }

        except Exception as e:
            raise AppException(
                f"Chatbot error: {str(e)}",
                500
            )