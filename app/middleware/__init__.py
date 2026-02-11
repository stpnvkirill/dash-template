from flask import Flask, Response


def init_middlewares(app: Flask):
    @app.before_request
    def before_request(): ...

    @app.after_request
    def after_request(response: Response):
        return response
