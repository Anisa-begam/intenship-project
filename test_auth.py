"""
Test script to verify authentication
"""

from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    # Check if users exist
    users = User.query.all()
    print(f"Total users in database: {len(users)}")
    
    for user in users:
        print(f"\nUsername: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Full Name: {user.full_name}")
        print(f"Is Active: {user.is_active}")
        print(f"Password Hash: {user.password_hash[:50]}...")
        
        # Test password verification
        test_passwords = {
            'admin': 'admin123',
            'faculty': 'faculty123',
            'student': 'student123',
            'parent': 'parent123'
        }
        
        if user.username in test_passwords:
            test_password = test_passwords[user.username]
            is_valid = user.check_password(test_password)
            print(f"Password '{test_password}' valid: {is_valid}")
