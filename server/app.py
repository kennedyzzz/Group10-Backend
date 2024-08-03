from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import User, Catalog, Product, Review, Wishlist, Cart, Payment, CartItems

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Zuri Trends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class UserResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'email': fields.String,
        'created_at': fields.DateTime
    }
    
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
    parser.add_argument('password', type=str, required=True, help="Password cannot be blank!")
    parser.add_argument('email', type=str, required=True, help="Email cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_user = User(name=args['name'], password=args['password'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201
    
    @marshal_with(resource_fields)
    def put(self, user_id):
        args = self.parser.parse_args()
        user = User.query.get_or_404(user_id)
        user.name = args['name']
        user.password = args['password']
        user.email = args['email']
        db.session.commit()
        return user
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

class CatalogResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, catalog_id):
        catalog = Catalog.query.get_or_404(catalog_id)
        return catalog
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_catalog = Catalog(name=args['name'])
        db.session.add(new_catalog)
        db.session.commit()
        return new_catalog, 201
    
    @marshal_with(resource_fields)
    def put(self, catalog_id):
        args = self.parser.parse_args()
        catalog = Catalog.query.get_or_404(catalog_id)
        catalog.name = args['name']
        db.session.commit()
        return catalog
    
    def delete(self, catalog_id):
        catalog = Catalog.query.get_or_404(catalog_id)
        db.session.delete(catalog)
        db.session.commit()
        return '', 204

class ProductResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'price': fields.Integer,
        'image': fields.String,
        'quantity': fields.Integer,
        'catalog_id': fields.Integer,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
    parser.add_argument('price', type=int, required=True, help="Price cannot be blank!")
    parser.add_argument('image', type=str, required=True, help="Image cannot be blank!")
    parser.add_argument('quantity', type=int, required=True, help="Quantity cannot be blank!")
    parser.add_argument('catalog_id', type=int, required=True, help="Catalog ID cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, product_id):
        product = Product.query.get_or_404(product_id)
        return product
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_product = Product(name=args['name'], price=args['price'], image=args['image'], quantity=args['quantity'], catalog_id=args['catalog_id'])
        db.session.add(new_product)
        db.session.commit()
        return new_product, 201
    
    @marshal_with(resource_fields)
    def put(self, product_id):
        args = self.parser.parse_args()
        product = Product.query.get_or_404(product_id)
        product.name = args['name']
        product.price = args['price']
        product.image = args['image']
        product.quantity = args['quantity']
        product.catalog_id = args['catalog_id']
        db.session.commit()
        return product
    
    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204

class ReviewResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'product_id': fields.Integer,
        'user_id': fields.Integer,
        'created_at': fields.DateTime
    }

    parser = reqparse.RequestParser()
    parser.add_argument('product_id', type=int, required=True, help="Product ID cannot be blank!")
    parser.add_argument('user_id', type=int, required=True, help="User ID cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, review_id):
        review = Review.query.get_or_404(review_id)
        return review
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_review = Review(product_id=args['product_id'], user_id=args['user_id'])
        db.session.add(new_review)
        db.session.commit()
        return new_review, 201
    
    @marshal_with(resource_fields)
    def put(self, review_id):
        args = self.parser.parse_args()
        review = Review.query.get_or_404(review_id)
        review.product_id = args['product_id']
        review.user_id = args['user_id']
        db.session.commit()
        return review
    
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return '', 204

class WishlistResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'product_id': fields.Integer,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('product_id', type=int, required=True, help="Product ID cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, wishlist_id):
        wishlist = Wishlist.query.get_or_404(wishlist_id)
        return wishlist
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_wishlist = Wishlist(product_id=args['product_id'])
        db.session.add(new_wishlist)
        db.session.commit()
        return new_wishlist, 201
    
    @marshal_with(resource_fields)
    def put(self, wishlist_id):
        args = self.parser.parse_args()
        wishlist = Wishlist.query.get_or_404(wishlist_id)
        wishlist.product_id = args['product_id']
        db.session.commit()
        return wishlist
    
    def delete(self, wishlist_id):
        wishlist = Wishlist.query.get_or_404(wishlist_id)
        db.session.delete(wishlist)
        db.session.commit()
        return '', 204

class CartResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'product_id': fields.Integer,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('user_id', type=int, required=True, help="User ID cannot be blank!")
    parser.add_argument('product_id', type=int, required=True, help="Product ID cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, cart_id):
        cart = Cart.query.get_or_404(cart_id)
        return cart
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_cart = Cart(user_id=args['user_id'], product_id=args['product_id'])
        db.session.add(new_cart)
        db.session.commit()
        return new_cart, 201
    
    @marshal_with(resource_fields)
    def put(self, cart_id):
        args = self.parser.parse_args()
        cart = Cart.query.get_or_404(cart_id)
        cart.user_id = args['user_id']
        cart.product_id = args['product_id']
        db.session.commit()
        return cart
    
    def delete(self, cart_id):
        cart = Cart.query.get_or_404(cart_id)
        db.session.delete(cart)
        db.session.commit()
        return '', 204

class PaymentResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'cart_id': fields.Integer,
        'user_id': fields.Integer,
        'mpesa': fields.String,
        'created_at': fields.DateTime,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('cart_id', type=int, required=True, help="Cart ID cannot be blank!")
    parser.add_argument('user_id', type=int, required=True, help="User ID cannot be blank!")
    parser.add_argument('mpesa', type=str)
    
    @marshal_with(resource_fields)
    def get(self, payment_id):
        payment = Payment.query.get_or_404(payment_id)
        return payment
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_payment = Payment(cart_id=args['cart_id'], user_id=args['user_id'], mpesa=args['mpesa'])
        db.session.add(new_payment)
        db.session.commit()
        return new_payment, 201
    
    @marshal_with(resource_fields)
    def put(self, payment_id):
        args = self.parser.parse_args()
        payment = Payment.query.get_or_404(payment_id)
        payment.cart_id = args['cart_id']
        payment.user_id = args['user_id']
        payment.mpesa = args['mpesa']
        db.session.commit()
        return payment
    
    def delete(self, payment_id):
        payment = Payment.query.get_or_404(payment_id)
        db.session.delete(payment)
        db.session.commit()
        return '', 204

class CartItemsResource(Resource):
    resource_fields = {
        'id': fields.Integer,
        'products_id': fields.Integer,
        'quantity': fields.Integer,
        'list_price': fields.Integer,
        'cart_id': fields.Integer,
    }

    parser = reqparse.RequestParser()
    parser.add_argument('products_id', type=int, required=True, help="Product ID cannot be blank!")
    parser.add_argument('quantity', type=int, required=True, help="Quantity cannot be blank!")
    parser.add_argument('list_price', type=int, required=True, help="List Price cannot be blank!")
    parser.add_argument('cart_id', type=int, required=True, help="Cart ID cannot be blank!")
    
    @marshal_with(resource_fields)
    def get(self, cart_item_id):
        cart_item = CartItems.query.get_or_404(cart_item_id)
        return cart_item
    
    @marshal_with(resource_fields)
    def post(self):
        args = self.parser.parse_args()
        new_cart_item = CartItems(products_id=args['products_id'], quantity=args['quantity'], list_price=args['list_price'], cart_id=args['cart_id'])
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item, 201
    
    @marshal_with(resource_fields)
    def put(self, cart_item_id):
        args = self.parser.parse_args()
        cart_item = CartItems.query.get_or_404(cart_item_id)
        cart_item.products_id = args['products_id']
        cart_item.quantity = args['quantity']
        cart_item.list_price = args['list_price']
        cart_item.cart_id = args['cart_id']
        db.session.commit()
        return cart_item
    
    def delete(self, cart_item_id):
        cart_item = CartItems.query.get_or_404(cart_item_id)
        db.session.delete(cart_item)
        db.session.commit()
        return '', 204
