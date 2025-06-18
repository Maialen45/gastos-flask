import pytest
from app import create_app
from app.extensions import db
from app.models import usuario

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-secret-key'
    })
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client, app):
    response = client.post('/register', data={
        'username': 'Pedro',
        'password': '123456'
    })
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert "<label>Confirmar Contraseña</label>" in html

    with app.app_context():
        user = usuario.Usuario.query.filter_by(username='Pedro').first()
        assert user is not None

def test_register_empty_username(client):
    response = client.post('/register', data={
        'username': '',
        'password': '123456'
    })
    assert response.status_code ==200
    html = response.data.decode('utf-8')
    print(html)
    assert 'Todos los campos son obligatorios' in html