from flask import Response


class BaseMiddleware:
    """Base class for Flask middleware."""

    def before(self) -> None:
        """Called before request processing."""
        pass

    def after(self, response: Response) -> Response:
        """Called after request processing."""
        return response
