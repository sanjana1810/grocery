from flask_sqlalchemy import SQLAlchemy
from applications.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    password=db.Column(db.String(40), nullable=False)
    

    @property
    def cart_total(self):
        total=0
        for cart_item in self.cart:
            total+=cart_item.subtotal
        return total
    

class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, unique=True, nullable=False)
    

class Product(db.Model):
    __tablename__="product"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, unique=True, nullable=False)
    quantity=db.Column(db.Integer, nullable=False)
    description=db.Column(db.String, nullable=False)
    price=db.Column(db.Integer, nullable=False, default=40)
    image_filename=db.Column(db.String(255),nullable=False)
    category_id=db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    category=db.relationship('Category',backref=db.backref('products',lazy=True))

class CartItems(db.Model):
    __tablename__="cartitems"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    product=db.relationship('Product',backref='cart_items')
    user=db.relationship('User',backref='cart_items')
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), autoincrement=True)
    product_id=db.Column(db.Integer, db.ForeignKey('product.id'), autoincrement=True)
    quantity=db.Column(db.Integer, nullable=False,default=1)

    @property
    def subtotal(self):
        return self.quantity * self.product.price