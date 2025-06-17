from flask import Flask
from .extensions import db, migrate, jwt

def create_app(config_class='instance.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .models import gastos, usuario, ingresos
    from .routes.gastos import gastos_bp
    from .routes.auth import auth_bp
    from .routes.ingresos import ingresos_bp
    app.register_blueprint(gastos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ingresos_bp)


    return app