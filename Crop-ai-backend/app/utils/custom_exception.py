import logging
from typing import Optional


logger = logging.getLogger(__name__)


class AppException(Exception):
    """
    Base Application Exception

    Used for:
    - Validation errors
    - Authentication errors
    - Business logic errors
    """

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None
    ):
        super().__init__(message)

        self.message = message
        self.status_code = status_code
        self.error_code = error_code

        # Log immediately when exception is created
        logger.error(
            f"AppException Raised | "
            f"Status: {status_code} | "
            f"Error Code: {error_code} | "
            f"Message: {message}"
        )

    def to_dict(self):
        """
        Standard API error response format
        """
        response = {
            "success": False,
            "error": {
                "message": self.message,
                "status_code": self.status_code
            }
        }

        if self.error_code:
            response["error"]["error_code"] = self.error_code

        return response


# ==========================================
# Global Exception Handlers (Flask Binding)
# ==========================================

def register_error_handlers(app):
    """
    Register global error handlers
    """

    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return error.to_dict(), error.status_code

    @app.errorhandler(404)
    def handle_404_error(_):
        logger.warning("404 - Route not found")
        return {
            "success": False,
            "error": {
                "message": "Resource not found",
                "status_code": 404
            }
        }, 404

    @app.errorhandler(500)
    def handle_500_error(error):
        logger.critical(f"Internal Server Error: {str(error)}")
        return {
            "success": False,
            "error": {
                "message": "Internal server error",
                "status_code": 500
            }
        }, 500

    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        logger.exception(f"Unhandled Exception: {str(error)}")
        return {
            "success": False,
            "error": {
                "message": "Unexpected error occurred",
                "status_code": 500
            }
        }, 500