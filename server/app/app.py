from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zuri_trends.db'
    app.config['UPLOAD_FOLDER'] = 'uploads/'
    app.config['CONSUMER_KEY'] = 'yty83hjgw0EEGrxoV9j3AAQxVJL2hmjcvYMPxsjXH2ghL8AF'
    app.config['CONSUMER_SECRET'] = 'asJhwuTM0XXBWyTJwCWgPWITuucxPoDkNiQWfeTQGgjGraLyl5KO6Ay93sxrSwIm'
    app.config['174379'] = 'your_short_code'
    app.config['bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'] = 'your_shortcode_key'
    app.config['https://mydomain.com/path'] = 'your_callback_url'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    ma.init_app(app)

    class Catalog(db.Model):
        __tablename__ = 'catalog'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        products = db.relationship('Product', backref='catalog', lazy=True)

    class Product(db.Model):
        __tablename__ = 'product'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        price = db.Column(db.Float, nullable=False)
        image_path = db.Column(db.String(200), nullable=True)
        quantity = db.Column(db.Integer, nullable=False)
        catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=False)
        size = db.Column(db.String(10), nullable=True)
        color = db.Column(db.String(20), nullable=True)
        description = db.Column(db.Text, nullable=True)
        reviews = db.relationship('Review', backref='product', lazy=True)
        wishlists = db.relationship('Wishlist', backref='product', lazy=True)
        cart_items = db.relationship('CartItem', backref='product', lazy=True)

    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        password = db.Column(db.String(200), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)
        reviews = db.relationship('Review', backref='user', lazy=True)
        wishlists = db.relationship('Wishlist', backref='user', lazy=True)
        carts = db.relationship('Cart', backref='user', lazy=True)
        payments = db.relationship('Payment', backref='user', lazy=True)

    class Review(db.Model):
        __tablename__ = 'review'
        id = db.Column(db.Integer, primary_key=True)
        product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        rating = db.Column(db.Integer, nullable=False)
        comment = db.Column(db.Text, nullable=True)

    class Wishlist(db.Model):
        __tablename__ = 'wishlist'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    class Cart(db.Model):
        __tablename__ = 'cart'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        items = db.relationship('CartItem', backref='cart', lazy=True)

    class CartItem(db.Model):
        __tablename__ = 'cart_item'
        id = db.Column(db.Integer, primary_key=True)
        cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
        product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
        quantity = db.Column(db.Integer, nullable=False)
        list_price = db.Column(db.Float, nullable=False)

    class Payment(db.Model):
        __tablename__ = 'payment'
        id = db.Column(db.Integer, primary_key=True)
        cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        mpesa_transaction_id = db.Column(db.String(100), nullable=False)
        amount = db.Column(db.Float, nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Routes
    @app.route('/catalogs', methods=['GET'])
    def get_catalogs():
        catalogs = Catalog.query.all()
        return jsonify([{'id': c.id, 'name': c.name} for c in catalogs])

    @app.route('/catalogs/<int:id>', methods=['GET'])
    def get_catalog(id):
        catalog = Catalog.query.get_or_404(id)
        return jsonify({'id': catalog.id, 'name': catalog.name})

    @app.route('/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        return jsonify([{
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'image_path': p.image_path,
            'quantity': p.quantity,
            'catalog_id': p.catalog_id,
            'size': p.size,
            'color': p.color,
            'description': p.description
        } for p in products])

    @app.route('/products/<int:id>', methods=['GET'])
    def get_product(id):
        product = Product.query.get_or_404(id)
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image_path': product.image_path,
            'quantity': product.quantity,
            'catalog_id': product.catalog_id,
            'size': product.size,
            'color': product.color,
            'description': product.description
        })

    @app.route('/users', methods=['GET'])
    def get_users():
        users = User.query.all()
        return jsonify([{
            'id': u.id,
            'name': u.name,
            'email': u.email
        } for u in users])

    @app.route('/users/<int:id>', methods=['GET'])
    def get_user(id):
        user = User.query.get_or_404(id)
        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email
        })

    @app.route('/reviews', methods=['GET'])
    def get_reviews():
        reviews = Review.query.all()
        return jsonify([{
            'id': r.id,
            'product_id': r.product_id,
            'user_id': r.user_id,
            'rating': r.rating,
            'comment': r.comment
        } for r in reviews])

    @app.route('/reviews/<int:id>', methods=['GET'])
    def get_review(id):
        review = Review.query.get_or_404(id)
        return jsonify({
            'id': review.id,
            'product_id': review.product_id,
            'user_id': review.user_id,
            'rating': review.rating,
            'comment': review.comment
        })

    @app.route('/wishlists', methods=['GET'])
    def get_wishlists():
        wishlists = Wishlist.query.all()
        return jsonify([{
            'id': w.id,
            'user_id': w.user_id,
            'product_id': w.product_id
        } for w in wishlists])

    @app.route('/wishlists/<int:id>', methods=['GET'])
    def get_wishlist(id):
        wishlist = Wishlist.query.get_or_404(id)
        return jsonify({
            'id': wishlist.id,
            'user_id': wishlist.user_id,
            'product_id': wishlist.product_id
        })

    @app.route('/carts', methods=['GET'])
    def get_carts():
        carts = Cart.query.all()
        return jsonify([{
            'id': c.id,
            'user_id': c.user_id
        } for c in carts])

    @app.route('/carts/<int:id>', methods=['GET'])
    def get_cart(id):
        cart = Cart.query.get_or_404(id)
        return jsonify({
            'id': cart.id,
            'user_id': cart.user_id
        })

    @app.route('/cart_items', methods=['GET'])
    def get_cart_items():
        cart_items = CartItem.query.all()
        return jsonify([{
            'id': ci.id,
            'cart_id': ci.cart_id,
            'product_id': ci.product_id,
            'quantity': ci.quantity,
            'list_price': ci.list_price
        } for ci in cart_items])

    @app.route('/cart_items/<int:id>', methods=['GET'])
    def get_cart_item(id):
        cart_item = CartItem.query.get_or_404(id)
        return jsonify({
            'id': cart_item.id,
            'cart_id': cart_item.cart_id,
            'product_id': cart_item.product_id,
            'quantity': cart_item.quantity,
            'list_price': cart_item.list_price
        })

    @app.route('/payments', methods=['GET'])
    def get_payments():
        payments = Payment.query.all()
        return jsonify([{
            'id': p.id,
            'cart_id': p.cart_id,
            'user_id': p.user_id,
            'mpesa_transaction_id': p.mpesa_transaction_id,
            'amount': p.amount,
            'created_at': p.created_at
        } for p in payments])

    @app.route('/payments/<int:id>', methods=['GET'])
    def get_payment(id):
        payment = Payment.query.get_or_404(id)
        return jsonify({
            'id': payment.id,
            'cart_id': payment.cart_id,
            'user_id': payment.user_id,
            'mpesa_transaction_id': payment.mpesa_transaction_id,
            'amount': payment.amount,
            'created_at': payment.created_at
        })

    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5555,debug=True)
