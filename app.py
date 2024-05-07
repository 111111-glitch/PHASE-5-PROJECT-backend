from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
from models import db, User,Admin
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, get_jwt
from flask_bcrypt import Bcrypt
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

bcrypt = Bcrypt(app)

app.secret_key = 'secret key'
app.config['JWT_SECRET_KEY'] = 'this-is-secret-key'

jwt = JWTManager(app)

revoked_tokens = set()


# Decorator for admin-only access
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Unauthorized'}), 403
        return fn(*args, **kwargs)
    return wrapper

# User Registration
class UserRegister(Resource):
    @cross_origin()
    def post(self):
        data = request.get_json(force=True)

        username = data.get('username')
        email = data.get('email')
        phone_number = data.get('phone_number')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        user_exists = User.query.filter_by(username=username).first()

        if user_exists:
            return jsonify({'error': 'User already exists'}), 409
        
        if password != confirm_password:
            return jsonify({'Error': 'Passwords not matching'}), 400
        
        hashed_pw = bcrypt.generate_password_hash(password.encode('utf-8'))

        new_user = User(
            username=username,
            email=email, 
            phone_number=phone_number, 
            password=hashed_pw,
            role='user'
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            'phone_number': new_user.phone_number,
        }), 201

api.add_resource(UserRegister, '/userRegister')


# User Login
class UserLogin(Resource):
    @cross_origin()
    def post(self):
        data = request.get_json(force=True)

        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Unauthorized, incorrect password'}), 401
        
        # Generate access token with role included
        access_token = create_access_token(identity={'username': username, 'role': 'user'})

        return jsonify({
            "id": user.id,
            "username": user.username,
            "access_token": access_token
        }), 201

api.add_resource(UserLogin, '/user/login')

# Admin Login
class AdminLogin(Resource):
    @cross_origin()
    def post(self):
        data = request.get_json(force=True)

        username = data.get('username')
        password = data.get('password')

        # Checks if the admin exists in the Admin Table
        admin = Admin.query.filter_by(username=username).first()

        if admin is None:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if not bcrypt.check_password_hash(admin.password, password):
            return jsonify({'error': 'Unauthorized, incorrect password'}), 401
        
        # Generate access token with role included
        access_token = create_access_token(identity={'username': username, 'role': 'admin'})

        return jsonify({
            "id": admin.id,
            "username": admin.username,
            "access_token": access_token
        }), 201

api.add_resource(AdminLogin, '/admin/login')


# User Logout
class UserLogout(Resource):
    @jwt_required()  # Requires a valid access token to access this endpoint
    def post(self):
        try:
            # No need to retrieve raw JWT token, as jwt_required ensures a valid token
            # Revoke the current access token directly
            jti = get_jwt()["jti"]
            revoked_tokens.add(jti)

            return jsonify({'message': 'User Logout successful'}), 200
        except Exception as e:
            print(f"Error occurred during logout: {e}")
            return jsonify({'error': 'An unexpected error occurred'}), 500

api.add_resource(UserLogout, '/userLogout')


# Admin Logout
class AdminLogout(Resource):
    @jwt_required()  # Requires a valid access token to access this endpoint
    def post(self):
        try:
            # Get the raw JWT token (access token)
            jti = get_jwt()["jti"]
            revoked_tokens.add(jti)

            return jsonify({'message': 'Admin logout successful'}), 200
        except Exception as e:
            print(f"Error occurred during admin logout: {e}")
            return jsonify({'error': 'An unexpected error occurred'}), 500

api.add_resource(AdminLogout, '/adminLogout')

@app.route('/users/<int:id>', methods=["GET", "PATCH"])
def get_and_update_user_info_by_id(id):
    session = db.session()
    user = session.get(User,id)

    if request.method == 'GET':
        if not user:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(user.to_dict()), 200
    
    if request.method == 'PATCH':
        data = request.json7

        if not data:
            return jsonify({'error': 'No data provided for update'}), 401
        
        if not user:
            return jsonify({'error': 'Item not found'}), 404
        
        for key, value in data.items():
            setattr(user, key, value)

        try:
            db.session.commit()
            return jsonify(user.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update item: {str(e)}'}), 500
        
@app.route('/admins/<int:id>', methods=["GET", "PATCH"])
def get_and_update_admin_info_by_id(id):
    session = db.session()
    admin = session.get(Admin,id)

    if request.method == 'GET':
        if not admin:
            return jsonify({'error': 'Item not found'}), 404
        return jsonify(admin.to_dict()), 200
    
    if request.method == 'PATCH':
        data = request.json7

        if not data:
            return jsonify({'error': 'No data provided for update'}), 401
        
        if not admin:
            return jsonify({'error': 'Item not found'}), 404
        
        for key, value in data.items():
            setattr(admin, key, value)

        try:
            db.session.commit()
            return jsonify(admin.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to update item: {str(e)}'}), 500
