"""User-Agent middleware for extracting client information."""

import ipaddress
import logging

from flask import g, request
from user_agents import parse

from .base import BaseMiddleware

logger = logging.getLogger(__name__)


def validate_ip_address(ip: str | None) -> str:
    """Validate and sanitize IP address.

    Args:
        ip: IP address string to validate.

    Returns:
        Valid IP address string or '0.0.0.0' if invalid.
    """
    if not ip:
        return "0.0.0.0"

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        logger.warning(f"Invalid IP address format: {ip}")
        return "0.0.0.0"

    return ip


class UserAgentMiddleware(BaseMiddleware):
    """Middleware to extract and store user agent and IP information."""

    def before(self) -> None:
        """Extract IP and user agent from request."""
        # Get IP address from headers or remote address
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr

        # Validate IP address
        g.ip_address = validate_ip_address(ip_address)

        # Parse user agent
        ua_string = request.headers.get("User-Agent", "Unknown")
        g.user_agent = parse(ua_string)
