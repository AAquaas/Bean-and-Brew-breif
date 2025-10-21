##################################################
############### PYTHON PACKAGES ##################
##################################################

import encodings
from decimal import Decimal
import os
import os.path as op
from datetime import datetime as dt
from sqlalchemy import Column, Integer, DateTime
from flask import Flask, render_template, send_from_directory, url_for, redirect, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.event import listens_for
from markupsafe import Markup
from flask_admin import Admin, form
from flask_admin.form import rules
from flask_admin.contrib import sqla, rediscli
from flask import session as login_session
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy import select
import operator
from werkzeug.utils import secure_filename
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy import update
from wtforms import PasswordField
#new imports
from sqlalchemy.ext.hybrid import hybrid_property

from jinja2 import TemplateNotFound  # Import TemplateNotFound exception
import logging

#for xml files
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree
from datetime import datetime as dt

##################################################
##################################################
##################################################

# setting up admin
admin = Admin()
app = Flask(__name__, static_folder='static')

# configuring the app, bcrypt and admin
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\753503\\DB.Browser.for.SQLite-v3.13.1-win64\\coffee_orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'this is a secret key '
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
login_manager.init_app(app)
admin.init_app(app)

# setting up thr upload folder
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#log errors
app_dir = op.realpath(os.path.dirname(__file__))
logger = logging.getLogger('app_logger')
logger.setLevel(logging.DEBUG)  #set the logger level to DEBUG or higher

# Create a file handler and set the level to DEBUG
log_file_path = op.join(app_dir, 'app.log')
handler = logging.FileHandler(log_file_path)
# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)


# error display
@app.errorhandler(404)
def page_not_found(e):
    logger.error('Page not found: %s', e)
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error('Page not found: %s', e)
    db.session.rollback()
    return render_template('500.html'), 500



# creating relivant tables
class MenuItems(db.Model):
    __tablename__ = "beverage"
    beverage_id = db.Column(db.Integer, primary_key=True)
    beverage_name = db.Column(db.Unicode(64), nullable=False)
    beverage_price = db.Column(db.Numeric(10, 2), nullable=False)
    beverage_type = db.Column(db.String(30), nullable=False)
    file_image = db.Column(db.String(30), nullable=False)

    cartitems = relationship("CartItem", back_populates="beverage")

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

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def __repr__(self):
    return f'<User {self.username}>'

class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

def __str__(self):
    return self.username

class Message(db.Model, UserMixin):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(80), nullable=False)


def __str__(self):
    return f"{self.name}: {self.message}"


# setting up user login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


# main website hosting
# subtitle is the name at the top of the tab

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', subtitle="Home")


@app.route('/welcome')
def welcome():
    return render_template('welcome.html', subtitle="Order as a guest")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        customer = Customer.query.filter_by(username=username).first()
        if customer and bcrypt.check_password_hash(customer.password, password):
            #db.session["username"] = username
            login_session['username'] = username
            login_user(customer)
            return redirect(url_for('welcome'))
        else:
            flash("Invalid username or password")
            return redirect(url_for('login'))
    return render_template('login.html', subtitle="Login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        terms = request.form['terms']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        checkemail = Customer.query.filter(Customer.email == email).first()
        checkuser = Customer.query.filter(Customer.username == username).first()

        if not terms:
            flash("Please accept our terms to continue")

        if checkemail != None:
            flash("Please register using a different email.")

            return render_template("register.html", subtitle="Register")
        elif checkuser is not None:
            flash("Username already exists !")

            return render_template("register.html")

        else:
            new_customer = Customer(username=username, email=email, password=hashed_password)
            db.session.add(new_customer)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/table_booking')
def table_booking():
    return render_template('table_booking.html', subtitle="Book a table")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']
        new_message = Message(name=name, message=message)
        db.session.add(new_message)
        db.session.commit()

    return render_template('contact.html', subtitle="Contact us!")




if __name__ == "__main__":
    app_dir = op.realpath(os.path.dirname(__file__))
    with app.app_context():
        db.create_all() # create a database
    app.run(debug=True)