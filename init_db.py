from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv

from server.app.models import db, Catalog, Product, User, Review, Wishlist, Cart, CartItem, Payment
from server.app.views import views

ma = Marshmallow()
migrate = Migrate()

def create_app():
    """Create and configure the Flask application."""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object('server.app.config.Config')

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(views)

    return app

def run_flask_command(command, *args):
    """Run a Flask CLI command."""
    try:
        cmd_list = ['flask'] + command.split() + list(args)
        subprocess.run(cmd_list, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{' '.join(cmd_list)}': {e}")

def create_migrations():
    """Initialize Flask-Migrate and create migration scripts if they don't exist."""
    if not os.path.exists('migrations'):
        run_flask_command('db init')
        print("Migrations folder created.")
    else:
        print("Migrations folder already exists.")

def apply_migrations():
    """Apply migrations to the database."""
    run_flask_command('db migrate', '-m', 'Initial migration')
    run_flask_command('db upgrade')
    print("Database migrated.")

def seed_catalogs():
    catalogs = [
        Catalog(name="Men's Clothing"),
        Catalog(name="Women's Clothing"),
        Catalog(name="Kids' Clothing"),
        Catalog(name="Accessories"),
        Catalog(name="Footwear")
    ]
    db.session.add_all(catalogs)
    db.session.commit()

def seed_products():
    products = [
        Product(name="Men's T-Shirt", price=1200, image_path="mens_tshirt.jpg", quantity=50, catalog_id=1, size="L", color="Blue", description="Comfortable cotton t-shirt for men."),
        Product(name="Women's Dress", price=2500, image_path="womens_dress.jpg", quantity=30, catalog_id=2, size="M", color="Red", description="Elegant summer dress for women."),
        Product(name="Kids' Jacket", price=1800, image_path="kids_jacket.jpg", quantity=20, catalog_id=3, size="S", color="Green", description="Warm jacket for kids."),
        Product(name="Leather Belt", price=1500, image_path="leather_belt.jpg", quantity=40, catalog_id=4, size="N/A", color="Brown", description="Stylish leather belt for all occasions."),
        Product(name="Running Shoes", price=3000, image_path="running_shoes.jpg", quantity=25, catalog_id=5, size="42", color="Black", description="Comfortable running shoes for all terrains.")
    ]
    db.session.add_all(products)
    db.session.commit()

def seed_users():
    users = [
        User(name="Alice", password="password123", email="alice@example.com"),
        User(name="Bob", password="password123", email="bob@example.com"),
        User(name="Charlie", password="password123", email="charlie@example.com"),
        User(name="David", password="password123", email="david@example.com"),
        User(name="Eve", password="password123", email="eve@example.com")
    ]
    db.session.add_all(users)
    db.session.commit()

def seed_reviews():
    reviews = [
        Review(product_id=1, user_id=1, rating=5, comment="Great quality t-shirt, very comfortable!"),
        Review(product_id=2, user_id=2, rating=4, comment="Beautiful dress, fits perfectly."),
        Review(product_id=3, user_id=3, rating=3, comment="Jacket is okay, but size runs a bit small."),
        Review(product_id=4, user_id=4, rating=5, comment="Excellent belt, very durable."),
        Review(product_id=5, user_id=5, rating=4, comment="Good running shoes, very comfortable for long runs.")
    ]
    db.session.add_all(reviews)
    db.session.commit()

def seed_wishlist():
    wishlists = [
        Wishlist(user_id=1, product_id=2),
        Wishlist(user_id=2, product_id=4),
        Wishlist(user_id=3, product_id=1),
        Wishlist(user_id=4, product_id=3),
        Wishlist(user_id=5, product_id=5)
    ]
    db.session.add_all(wishlists)
    db.session.commit()

def seed_cart():
    carts = [
        Cart(user_id=1),
        Cart(user_id=2),
        Cart(user_id=3),
        Cart(user_id=4),
        Cart(user_id=5)
    ]
    db.session.add_all(carts)
    db.session.commit()

def seed_cart_items():
    cart_items = [
        CartItem(cart_id=1, product_id=1, quantity=2, list_price=1200),
        CartItem(cart_id=2, product_id=2, quantity=1, list_price=2500),
        CartItem(cart_id=3, product_id=3, quantity=1, list_price=1800),
        CartItem(cart_id=4, product_id=4, quantity=1, list_price=1500),
        CartItem(cart_id=5, product_id=5, quantity=1, list_price=3000)
    ]
    db.session.add_all(cart_items)
    db.session.commit()

def seed_payments():
    payments = [
        Payment(cart_id=1, user_id=1, mpesa_transaction_id="TRX1234567890", amount=2400, created_at=datetime.utcnow()),
        Payment(cart_id=2, user_id=2, mpesa_transaction_id="TRX1234567891", amount=2500, created_at=datetime.utcnow()),
        Payment(cart_id=3, user_id=3, mpesa_transaction_id="TRX1234567892", amount=1800, created_at=datetime.utcnow()),
        Payment(cart_id=4, user_id=4, mpesa_transaction_id="TRX1234567893", amount=1500, created_at=datetime.utcnow()),
        Payment(cart_id=5, user_id=5, mpesa_transaction_id="TRX1234567894", amount=3000, created_at=datetime.utcnow())
    ]
    db.session.add_all(payments)
    db.session.commit()

def init_db():
    app = create_app()
    with app.app_context():
        create_migrations()
        apply_migrations()

        db.create_all()
        print("Database tables created.")

        seed_catalogs()
        seed_products()
        seed_users()
        seed_reviews()
        seed_wishlist()
        seed_cart()
        seed_cart_items()
        seed_payments()
        print("Database seeded successfully!")

if __name__ == "__main__":
    init_db()
