"""Exception handlers and error responses."""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

logger = logging.getLogger(__name__)


class PatentAppException(Exception):
    """Base exception for patent application errors."""

    def __init__(self, message: str, status_code: int = 500, error_code: str = "INTERNAL_ERROR"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)


class ValidationException(PatentAppException):
    """Validation error exception."""

    def __init__(self, message: str):
        super().__init__(message, status_code=400, error_code="VALIDATION_ERROR")


class NotFoundException(PatentAppException):
    """Resource not found exception."""

    def __init__(self, resource: str):
        message = f"{resource} not found"
        super().__init__(message, status_code=404, error_code="NOT_FOUND")


class UnauthorizedException(PatentAppException):
    """Unauthorized access exception."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401, error_code="UNAUTHORIZED")


class ForbiddenException(PatentAppException):
    """Forbidden access exception."""

    def __init__(self, message: str = "Access denied"):
        super().__init__(message, status_code=403, error_code="FORBIDDEN")


class ConflictException(PatentAppException):
    """Conflict exception (e.g., duplicate resource)."""

    def __init__(self, message: str):
        super().__init__(message, status_code=409, error_code="CONFLICT")


class ExternalServiceException(PatentAppException):
    """External service failure exception."""

    def __init__(self, service: str, message: str = "Service unavailable"):
        full_message = f"{service} error: {message}"
        super().__init__(full_message, status_code=503, error_code="SERVICE_UNAVAILABLE")


class RateLimitException(PatentAppException):
    """Rate limit exceeded exception."""

    def __init__(self, retry_after: int = 60):
        super().__init__(
            "Too many requests",
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED"
        )
        self.retry_after = retry_after


def register_exception_handlers(app: FastAPI):
    """Register all exception handlers with the FastAPI app."""

    @app.exception_handler(PatentAppException)
    async def patent_exception_handler(request: Request, exc: PatentAppException):
        """Handle custom patent application exceptions."""
        logger.error(f"{exc.error_code}: {exc.message}", extra={
            "path": request.url.path,
            "status_code": exc.status_code,
        })

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.error_code,
                "message": exc.message,
                "status": exc.status_code,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"][1:]),
                "message": error["msg"],
            })

        logger.warning(f"Validation error: {errors}", extra={"path": request.url.path})

        return JSONResponse(
            status_code=400,
            content={
                "error": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": errors,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True, extra={
            "path": request.url.path,
        })

        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "status": 500,
            },
        )


class APIResponse:
    """Standard API response formatter."""

    @staticmethod
    def success(data: any, message: str = "Success") -> dict:
        """Format successful response."""
        return {
            "success": True,
            "message": message,
            "data": data,
        }

    @staticmethod
    def error(error_code: str, message: str, status_code: int = 400) -> dict:
        """Format error response."""
        return {
            "success": False,
            "error": error_code,
            "message": message,
            "status": status_code,
        }

    @staticmethod
    def paginated(items: list, total: int, skip: int, limit: int) -> dict:
        """Format paginated response."""
        return {
            "items": items,
            "total": total,
            "skip": skip,
            "limit": limit,
            "pages": (total + limit - 1) // limit,
        }
