from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app import mongo

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': 'Token is invalid or missing'}), 401
    return decorated_function

def role_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                user = mongo.db.users.find_one({'_id': current_user_id})
                
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                
                if user['role'] not in allowed_roles:
                    return jsonify({'error': 'Insufficient permissions'}), 403
                
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({'error': str(e)}), 401
        return decorated_function
    return decorator

def get_current_user():
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        return mongo.db.users.find_one({'_id': current_user_id}, {'password': 0})
    except:
        return None
