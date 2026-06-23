"""
Authentication routes for login, logout, and session management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if current_user.is_authenticated:
        # Redirect to appropriate dashboard based on role
        return redirect_to_dashboard()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Debug logging
        print(f"Login attempt - Username: {username}, Password: {'*' * len(password) if password else 'None'}")
        
        user = User.query.filter_by(username=username).first()
        
        print(f"User found: {user is not None}")
        if user:
            print(f"User role: {user.role}, is_active: {user.is_active}")
            print(f"Password check result: {user.check_password(password) if password else False}")
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact administrator.', 'danger')
                return render_template('auth/login.html')
            
            login_user(user, remember=remember)
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Update session with role
            session['role'] = user.role
            
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect_to_dashboard()
        else:
            flash('Invalid username or password.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    session.clear()
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))

def redirect_to_dashboard():
    """Redirect user to appropriate dashboard based on role"""
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_faculty():
        return redirect(url_for('faculty.dashboard'))
    elif current_user.is_student():
        return redirect(url_for('student.dashboard'))
    elif current_user.is_parent():
        return redirect(url_for('parent.dashboard'))
    else:
        return redirect(url_for('main.index'))
