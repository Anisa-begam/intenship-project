"""
Faculty routes for dashboard and syllabus logging
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.faculty import Faculty
from app.models.class_model import Class
from app.models.subject import Subject
from app.models.faculty_log import FacultyLog
from app.models.student_feedback import StudentFeedback
from datetime import datetime
from sqlalchemy import func

faculty_bp = Blueprint('faculty', __name__)

def faculty_required(f):
    """Decorator to require faculty access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_faculty():
            flash('Access denied. Faculty privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@faculty_bp.route('/dashboard')
@login_required
@faculty_required
def dashboard():
    """Faculty dashboard"""
    faculty = Faculty.query.filter_by(user_id=current_user.id).first()
    
    if not faculty:
        flash('Faculty profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get faculty's recent logs
    recent_logs = FacultyLog.query.filter_by(faculty_id=faculty.id)\
        .order_by(FacultyLog.date.desc()).limit(10).all()
    
    # Get classes and subjects
    classes = Class.query.all()
    subjects = Subject.query.all()
    
    # Get student feedback for faculty's subjects
    feedbacks = StudentFeedback.query.join(Subject)\
        .filter(Subject.id.in_([s.id for s in subjects]))\
        .order_by(StudentFeedback.date.desc()).limit(10).all()
    
    # Get statistics
    total_logs = FacultyLog.query.filter_by(faculty_id=faculty.id).count()
    avg_completion = db.session.query(func.avg(FacultyLog.completion_percentage))\
        .filter_by(faculty_id=faculty.id).scalar() or 0
    
    return render_template('faculty/dashboard.html',
                         faculty=faculty,
                         recent_logs=recent_logs,
                         classes=classes,
                         subjects=subjects,
                         feedbacks=feedbacks,
                         total_logs=total_logs,
                         avg_completion=round(avg_completion, 1))

@faculty_bp.route('/add-log', methods=['GET', 'POST'])
@login_required
@faculty_required
def add_log():
    """Add daily syllabus log"""
    faculty = Faculty.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        subject_id = request.form.get('subject_id')
        unit = request.form.get('unit')
        topic = request.form.get('topic')
        date = request.form.get('date')
        completion_percentage = request.form.get('completion_percentage')
        confidence_level = request.form.get('confidence_level')
        remarks = request.form.get('remarks')
        
        # Validation
        if not all([class_id, subject_id, unit, topic, date, completion_percentage, confidence_level]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('faculty.add_log'))
        
        try:
            completion_percentage = int(completion_percentage)
            if completion_percentage < 0 or completion_percentage > 100:
                flash('Completion percentage must be between 0 and 100.', 'danger')
                return redirect(url_for('faculty.add_log'))
        except ValueError:
            flash('Invalid completion percentage.', 'danger')
            return redirect(url_for('faculty.add_log'))
        
        # Create new log
        log = FacultyLog(
            faculty_id=faculty.id,
            class_id=class_id,
            subject_id=subject_id,
            unit=unit,
            topic=topic,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            completion_percentage=completion_percentage,
            confidence_level=confidence_level,
            remarks=remarks
        )
        
        db.session.add(log)
        db.session.commit()
        
        flash('Syllabus log added successfully!', 'success')
        return redirect(url_for('faculty.dashboard'))
    
    classes = Class.query.all()
    subjects = Subject.query.all()
    
    return render_template('faculty/add_log.html', classes=classes, subjects=subjects)

@faculty_bp.route('/logs')
@login_required
@faculty_required
def logs():
    """View all faculty logs"""
    faculty = Faculty.query.filter_by(user_id=current_user.id).first()
    logs = FacultyLog.query.filter_by(faculty_id=faculty.id)\
        .order_by(FacultyLog.date.desc()).all()
    
    return render_template('faculty/logs.html', logs=logs)

@faculty_bp.route('/feedback')
@login_required
@faculty_required
def feedback():
    """View student feedback"""
    faculty = Faculty.query.filter_by(user_id=current_user.id).first()
    
    # Get feedback for subjects taught by this faculty
    subjects = Subject.query.all()
    subject_ids = [s.id for s in subjects]
    
    feedbacks = StudentFeedback.query.filter(StudentFeedback.subject_id.in_(subject_ids))\
        .order_by(StudentFeedback.date.desc()).all()
    
    return render_template('faculty/feedback.html', feedbacks=feedbacks)

@faculty_bp.route('/profile')
@login_required
@faculty_required
def profile():
    """View faculty profile"""
    faculty = Faculty.query.filter_by(user_id=current_user.id).first()
    return render_template('faculty/profile.html', faculty=faculty)
