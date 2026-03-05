from app.utils.custom_exception import AppException


class ChatbotService:

    @staticmethod
    def get_response(message: str):

        try:
            # Placeholder logic
            return {
                "reply": f"You said: {message}"
            }

        except Exception as e:
            raise AppException(
                f"Chatbot error: {str(e)}",
                500
            )