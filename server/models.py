from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reviews = db.relationship('Review', backref='user', cascade="all, delete-orphan")
    cart_items = db.relationship('Cart', backref='user', cascade="all, delete-orphan")
    payments = db.relationship('Payment', backref='user', cascade="all, delete-orphan")

    serialize_only = ('id', 'name', 'email', 'created_at')

    def __repr__(self):
        return f'<User {self.id}, {self.name}, {self.email}, {self.created_at}>'
    

class Catalog(db.Model, SerializerMixin):
    __tablename__ = 'catalog'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    products = db.relationship('Product', backref='catalog', cascade="all, delete-orphan")

    serialize_only = ('id', 'name')

    def __repr__(self):
        return f'<Catalog {self.id}, {self.name}>'
    

class Product(db.Model, SerializerMixin):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=True)
    
    reviews = db.relationship('Review', backref='product', cascade="all, delete-orphan")
    wishlist_items = db.relationship('Wishlist', backref='product', cascade="all, delete-orphan")
    cart_items = db.relationship('CartItems', backref='product', cascade="all, delete-orphan")

    serialize_only = ('id', 'name', 'price', 'image', 'quantity', 'catalog_id')
    exclude = ('reviews', 'wishlist_items', 'cart_items')

    def __repr__(self):
        return f'<Product {self.id}, {self.name}, {self.price}, {self.image}, {self.quantity}, {self.catalog_id}>'
    

class Review(db.Model, SerializerMixin):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_only = ('id', 'product_id', 'user_id', 'created_at')

    def __repr__(self):
        return f'<Review {self.id}, Product ID: {self.product_id}, User ID: {self.user_id}, {self.created_at}>'
    

class Wishlist(db.Model, SerializerMixin):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    serialize_only = ('id', 'product_id')

    def __repr__(self):
        return f'<Wishlist {self.id}, Product ID: {self.product_id}>'
    

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    
    serialize_only = ('id', 'user_id', 'product_id')

    def __repr__(self):
        return f'<Cart {self.id}, User ID: {self.user_id}, Product ID: {self.product_id}>'
    

class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payment'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mpesa = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    serialize_only = ('id', 'cart_id', 'user_id', 'mpesa', 'created_at')

    def __repr__(self):
        return f'<Payment {self.id}, Cart ID: {self.cart_id}, User ID: {self.user_id}, MPESA: {self.mpesa}, Created At: {self.created_at}>'
    

class CartItems(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    products_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    list_price = db.Column(db.Integer, nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)

    serialize_only = ('id', 'products_id', 'quantity', 'list_price', 'cart_id')

    def __repr__(self):
        return f'<CartItems {self.id}, Product ID: {self.products_id}, Quantity: {self.quantity}, List Price: {self.list_price}, Cart ID: {self.cart_id}>'
