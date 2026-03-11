from app.utils.custom_exception import AppException
from app.services.chat_history_service import ChatHistoryService
from app.services.activity_service import ActivityService
import os
from groq import Groq


class ChatbotService:

    @staticmethod
    def get_response(user_id: str, message: str):
        """
        Process chatbot message using Groq LLaMA-3.3-70b-versatile,
        store chat history and log user activity.
        """

        try:
            # Build conversation messages
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are CropAI, a helpful expert assistant specialized in agriculture, "
                        "crop farming, plant diseases, soil management, and sustainable farming practices. "
                        "Provide concise, practical, and accurate answers for farmers and agronomists."
                    )
                }
            ]

            # Add the current user message
            messages.append({"role": "user", "content": message})

            # Call Groq API
            client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7,
                max_tokens=1024,
            )

            reply = completion.choices[0].message.content

            # Save chat history with user_id
            ChatHistoryService.save_chat(
                user_id=user_id,
                user_message=message,
                bot_reply=reply
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
