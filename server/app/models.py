from app import db, ma
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200), nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=True)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    description = db.Column(db.Text)

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    products = db.relationship('Product', backref='catalog', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    list_price = db.Column(db.Integer, nullable=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mpesa_transaction_id = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Schemas
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class CatalogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Catalog

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review

class WishlistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist

class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
