from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.Integer, unique = True, nullable = False)
    password=db.Column(db.String(80), nullable=False)
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

class Admin(db.Model, SerializerMixin):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"<Admin(id={self.id}, username='{self.username}')>"


class Product(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    quantity_available = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.name} from seller {self.seller_id}>'
    
class Service(db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Product {self.name} from seller {self.seller_id}>'