from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.auth_service import AuthService
from app.utils.custom_exception import AppException
from app.models.user_model import UserRegister, UserLogin


auth_bp = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_bp.post("/register")
async def register(user: UserRegister):
    try:
        result = AuthService.register_user(user)

        return JSONResponse(
            status_code=201,
            content={"success": True, "data": result}
        )

    except AppException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"success": False, "message": e.message}
        )


@auth_bp.post("/login")
async def login(user: UserLogin):
    try:
        result = AuthService.login_user(user)

        return JSONResponse(
            status_code=200,
            content={"success": True, "data": result}
        )

    except AppException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"success": False, "message": e.message}
        )