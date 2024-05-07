from market import db, login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKey

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


shopping_list = db.Table('shopping_list',
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                         db.Column('product_id', db.Integer, db.ForeignKey('products.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(512), nullable=False)
    items = db.relationship('Products', backref='owned', lazy=True)
    shopping_list = db.relationship('Products', secondary=shopping_list, backref=db.backref('users', lazy=True))


class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float(), nullable=False)
    discount = db.Column(db.String(50), default=0)
    link = db.Column(db.String(500), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Product {self.name}'
