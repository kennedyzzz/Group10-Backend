from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from models import db, User, Catalog, Product, Review, Wishlist, Cart, Payment, CartItems

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Zuri Trends.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
api = Api(app)

# User Resource
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            return [user.to_dict() for user in users], 200
        else:
            user = User.query.get(user_id)
            if user:
                return user.to_dict(), 200
            return {'error': 'User not found'}, 404

    def post(self):
        data = request.json
        new_user = User(name=data['name'], password=data['password'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return new_user.to_dict(), 201

# Catalog Resource
class CatalogResource(Resource):
    def get(self, catalog_id=None):
        if catalog_id is None:
            catalogs = Catalog.query.all()
            return [catalog.to_dict() for catalog in catalogs], 200
        else:
            catalog = Catalog.query.get(catalog_id)
            if catalog:
                return catalog.to_dict(), 200
            return {'error': 'Catalog not found'}, 404

    def post(self):
        data = request.json
        new_catalog = Catalog(name=data['name'])
        db.session.add(new_catalog)
        db.session.commit()
        return new_catalog.to_dict(), 201


# Product Resource
class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id is None:
            products = Product.query.all()
            return [product.to_dict() for product in products], 200
        else:
            product = Product.query.get(product_id)
            if product:
                return product.to_dict(), 200
            return {'error': 'Product not found'}, 404

    def post(self):
        data = request.json
        new_product = Product(
            name=data['name'],
            price=data['price'],
            image=data['image'],
            quantity=data['quantity'],
            catalog_id=data.get('catalog_id')
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product.to_dict(), 201

# Review Resource
class ReviewResource(Resource):
    def get(self, review_id=None):
        if review_id is None:
            reviews = Review.query.all()
            return [review.to_dict() for review in reviews], 200
        else:
            review = Review.query.get(review_id)
            if review:
                return review.to_dict(), 200
            return {'error': 'Review not found'}, 404

    def post(self):
        data = request.json
        new_review = Review(
            product_id=data['product_id'],
            user_id=data['user_id']
        )
        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict(), 201


# Wishlist Resource
class WishlistResource(Resource):
    def get(self, wishlist_id=None):
        if wishlist_id is None:
            wishlists = Wishlist.query.all()
            return [wishlist.to_dict() for wishlist in wishlists], 200
        else:
            wishlist = Wishlist.query.get(wishlist_id)
            if wishlist:
                return wishlist.to_dict(), 200
            return {'error': 'Wishlist not found'}, 404

    def post(self):
        data = request.json
        new_wishlist = Wishlist(product_id=data['product_id'])
        db.session.add(new_wishlist)
        db.session.commit()
        return new_wishlist.to_dict(), 201

# Cart Resource
class CartResource(Resource):
    def get(self, cart_id=None):
        if cart_id is None:
            carts = Cart.query.all()
            return [cart.to_dict() for cart in carts], 200
        else:
            cart = Cart.query.get(cart_id)
            if cart:
                return cart.to_dict(), 200
            return {'error': 'Cart not found'}, 404

    def post(self):
        data = request.json
        new_cart = Cart(user_id=data['user_id'], product_id=data['product_id'])
        db.session.add(new_cart)
        db.session.commit()
        return new_cart.to_dict(), 201

    def delete(self, cart_id):
        cart = Cart.query.get(cart_id)
        if not cart:
            return {'error': 'Cart not found'}, 404

        db.session.delete(cart)
        db.session.commit()
        return {'message': 'Cart deleted'}, 204

# Payment Resource
class PaymentResource(Resource):
    def get(self, payment_id=None):
        if payment_id is None:
            payments = Payment.query.all()
            return [payment.to_dict() for payment in payments], 200
        else:
            payment = Payment.query.get(payment_id)
            if payment:
                return payment.to_dict(), 200
            return {'error': 'Payment not found'}, 404

    def post(self):
        data = request.json
        new_payment = Payment(
            cart_id=data['cart_id'],
            user_id=data['user_id'],
            mpesa_transaction_id=data.get('mpesa')
        )
        db.session.add(new_payment)
        db.session.commit()
        return new_payment.to_dict(), 201

    def delete(self, payment_id):
        payment = Payment.query.get(payment_id)
        if not payment:
            return {'error': 'Payment not found'}, 404

        db.session.delete(payment)
        db.session.commit()
        return {'message': 'Payment deleted'}, 204

# CartItems Resource
class CartItemsResource(Resource):
    def get(self, cart_item_id=None):
        if cart_item_id is None:
            cart_items = CartItems.query.all()
            return [cart_item.to_dict() for cart_item in cart_items], 200
        else:
            cart_item = CartItems.query.get(cart_item_id)
            if cart_item:
                return cart_item.to_dict(), 200
            return {'error': 'Cart Item not found'}, 404

    def post(self):
        data = request.json
        new_cart_item = CartItems(
            products_id=data['products_id'],
            quantity=data['quantity'],
            list_price=data['list_price'],
            cart_id=data['cart_id']
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return new_cart_item.to_dict(), 201


api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(CatalogResource, '/catalogs', '/catalogs/<int:catalog_id>')
api.add_resource(ProductResource, '/products', '/products/<int:product_id>')
api.add_resource(ReviewResource, '/reviews', '/reviews/<int:review_id>')
api.add_resource(WishlistResource, '/wishlists', '/wishlists/<int:wishlist_id>')
api.add_resource(CartResource, '/carts', '/carts/<int:cart_id>')
api.add_resource(PaymentResource, '/payments', '/payments/<int:payment_id>')
api.add_resource(CartItemsResource, '/cart_items', '/cart_items/<int:cart_item_id>')

if __name__ == '__main__':
    app.run(debug=True)
