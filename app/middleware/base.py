from flask import Response


class BaseMiddlaware:
    def before(self):
        pass

    def after(self, response: Response):
        pass
