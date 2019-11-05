# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from apps import settings
db = SQLAlchemy()
# import blueprints

from apps.translation.views import translation_bp
from apps.advance.views import advance_bp


def create_app():
    app = Flask(__name__, static_folder=settings.STATIC_DIR)
    app.register_blueprint(translation_bp, url_prefix=settings.API_PREFIX + '/translation')
    app.register_blueprint(advance_bp, url_prefix=settings.API_PREFIX + '/advance')
    # change your password
    app.config['SQLALCHEMY_DATABASE_URI'] \
        = 'mysql+pymysql://root:password@127.0.0.1:3306/file_go?charset=utf8mb4'
    app.config['SQLALCHEMY_POOL_SIZE'] = 6
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    CORS(app, supports_credentials=True, resources=r'/*')
    return app
