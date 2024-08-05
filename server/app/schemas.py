from flask_marshmallow import Marshmallow
from app import ma
from app.models import Product, Catalog, User, Review, Wishlist, Cart, CartItem, Payment

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        include_fk = True

class CatalogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Catalog
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ReviewSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        include_fk = True

class WishlistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Wishlist
        include_fk = True

class CartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Cart
        include_fk = True

class CartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CartItem
        include_fk = True

class PaymentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Payment
        include_fk = True

ma = Marshmallow()
