from flask import Flask
from .extensions import db, migrate, jwt

def create_app(config_class='instance.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .models import gastos, usuario
    from .routes.gastos import main_bp
    from .routes.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)


    return app