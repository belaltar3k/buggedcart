import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'database.db'

from .models import Product


def seed_products():
    if Product.query.count() > 0:
        return

    products = [
        Product(name='iPhone 14 Pro', price=999.99, description='Latest smartphone'),
        Product(name='MacBook Pro', price=1999.99, description='Professional laptop'),
        Product(name='Samsung Galaxy S23', price=799.99, description='Android smartphone'),
        Product(name='iPad Air', price=599.99, description='Tablet device'),
        Product(name='AirPods Pro', price=249.99, description='Wireless earbuds'),
    ]
    db.session.add_all(products)
    db.session.commit()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SECRET_KEY'] = 'thisisunsafe'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH.as_posix()}'

    db.init_app(app)

    with app.app_context():
        db.create_all()
        seed_products()

    from .routes import main
    app.register_blueprint(main)

    return app