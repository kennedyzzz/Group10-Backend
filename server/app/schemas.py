from server.app import ma
from server.app.models import Product, Catalog, User, Review, Wishlist, Cart, CartItem, Payment
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
