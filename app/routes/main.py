"""
Main routes for home page and public access
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        # Redirect to appropriate dashboard
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_faculty():
            return redirect(url_for('faculty.dashboard'))
        elif current_user.is_student():
            return redirect(url_for('student.dashboard'))
        elif current_user.is_parent():
            return redirect(url_for('parent.dashboard'))
    
    return render_template('index.html')

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')
