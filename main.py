from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required
import os
import os.path as op
import logging
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from decimal import Decimal

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


"""
# creating relivant tables
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
"""
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


# setting up user login
@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


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


@app.route('/login')
def login():
    return render_template('login.html', subtitle="Login")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        checkemail = customer.query.filter(customer.email == email).first()
        checkuser = customer.query.filter(customer.username == username).first()

        if checkemail != None:
            flash("Please register using a different email.")

            return render_template("register.html")
        elif checkuser is not None:
            flash("Username already exists !")

            return render_template("register.html")

        else:
            new_customer = customer(username=username, email=email, password=hashed_password)
            db.session.add(new_customer)
            db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/table_booking')
def table_booking():
    return render_template('table_booking.html', subtitle="Book a table")




if __name__ == "__main__":
    app_dir = op.realpath(os.path.dirname(__file__))
    with app.app_context():
        db.create_all() # create a database
    app.run(debug=True)