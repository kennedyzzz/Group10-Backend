from flask import request, jsonify
from app import app, db
from app.models import Product, Catalog, User, Review, Wishlist, Cart, CartItem, Payment, ProductSchema, CatalogSchema, UserSchema, ReviewSchema, WishlistSchema, CartSchema, CartItemSchema, PaymentSchema

# Initialize schemas
product_schema = ProductSchema()
catalog_schema = CatalogSchema()
user_schema = UserSchema()
review_schema = ReviewSchema()
wishlist_schema = WishlistSchema()
cart_schema = CartSchema()
cart_item_schema = CartItemSchema()
payment_schema = PaymentSchema()

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

# M-Pesa integration
@app.route('/payments/mpesa', methods=['POST'])
def mpesa_payment():
    data = request.json
    amount = data['amount']
    phone_number = data['phone_number']
    response = lipa_na_mpesa_online(amount, phone_number)
    return jsonify(response)

@app.route('/callback', methods=['POST'])
def mpesa_callback():
    mpesa_response = request.get_json()
    print(mpesa_response)
    return {"ResultCode": 0, "ResultDesc": "Accepted"}, 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
