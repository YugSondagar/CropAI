import jwt
import os
from app.utils.logger import logger
from app.utils.custom_exception import AppException

JWT_SECRET = os.environ.get("JWT_SECRET", "super-secret-key-123")
JWT_ALGORITHM = "HS256"


def get_user_from_token(token: str) -> str:
    """
    Decode a JWT Bearer token and return the user identifier (email = 'sub').
    Raises AppException on failure.
    """
    logger.info(f"JWT DEBUG: Attempting to decode token starting with: {token[:30]}...")
    if not token:
        logger.error("JWT DEBUG: Token is empty/missing")
        raise AppException("Authorization token missing", 401)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        logger.info(f"JWT DEBUG: Successfully decoded. user_id={user_id}, payload keys={list(payload.keys())}")
        if not user_id:
            logger.error("JWT DEBUG: No 'sub' in payload")
            raise AppException("Invalid token payload", 401)
        return user_id
    except jwt.ExpiredSignatureError as e:
        logger.error(f"JWT DEBUG: Token expired: {str(e)}")
        raise AppException("Token has expired", 401)
    except jwt.InvalidTokenError as e:
        logger.error(f"JWT DEBUG: Invalid token: {str(e)}")
        raise AppException("Invalid token", 401)
    except Exception as e:
        logger.error(f"JWT DEBUG: Unexpected decode error: {str(e)}")
        raise AppException(f"Token decode failed: {str(e)}", 401)
