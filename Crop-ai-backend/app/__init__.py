from fastapi import FastAPI

from app.routes.auth_routes import auth_bp
from app.routes.crop_routes import crop_bp
from app.routes.disease_routes import disease_bp
from app.routes.chatbot_routes import chatbot_bp


def create_app():

    app = FastAPI(
        title="Crop AI API",
        description="AI Powered Crop Recommendation & Disease Detection",
        version="1.0"
    )

    @app.get("/")
    def home():
        return {
            "message": "Crop AI Backend Running",
            "docs": "/docs"
        }

    app.include_router(auth_bp)
    app.include_router(crop_bp)
    app.include_router(disease_bp)
    app.include_router(chatbot_bp)

    return app