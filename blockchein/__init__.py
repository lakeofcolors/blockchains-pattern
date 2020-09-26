#!/usr/bin/env python
from flask import Flask
from .settings import DevelopmentConfig

def create_app(config):

    app = Flask(__name__)

    app.config.from_object(config)

    return app


if __name__ == "__main__":
    create_app(Config)
