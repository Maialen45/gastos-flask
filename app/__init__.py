from flask import Flask
from .extensions import db, migrate

def create_app(config_class='instance.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app