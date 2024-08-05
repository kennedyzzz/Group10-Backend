from flask import Flask, request, jsonify
from flask_cors import CORS
from app import db
from app.models import Product, Catalog, User, Review, Wishlist, Cart, CartItem, Payment
from app.schemas import (
    ProductSchema, CatalogSchema, UserSchema, ReviewSchema, WishlistSchema,
    CartSchema, CartItemSchema, PaymentSchema
)
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64

app = Flask(__name__)
CORS(app)

# Configuration for M-Pesa
consumer_key = 'yty83hjgw0EEGrxoV9j3AAQxVJL2hmjcvYMPxsjXH2ghL8AF'
consumer_secret = 'asJhwuTM0XXBWyTJwCWgPWITuucxPoDkNiQWfeTQGgjGraLyl5KO6Ay93sxrSwIm'
shortcode = '174379'
lipa_na_mpesa_online_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
callback_url = 'https://mydomain.com/path'
fixed_phone_number = '0115743312'

def get_access_token():
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()['access_token']

def lipa_na_mpesa_online(amount, phone_number):
    access_token = get_access_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {'Authorization': f'Bearer {access_token}'}

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + lipa_na_mpesa_online_passkey + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode())
    password = encoded_string.decode('utf-8')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for goods"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

# Initialize schemas
product_schema = ProductSchema()
catalog_schema = CatalogSchema()
user_schema = UserSchema()
review_schema = ReviewSchema()
wishlist_schema = WishlistSchema()
cart_schema = CartSchema()
cart_item_schema = CartItemSchema()
payment_schema = PaymentSchema()

# Catalog CRUD
@app.route('/catalogs', methods=['POST'])
def create_catalog():
    data = request.get_json()
    catalog, errors = catalog_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(catalog)
    db.session.commit()
    return catalog_schema.jsonify(catalog), 201

@app.route('/catalogs', methods=['GET'])
def get_catalogs():
    catalogs = Catalog.query.all()
    return catalog_schema.jsonify(catalogs, many=True), 200

@app.route('/catalogs/<int:id>', methods=['GET'])
def get_catalog(id):
    catalog = Catalog.query.get_or_404(id)
    return catalog_schema.jsonify(catalog), 200

@app.route('/catalogs/<int:id>', methods=['PUT'])
def update_catalog(id):
    catalog = Catalog.query.get_or_404(id)
    data = request.get_json()
    updated_catalog, errors = catalog_schema.load(data, instance=catalog)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return catalog_schema.jsonify(updated_catalog), 200

@app.route('/catalogs/<int:id>', methods=['DELETE'])
def delete_catalog(id):
    catalog = Catalog.query.get_or_404(id)
    db.session.delete(catalog)
    db.session.commit()
    return '', 204

# Product CRUD
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product, errors = product_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(product)
    db.session.commit()
    return product_schema.jsonify(product), 201

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return product_schema.jsonify(products, many=True), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    updated_product, errors = product_schema.load(data, instance=product)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return product_schema.jsonify(updated_product), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

# User CRUD
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user, errors = user_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return user_schema.jsonify(users, many=True), 200

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    updated_user, errors = user_schema.load(data, instance=user)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return user_schema.jsonify(updated_user), 200

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Review CRUD
@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    review, errors = review_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(review)
    db.session.commit()
    return review_schema.jsonify(review), 201

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return review_schema.jsonify(reviews, many=True), 200

@app.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get_or_404(id)
    return review_schema.jsonify(review), 200

@app.route('/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    review = Review.query.get_or_404(id)
    data = request.get_json()
    updated_review, errors = review_schema.load(data, instance=review)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return review_schema.jsonify(updated_review), 200

@app.route('/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return '', 204

# Wishlist CRUD
@app.route('/wishlists', methods=['POST'])
def create_wishlist():
    data = request.get_json()
    wishlist, errors = wishlist_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(wishlist)
    db.session.commit()
    return wishlist_schema.jsonify(wishlist), 201

@app.route('/wishlists', methods=['GET'])
def get_wishlists():
    wishlists = Wishlist.query.all()
    return wishlist_schema.jsonify(wishlists, many=True), 200

@app.route('/wishlists/<int:id>', methods=['GET'])
def get_wishlist(id):
    wishlist = Wishlist.query.get_or_404(id)
    return wishlist_schema.jsonify(wishlist), 200

@app.route('/wishlists/<int:id>', methods=['PUT'])
def update_wishlist(id):
    wishlist = Wishlist.query.get_or_404(id)
    data = request.get_json()
    updated_wishlist, errors = wishlist_schema.load(data, instance=wishlist)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return wishlist_schema.jsonify(updated_wishlist), 200

@app.route('/wishlists/<int:id>', methods=['DELETE'])
def delete_wishlist(id):
    wishlist = Wishlist.query.get_or_404(id)
    db.session.delete(wishlist)
    db.session.commit()
    return '', 204

# Cart CRUD
@app.route('/carts', methods=['POST'])
def create_cart():
    data = request.get_json()
    cart, errors = cart_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(cart)
    db.session.commit()
    return cart_schema.jsonify(cart), 201

@app.route('/carts', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    return cart_schema.jsonify(carts, many=True), 200

@app.route('/carts/<int:id>', methods=['GET'])
def get_cart(id):
    cart = Cart.query.get_or_404(id)
    return cart_schema.jsonify(cart), 200

@app.route('/carts/<int:id>', methods=['PUT'])
def update_cart(id):
    cart = Cart.query.get_or_404(id)
    data = request.get_json()
    updated_cart, errors = cart_schema.load(data, instance=cart)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return cart_schema.jsonify(updated_cart), 200

@app.route('/carts/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = Cart.query.get_or_404(id)
    db.session.delete(cart)
    db.session.commit()
    return '', 204

# CartItem CRUD
@app.route('/cart-items', methods=['POST'])
def create_cart_item():
    data = request.get_json()
    cart_item, errors = cart_item_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(cart_item)
    db.session.commit()
    return cart_item_schema.jsonify(cart_item), 201

@app.route('/cart-items', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()
    return cart_item_schema.jsonify(cart_items, many=True), 200

@app.route('/cart-items/<int:id>', methods=['GET'])
def get_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    return cart_item_schema.jsonify(cart_item), 200

@app.route('/cart-items/<int:id>', methods=['PUT'])
def update_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    data = request.get_json()
    updated_cart_item, errors = cart_item_schema.load(data, instance=cart_item)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return cart_item_schema.jsonify(updated_cart_item), 200

@app.route('/cart-items/<int:id>', methods=['DELETE'])
def delete_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return '', 204

# Payment CRUD
@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    payment, errors = payment_schema.load(data)
    if errors:
        return jsonify(errors), 400
    db.session.add(payment)
    db.session.commit()
    return payment_schema.jsonify(payment), 201

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return payment_schema.jsonify(payments, many=True), 200

@app.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get_or_404(id)
    return payment_schema.jsonify(payment), 200

@app.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    payment = Payment.query.get_or_404(id)
    data = request.get_json()
    updated_payment, errors = payment_schema.load(data, instance=payment)
    if errors:
        return jsonify(errors), 400
    db.session.commit()
    return payment_schema.jsonify(updated_payment), 200

@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    return '', 204

# M-Pesa Payment Route
@app.route('/mpesa/payment', methods=['POST'])
def mpesa_payment():
    data = request.get_json()
    amount = data.get('amount')
    phone_number = data.get('phone_number')
    if not amount or not phone_number:
        return jsonify({"error": "Amount and phone number are required"}), 400
    response = lipa_na_mpesa_online(amount, phone_number)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)
