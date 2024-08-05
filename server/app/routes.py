from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///zuri_trends.db'
db = SQLAlchemy(app)

class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalog.id'), nullable=False)
    catalog = db.relationship('Catalog', backref=db.backref('products', lazy=True))

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    product = db.relationship('Product', backref=db.backref('reviews', lazy=True))

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product = db.relationship('Product', backref=db.backref('wishlists', lazy=True))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cart = db.relationship('Cart', backref=db.backref('items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

@app.route('/api/catalogs', methods=['POST'])
def create_catalog():
    data = request.json
    catalog = Catalog(name=data['name'])
    db.session.add(catalog)
    db.session.commit()
    return jsonify({'id': catalog.id, 'name': catalog.name}), 201

@app.route('/api/catalogs', methods=['GET'])
def get_catalogs():
    catalogs = Catalog.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in catalogs])

@app.route('/api/catalogs/<int:id>', methods=['GET'])
def get_catalog(id):
    catalog = Catalog.query.get_or_404(id)
    return jsonify({'id': catalog.id, 'name': catalog.name})

@app.route('/api/catalogs/<int:id>', methods=['PUT'])
def update_catalog(id):
    data = request.json
    catalog = Catalog.query.get_or_404(id)
    catalog.name = data['name']
    db.session.commit()
    return jsonify({'id': catalog.id, 'name': catalog.name})

@app.route('/api/catalogs/<int:id>', methods=['DELETE'])
def delete_catalog(id):
    catalog = Catalog.query.get_or_404(id)
    db.session.delete(catalog)
    db.session.commit()
    return '', 204

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(name=data['name'], price=data['price'], catalog_id=data['catalog_id'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price}), 201

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get_or_404(id)
    product.name = data['name']
    product.price = data['price']
    product.catalog_id = data['catalog_id']
    db.session.commit()
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@app.route('/api/reviews', methods=['POST'])
def create_review():
    data = request.json
    review = Review(product_id=data['product_id'], rating=data['rating'], comment=data.get('comment'))
    db.session.add(review)
    db.session.commit()
    return jsonify({'id': review.id, 'rating': review.rating, 'comment': review.comment}), 201

@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([{'id': r.id, 'product_id': r.product_id, 'rating': r.rating, 'comment': r.comment} for r in reviews])

@app.route('/api/reviews/<int:id>', methods=['GET'])
def get_review(id):
    review = Review.query.get_or_404(id)
    return jsonify({'id': review.id, 'product_id': review.product_id, 'rating': review.rating, 'comment': review.comment})

@app.route('/api/reviews/<int:id>', methods=['PUT'])
def update_review(id):
    data = request.json
    review = Review.query.get_or_404(id)
    review.rating = data['rating']
    review.comment = data.get('comment')
    db.session.commit()
    return jsonify({'id': review.id, 'rating': review.rating, 'comment': review.comment})

@app.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return '', 204

@app.route('/api/wishlists', methods=['POST'])
def create_wishlist():
    data = request.json
    wishlist = Wishlist(user_id=data['user_id'], product_id=data['product_id'])
    db.session.add(wishlist)
    db.session.commit()
    return jsonify({'id': wishlist.id, 'user_id': wishlist.user_id, 'product_id': wishlist.product_id}), 201

@app.route('/api/wishlists', methods=['GET'])
def get_wishlists():
    wishlists = Wishlist.query.all()
    return jsonify([{'id': w.id, 'user_id': w.user_id, 'product_id': w.product_id} for w in wishlists])

@app.route('/api/wishlists/<int:id>', methods=['GET'])
def get_wishlist(id):
    wishlist = Wishlist.query.get_or_404(id)
    return jsonify({'id': wishlist.id, 'user_id': wishlist.user_id, 'product_id': wishlist.product_id})

@app.route('/api/wishlists/<int:id>', methods=['PUT'])
def update_wishlist(id):
    data = request.json
    wishlist = Wishlist.query.get_or_404(id)
    wishlist.user_id = data['user_id']
    wishlist.product_id = data['product_id']
    db.session.commit()
    return jsonify({'id': wishlist.id, 'user_id': wishlist.user_id, 'product_id': wishlist.product_id})

@app.route('/api/wishlists/<int:id>', methods=['DELETE'])
def delete_wishlist(id):
    wishlist = Wishlist.query.get_or_404(id)
    db.session.delete(wishlist)
    db.session.commit()
    return '', 204

@app.route('/api/carts', methods=['POST'])
def create_cart():
    data = request.json
    cart = Cart(user_id=data['user_id'])
    db.session.add(cart)
    db.session.commit()
    return jsonify({'id': cart.id, 'user_id': cart.user_id}), 201

@app.route('/api/carts', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    return jsonify([{'id': c.id, 'user_id': c.user_id} for c in carts])

@app.route('/api/carts/<int:id>', methods=['GET'])
def get_cart(id):
    cart = Cart.query.get_or_404(id)
    return jsonify({'id': cart.id, 'user_id': cart.user_id})

@app.route('/api/carts/<int:id>', methods=['PUT'])
def update_cart(id):
    data = request.json
    cart = Cart.query.get_or_404(id)
    cart.user_id = data['user_id']
    db.session.commit()
    return jsonify({'id': cart.id, 'user_id': cart.user_id})

@app.route('/api/carts/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = Cart.query.get_or_404(id)
    db.session.delete(cart)
    db.session.commit()
    return '', 204

@app.route('/api/cart-items', methods=['POST'])
def create_cart_item():
    data = request.json
    cart_item = CartItem(cart_id=data['cart_id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    return jsonify({'id': cart_item.id, 'cart_id': cart_item.cart_id, 'product_id': cart_item.product_id, 'quantity': cart_item.quantity}), 201

@app.route('/api/cart-items', methods=['GET'])
def get_cart_items():
    cart_items = CartItem.query.all()
    return jsonify([{'id': ci.id, 'cart_id': ci.cart_id, 'product_id': ci.product_id, 'quantity': ci.quantity} for ci in cart_items])

@app.route('/api/cart-items/<int:id>', methods=['GET'])
def get_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    return jsonify({'id': cart_item.id, 'cart_id': cart_item.cart_id, 'product_id': cart_item.product_id, 'quantity': cart_item.quantity})

@app.route('/api/cart-items/<int:id>', methods=['PUT'])
def update_cart_item(id):
    data = request.json
    cart_item = CartItem.query.get_or_404(id)
    cart_item.cart_id = data['cart_id']
    cart_item.product_id = data['product_id']
    cart_item.quantity = data['quantity']
    db.session.commit()
    return jsonify({'id': cart_item.id, 'cart_id': cart_item.cart_id, 'product_id': cart_item.product_id, 'quantity': cart_item.quantity})

@app.route('/api/cart-items/<int:id>', methods=['DELETE'])
def delete_cart_item(id):
    cart_item = CartItem.query.get_or_404(id)
    db.session.delete(cart_item)
    db.session.commit()
    return '', 204

@app.route('/api/mpesa-payment', methods=['POST'])
def mpesa_payment():
    data = request.json
    amount = data['amount']
    phone_number = data['phone_number']
    description = data['description']
        
    result = {
        'status': 'success',
        'amount': amount,
        'phone_number': phone_number,
        'description': description
    }
    
    return jsonify(result), 200

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
