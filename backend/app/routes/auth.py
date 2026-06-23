from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from app import mongo
from app.middleware.auth import get_current_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    existing_user = mongo.db.users.find_one({'email': data['email']})
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    
    # Hash password
    data['password'] = generate_password_hash(data['password'])
    
    # Create user
    result = mongo.db.users.insert_one({
        'email': data['email'],
        'password': data['password'],
        'name': data['name'],
        'role': data['role'],
        'student_id': data.get('student_id'),
        'parent_id': data.get('parent_id'),
        'department': data.get('department'),
        'class': data.get('class'),
        'created_at': None
    })
    
    return jsonify({'message': 'User created successfully', 'user_id': str(result.inserted_id)}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Find user
    user = mongo.db.users.find_one({'email': data['email']})
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Check password
    if not check_password_hash(user['password'], data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create tokens
    access_token = create_access_token(identity=str(user['_id']))
    refresh_token = create_refresh_token(identity=str(user['_id']))
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {
            'id': str(user['_id']),
            'email': user['email'],
            'name': user['name'],
            'role': user['role'],
            'department': user.get('department'),
            'class': user.get('class')
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user_info():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user['_id'] = str(user['_id'])
    return jsonify(user), 200

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
    try:
        verify_jwt_in_request(refresh=True)
        current_user_id = get_jwt_identity()
        access_token = create_access_token(identity=current_user_id)
        return jsonify({'access_token': access_token}), 200
    except:
        return jsonify({'error': 'Invalid refresh token'}), 401
