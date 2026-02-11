from flask import Flask

from config import config

from .frontend import create_dash
from .middleware import init_middlewares


def get_application():
    server = Flask(__name__)
    server.config.from_object(config.server)
    init_middlewares(server)
    return create_dash(server=server)
