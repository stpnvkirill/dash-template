from flask import Flask, Response

from .ua import UserAgentMiddleware


def init_middlewares(app: Flask):
    mlist = [UserAgentMiddleware()]

    @app.before_request
    def before_request():
        for m in mlist:
            m.before()

    @app.after_request
    def after_request(response: Response):
        for m in mlist:
            response = m.after(response)
        return response
