from app import create_app
from app.extensions import db
from app.models.gastos import Gastos
from datetime import date

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)