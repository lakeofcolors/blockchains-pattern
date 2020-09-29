#!/usr/bin/env python
from flask import Flask
from .settings import DevelopmentConfig
from .routes import blockchain

def create_app(config):

    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(blockchain)
    return app


if __name__ == "__main__":
    create_app(Config)
