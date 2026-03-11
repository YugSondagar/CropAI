import jwt
import os
from app.utils.custom_exception import AppException

JWT_SECRET = os.environ.get("JWT_SECRET", "super-secret-key-123")
JWT_ALGORITHM = "HS256"


def get_user_from_token(token: str) -> str:
    """
    Decode a JWT Bearer token and return the user identifier (email = 'sub').
    Raises AppException on failure.
    """
    if not token:
        raise AppException("Authorization token missing", 401)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise AppException("Invalid token payload", 401)
        return user_id
    except jwt.ExpiredSignatureError:
        raise AppException("Token has expired", 401)
    except jwt.InvalidTokenError:
        raise AppException("Invalid token", 401)
