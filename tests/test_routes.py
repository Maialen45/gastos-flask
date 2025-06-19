import pytest
from app import create_app
from app.extensions import db
from app.models import usuario

@pytest.fixture
def app():
    app = create_app('testing')
    with app.test_client():
        with app.app_context():
            db.create_all()
            yield app
            db.session.remove()
            db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    response = client.post('/register', data={
        'username': 'Pedro',
        'password': '123456'
    })
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Bienvenido Pedro' in html

def test_register_empty_username(client):
    response = client.post('/register', data={
        'username': '',
        'password': '123456'
    })
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Todos los campos son obligatorios' in html

def test_register_password(client):
    response = client.post('/register', data={
        'username': 'Pedro',
        'password': '123'
    })
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Contraseña muy corta' in html