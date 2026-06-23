"""
Student routes for dashboard and feedback submission
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.class_model import Class
from app.models.subject import Subject
from app.models.faculty_log import FacultyLog
from app.models.student_feedback import StudentFeedback
from datetime import datetime
from sqlalchemy import func

student_bp = Blueprint('student', __name__)

def student_required(f):
    """Decorator to require student access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_student():
            flash('Access denied. Student privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """Student dashboard"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if not student:
        flash('Student profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get class information
    class_info = Class.query.get(student.class_id)
    
    # Get subjects for student's class
    subjects = Subject.query.filter_by(class_id=student.class_id).all()
    
    # Get syllabus progress for student's class
    progress_data = db.session.query(
        Subject.name,
        func.avg(FacultyLog.completion_percentage)
    ).join(FacultyLog).filter(FacultyLog.class_id == student.class_id)\
        .group_by(Subject.id).all()
    
    # Get student's feedback history
    feedback_history = StudentFeedback.query.filter_by(student_id=student.id)\
        .order_by(StudentFeedback.date.desc()).limit(10).all()
    
    # Get faculty remarks for student's class
    faculty_logs = FacultyLog.query.filter_by(class_id=student.class_id)\
        .order_by(FacultyLog.date.desc()).limit(10).all()
    
    # Calculate overall progress
    overall_progress = 0
    if progress_data:
        overall_progress = sum([p[1] for p in progress_data if p[1]]) / len(progress_data)
    
    return render_template('student/dashboard.html',
                         student=student,
                         class_info=class_info,
                         subjects=subjects,
                         progress_data=progress_data,
                         feedback_history=feedback_history,
                         faculty_logs=faculty_logs,
                         overall_progress=round(overall_progress, 1))

@student_bp.route('/add-feedback', methods=['GET', 'POST'])
@login_required
@student_required
def add_feedback():
    """Add student feedback"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        topic = request.form.get('topic')
        confidence_level = request.form.get('confidence_level')
        need_revision = request.form.get('need_revision') == 'on'
        comment = request.form.get('comment')
        
        # Validation
        if not all([subject_id, topic, confidence_level]):
            flash('Please fill in all required fields.', 'danger')
            return redirect(url_for('student.add_feedback'))
        
        # Create new feedback
        feedback = StudentFeedback(
            student_id=student.id,
            class_id=student.class_id,
            subject_id=subject_id,
            topic=topic,
            confidence_level=confidence_level,
            need_revision=need_revision,
            comment=comment,
            date=datetime.utcnow().date()
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('student.dashboard'))
    
    subjects = Subject.query.filter_by(class_id=student.class_id).all()
    
    return render_template('student/add_feedback.html', subjects=subjects)

@student_bp.route('/progress')
@login_required
@student_required
def progress():
    """View detailed syllabus progress"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    
    # Get detailed progress by subject
    progress_details = db.session.query(
        Subject.name,
        FacultyLog.unit,
        FacultyLog.topic,
        FacultyLog.completion_percentage,
        FacultyLog.confidence_level,
        FacultyLog.date,
        FacultyLog.remarks
    ).join(FacultyLog).filter(FacultyLog.class_id == student.class_id)\
        .order_by(Subject.name, FacultyLog.date.desc()).all()
    
    return render_template('student/progress.html', progress_details=progress_details)

@student_bp.route('/feedback-history')
@login_required
@student_required
def feedback_history():
    """View feedback history"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    feedbacks = StudentFeedback.query.filter_by(student_id=student.id)\
        .order_by(StudentFeedback.date.desc()).all()
    
    return render_template('student/feedback_history.html', feedbacks=feedbacks)

@student_bp.route('/profile')
@login_required
@student_required
def profile():
    """View student profile"""
    student = Student.query.filter_by(user_id=current_user.id).first()
    class_info = Class.query.get(student.class_id)
    
    return render_template('student/profile.html', student=student, class_info=class_info)
