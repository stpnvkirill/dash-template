from flask import g, request
from user_agents import parse

from .base import BaseMiddleware


class UserAgentMiddleware(BaseMiddleware):
    def before(self) -> None:
        if request.headers.getlist("X-Forwarded-For"):
            ip_address = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip_address = request.remote_addr

        ua_string = request.headers.get("User-Agent", "Unknown")

        g.ip_address = ip_address
        g.user_agent = parse(ua_string)
