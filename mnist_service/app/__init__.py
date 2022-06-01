import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from .config import config
from .core import db
from .core import models
from .core.schemas import ma
from .core.views import bp


migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config[os.environ.get('APPLICATION_ENV')])
    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(
        bp,
        url_prefix='/api/MNIST/v1'
    )
    
    with app.app_context():
        db.create_all()
        ma.init_app(app)

    return app


if __name__ == '__main__':
    create_app()
