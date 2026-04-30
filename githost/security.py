"""Security utilities: CSRF protection, rate limiting, input validation."""

import re
import time
import hashlib
import secrets
import logging
from collections import defaultdict
from functools import wraps
from typing import Optional

from flask import request, session, abort, make_response

logger = logging.getLogger(__name__)


# --- CSRF Protection ---

def generate_csrf_token() -> str:
    """Generate a CSRF token and store it in the session."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def validate_csrf_token(token: str) -> bool:
    """Validate a CSRF token against the session."""
    return secrets.compare_digest(token, session.get("csrf_token", ""))


def csrf_protect(f):
    """Decorator to validate CSRF token on POST requests."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == "POST":
            token = request.form.get("csrf_token", "")
            if not validate_csrf_token(token):
                logger.warning("CSRF validation failed from %s", request.remote_addr)
                abort(403)
        return f(*args, **kwargs)
    return decorated


# --- Rate Limiting ---

class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self):
        self._requests: dict = defaultdict(list)
        self._blocked: dict = {}

    def is_rate_limited(self, key: str, max_requests: int = 30, window_seconds: int = 60) -> bool:
        """Check if a key has exceeded the rate limit."""
        now = time.time()

        # Check if temporarily blocked
        if key in self._blocked:
            if now < self._blocked[key]:
                return True
            del self._blocked[key]

        # Clean old entries
        self._requests[key] = [t for t in self._requests[key] if now - t < window_seconds]

        if len(self._requests[key]) >= max_requests:
            self._blocked[key] = now + window_seconds  # Block for one more window
            logger.warning("Rate limit exceeded for %s", key)
            return True

        self._requests[key].append(now)
        return False

    def get_remaining(self, key: str, max_requests: int = 30, window_seconds: int = 60) -> int:
        """Get remaining requests in the current window."""
        now = time.time()
        self._requests[key] = [t for t in self._requests[key] if now - t < window_seconds]
        return max(0, max_requests - len(self._requests[key]))


# Global rate limiter instance
rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 30, window_seconds: int = 60):
    """Decorator to apply rate limiting to a route."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = f"{request.remote_addr}:{request.path}"
            if rate_limiter.is_rate_limited(key, max_requests, window_seconds):
                retry_after = window_seconds
                response = make_response(
                    f"Rate limit exceeded. Try again in {retry_after} seconds.", 429
                )
                response.headers["Retry-After"] = str(retry_after)
                return response
            return f(*args, **kwargs)
        return decorated
    return decorator


# --- Input Validation ---

# Characters that should never appear in filenames
DANGEROUS_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

# Max filename length
MAX_FILENAME_LENGTH = 255

# Max password length (prevent DoS via long hash computation)
MAX_PASSWORD_LENGTH = 128


def sanitize_filename(filename: str) -> str:
    """Sanitize a filename to prevent path traversal and other attacks."""
    # Remove path components
    filename = filename.split("/")[-1].split("\\")[-1]
    # Remove dangerous characters
    filename = DANGEROUS_FILENAME_CHARS.sub("", filename)
    # Limit length
    filename = filename[:MAX_FILENAME_LENGTH]
    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")
    return filename or "unnamed"


def validate_password(password: str) -> tuple[bool, str]:
    """Validate a password input. Returns (is_valid, error_message)."""
    if not password:
        return True, ""  # Password is optional
    if len(password) > MAX_PASSWORD_LENGTH:
        return False, f"Password too long (max {MAX_PASSWORD_LENGTH} chars)"
    return True, ""


def validate_expiry_days(days: int) -> tuple[bool, str]:
    """Validate expiry days input."""
    if days < 1:
        return False, "Expiry must be at least 1 day"
    if days > 365:
        return False, "Expiry cannot exceed 365 days"
    return True, ""


def validate_max_views(views: int) -> tuple[bool, str]:
    """Validate max views input."""
    if views < 0:
        return False, "Max views cannot be negative"
    if views > 100000:
        return False, "Max views cannot exceed 100,000"
    return True, ""


def validate_url(url: str) -> tuple[bool, str]:
    """Validate a URL for upload-from-URL."""
    if not url:
        return False, "URL is required"
    if not url.startswith(("http://", "https://")):
        return False, "URL must start with http:// or https://"
    if len(url) > 2048:
        return False, "URL too long"
    # Block internal/private IPs
    import ipaddress
    from urllib.parse import urlparse
    try:
        parsed = urlparse(url)
        if parsed.hostname:
            try:
                ip = ipaddress.ip_address(parsed.hostname)
                if ip.is_private or ip.is_loopback or ip.is_reserved:
                    return False, "Cannot download from private/internal URLs"
            except ValueError:
                # Not an IP, that's fine (it's a hostname)
                pass
    except Exception:
        return False, "Invalid URL format"
    return True, ""


# --- Security Headers ---

def add_security_headers(response):
    """Add security headers to a Flask response."""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "img-src 'self' data:; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; "
        "frame-ancestors 'none'"
    )
    return response
