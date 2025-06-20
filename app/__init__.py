from flask import Flask
from .extensions import db, migrate, jwt

def create_app(config_class=None):
    app = Flask(__name__)
    if config_class == 'testing':
        app.config.from_mapping({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'JWT_SECRET_KEY': 'test-secret-key',
        })
    else: 
        app.config.from_object('instance.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .models import gastos, usuario, ingresos
    from .routes.gastos import gastos_bp
    from .routes.auth import auth_bp
    from .routes.ingresos import ingresos_bp
    from .routes.analisis import analisis_bp
    app.register_blueprint(gastos_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(ingresos_bp)
    app.register_blueprint(analisis_bp)



    return app