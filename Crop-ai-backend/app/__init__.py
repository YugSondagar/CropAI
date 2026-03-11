from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

from app.routes.auth_routes import auth_bp
from app.routes.crop_routes import crop_bp
from app.routes.disease_routes import disease_bp
from app.routes.chatbot_routes import chatbot_bp
from app.routes.history_routes import history_bp


def create_app():

    app = FastAPI(
        title="Crop AI API",
        description="AI Powered Crop Recommendation & Disease Detection",
        version="1.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Get the frontend path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    frontend_path = os.path.join(project_root, "Crop-ai-frontend")

    # Include API routers FIRST (they take priority)
    app.include_router(auth_bp, prefix="/api")
    app.include_router(crop_bp, prefix="/api")
    app.include_router(disease_bp, prefix="/api")
    app.include_router(chatbot_bp, prefix="/api")
    app.include_router(history_bp, prefix="/api")

    # Serve static files from frontend (for CSS, JS, images, assets)
    if os.path.exists(frontend_path):
        app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
        app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")
        app.mount("/images", StaticFiles(directory=os.path.join(frontend_path, "images")), name="images")
        app.mount("/assets", StaticFiles(directory=os.path.join(frontend_path, "assets")), name="assets")

    # Root route - serve index.html
    @app.get("/")
    def root():
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {
            "message": "Crop AI Backend Running",
            "docs": "/docs"
        }

    # Serve HTML pages for known routes
    @app.get("/{page}")
    def serve_page(page: str):
        # Skip API routes and static files
        if page.startswith("api") or page.startswith("static"):
            return JSONResponse({"error": "Not found"}, status_code=404)
        
        if page == "docs":
            return JSONResponse({"error": "Not found"}, status_code=404)
        
        # Check for HTML files directly
        if page.endswith('.html'):
            page_path = os.path.join(frontend_path, page)
            if os.path.exists(page_path):
                return FileResponse(page_path)
        
        # Map short page names to HTML files
        html_files = {
            "index": "index.html",
            "login": "login.html",
            "register": "register.html",
            "dashboard": "dashboard.html",
            "crop": "crop.html",
            "disease": "disease.html",
            "chatbot": "chatbot.html",
            "history": "history.html"
        }
        
        if page in html_files:
            page_path = os.path.join(frontend_path, html_files[page])
            if os.path.exists(page_path):
                return FileResponse(page_path)
        
        # Default to index.html for SPA-like behavior
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        return {
            "message": "Crop AI Backend Running",
            "docs": "/docs"
        }

    return app
