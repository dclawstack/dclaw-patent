"""Input validation and security utilities."""

import re
from typing import Optional
from datetime import date, datetime


class ValidationError(ValueError):
    """Custom validation error."""

    pass


class InputValidator:
    """Validate user inputs for security and correctness."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_jurisdiction(jurisdiction: str) -> bool:
        """Validate patent jurisdiction code."""
        valid_jurisdictions = ['US', 'EP', 'JP', 'CN', 'IN', 'GB', 'DE', 'FR', 'CA', 'AU', 'KR']
        return jurisdiction in valid_jurisdictions

    @staticmethod
    def validate_patent_status(status: str) -> bool:
        """Validate patent status."""
        valid_statuses = ['draft', 'filed', 'prosecution', 'issued', 'abandoned', 'expired']
        return status in valid_statuses

    @staticmethod
    def validate_date_range(from_date: date, to_date: date) -> bool:
        """Validate that from_date <= to_date."""
        return from_date <= to_date

    @staticmethod
    def validate_future_date(target_date: date) -> bool:
        """Validate that date is not in the past (for deadlines)."""
        return target_date >= date.today()

    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input (prevent XSS, strip excessive whitespace)."""
        if not isinstance(text, str):
            raise ValidationError("Text must be a string")

        if len(text) > max_length:
            raise ValidationError(f"Text exceeds maximum length of {max_length}")

        # Remove control characters
        sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        return sanitized.strip()

    @staticmethod
    def validate_patent_title(title: str) -> bool:
        """Validate patent title."""
        if not title or not isinstance(title, str):
            return False
        if len(title) < 5 or len(title) > 200:
            return False
        return True

    @staticmethod
    def validate_claim_text(claims: str) -> bool:
        """Validate patent claims."""
        if not claims or not isinstance(claims, str):
            return False
        if len(claims) < 20 or len(claims) > 50000:
            return False
        return True

    @staticmethod
    def validate_offset_limit(skip: int, limit: int) -> bool:
        """Validate pagination parameters."""
        return skip >= 0 and 1 <= limit <= 100

    @staticmethod
    def validate_no_sql_injection(value: str) -> bool:
        """Basic check for SQL injection patterns (defense in depth)."""
        dangerous_patterns = [
            r";\s*DROP",
            r";\s*DELETE",
            r";\s*INSERT",
            r";\s*UPDATE",
            r"--\s+",
            r"/\*.*\*/",
            "' OR '",
            "' OR 1=1",
            "1=1",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return False

        return True


class SecurityHeaders:
    """Security headers for HTTP responses."""

    @staticmethod
    def get_headers() -> dict:
        """Return security headers dictionary."""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'",
        }


class RateLimiter:
    """Simple rate limiting tracker (replace with Redis in production)."""

    _requests = {}

    @classmethod
    def is_rate_limited(cls, key: str, max_requests: int = 100, window_seconds: int = 60) -> bool:
        """Check if request should be rate limited."""
        import time

        now = time.time()

        if key not in cls._requests:
            cls._requests[key] = []

        # Remove old requests outside the window
        cls._requests[key] = [
            req_time for req_time in cls._requests[key]
            if now - req_time < window_seconds
        ]

        if len(cls._requests[key]) >= max_requests:
            return True

        cls._requests[key].append(now)
        return False
