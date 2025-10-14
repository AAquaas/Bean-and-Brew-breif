from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from decimal import Decimal

admin = Admin()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\753503\\DB.Browser.for.SQLite-v3.13.1-win64\\coffee_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MenuItems(db.Model):
    __tablename__ = "beverage"
    beverage_id = db.Column(db.Integer, primary_key=True)
    beverage_name = db.Column(db.Unicode(64), nullable=False)
    beverage_price = db.Column(db.Numeric(10, 2), nullable=False)
    beverage_type = db.Column(db.String(30), nullable=False)
    file_image = db.Column(db.String(30), nullable=False)

    cartitems = relationship("CartItem", back_populates="food")

    def __repr__(self):
        return f'<food {self.food_name}'

class CartItem(db.Model):
    __tablename__ = "cartitem"
    cart_id = db.Column(db.Integer, primary_key=True)
    cart_name = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    beverage_id = db.Column(db.Integer, db.ForeignKey('beverage.beverage_id'), nullable=False)
    beverage = relationship("MenuItems", back_populates="cartitems")

    def __repr__(self):
        return f'<cartitem{self.cart_name} (x{self.quantity})>'

class user(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<user {self.username}>'


class customer (db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<customer {self.username}>'


# @app.before_request
# def setup():
#
#     db.create_all()
#     # adding menu items (drinks)
#     black_coffee = beverage(beverage_name="Black Coffee", beverage_price=5.00, beverage_type="Drink", file_image="black_coffee.jpg")
#     white_coffee = beverage(beverage_name="White Coffee", beverage_price=5.00, beverage_type="Drink", file_image="white_coffee.jpg")
#     cappuccino = beverage(beverage_name="Cappuccino", beverage_price=5.00, beverage_type="Drink", file_image="cappuccino.jpg")
#     latte = beverage(beverage_name="Latte", beverage_price=6.00, beverage_type="Drink", file_image="latte.jpg")
#     expresso = beverage(beverage_name="Expresso", beverage_price=3.00, beverage_type="Drink", file_image="expresso.jpg")
#     tea = beverage(beverage_name="Tea", beverage_price=5.00, beverage_type="Drink", file_image="tea.jpg")
#     hot_chocolate = beverage(beverage_name="Hot Chocolate", beverage_price=4.50, beverage_type="Drink", file_image="hot_chocolate.jpg")
#     # adding menu items (food)
#     vanilla = beverage(beverage_name="Vanilla Cake", beverage_price=2.50, beverage_type="Food", file_image="vanilla_cake.jpg")
#     chocolate_cake = beverage(beverage_name="Chocolate Cake", beverage_price=2.50, beverage_type="Food", file_image="carrot_cake.jpg")
#     carrot_cake = beverage(beverage_name="Carrot Cake", beverage_price=2.50, beverage_type="Food", file_image="chocolate_cake.jpg")
#     scones = beverage(beverage_name="scones", beverage_price=3.50, beverage_type="Food", file_image="scones.jpg")
#     cookie = beverage(beverage_name="Cookie", beverage_price=2.00, beverage_type="Food", file_image="cookie.jpg")
#     brownie = beverage(beverage_name="Brownie", beverage_price=2.00, beverage_type="Food", file_image="brownie.jpg")