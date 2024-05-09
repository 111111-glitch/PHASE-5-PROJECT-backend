from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates, relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from sqlalchemy.orm import relationship

class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError('Password must be more than 8 characters.')
        return password

    def __repr__(self):
        return f"<Admin(id={self.id}, username='{self.username}')>"

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    confirm_password = db.Column(db.String(80), nullable=False)

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 8:
            raise ValueError('Password must be more than 8 characters.')
        return password
    
    @validates('email')
    def validate_email(self, key, email):
        if not email.endswith("@gmail.com"):
            raise ValueError("Email is not valid. It should end with @gmail.com")
        return email

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

class Product(db.Model, SerializerMixin):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)

    # Added seller_id to the Product model to establish a relationship with the Admin model, representing the seller of the product.
    seller_id = db.Column(db.Integer, db.ForeignKey('admins.id')) 

    # Added a relationship attribute seller to the Product model to access the seller of the product.
    seller = relationship("Admin", back_populates="products")

    serialize_rules = ('-seller.products', '-product_order_items.product')

    def __repr__(self):
        return f'<Product {self.name} from seller {self.seller_id}>'

class ProductOrder(db.Model, SerializerMixin):
    __tablename__ = "productorders"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False)

    # Added user_id to the ProductOrder model to establish a relationship with the User model, representing the user who placed the order.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Added a relationship attribute user to the ProductOrder model to access the user who placed the order.
    user = relationship("User", back_populates="orders")

    #Added order_items relationship to the ProductOrder model to represent the items in the order.
    product_order_items = relationship("ProductOrderItem", back_populates="order")

    serialize_rules = ('-user.orders', '-product_order_items.order')

    def __repr__(self):
        return f'<ProductOrder {self.id}>'

class ProductOrderItem(db.Model, SerializerMixin):
    __tablename__ = "productorderitems"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    product_order_id = db.Column(db.Integer, db.ForeignKey('productorders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    #Added product_order and product relationships to the ProductOrderItem model to represent the order and product associated with each item, respectively.
    product_order = relationship("ProductOrder", back_populates="product_order_items")
    product = relationship("Product", back_populates="product_order_items")

    serialize_rules = ('-product_order.product_order_items', '-product.product_order_items')


    def __repr__(self):
        return f'<OrderItem {self.id}>'

    
class Service(db.Model, SerializerMixin):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    # Added seller_id to the Service model to establish a relationship with the Admin model, representing the seller of the service.
    seller_id = db.Column(db.Integer, db.ForeignKey('admins.id'))

    # Added a relationship attribute seller to the Service model to access the seller of the service.
    seller = relationship("Admin", back_populates="services")

    serialize_rules = ('-seller.services', '-service_order_items.service')

    def __repr__(self):
        return f'<Product {self.name} from seller {self.seller_id}>'
    

class ServiceOrder(db.Model, SerializerMixin):
    __tablename__ = "serviceorders"

    id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, nullable=False) 

    # Added user_id to the ServiceOrder model to establish a relationship with the User model, representing the user who placed the order.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Added a relationship attribute user to the ServiceOrder model to access the user who placed the order.
    user = relationship("User", back_populates="orders")

    #Added order_items relationship to the ServiceOrder model to represent the items in the order.
    service_order_items = relationship("ServiceOrderItem", back_populates="order")

    serialize_rules = ('-user.orders', '-service_order_items.order')

    def __repr__(self):
        return f'<ServiceOrder {self.id}>'
    
class ServiceOrderItem(db.Model, SerializerMixin):
    __tablename__ = "serviceorderitems"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    service_order_id = db.Column(db.Integer, db.ForeignKey('serviceorders.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)

    #Added service_order and service relationships to the ServiceOrderItem model to represent the order and service associated with each item, respectively.
    service_order = relationship("ServiceOrder", back_populates="service_order_items")
    service = relationship("Service", back_populates="service_order_items")

    # Serialization rules to avoid recursion
    serialize_rules = ('-service_order.service_order_items', '-service.service_order_items')

    def __repr__(self):
        return f'< {self.id}>'
