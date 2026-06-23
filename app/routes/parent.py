"""
Parent routes for dashboard and child data viewing
"""

from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User
from app.models.parent import Parent
from app.models.student import Student
from app.models.parent_student_mapping import ParentStudentMapping
from app.models.class_model import Class
from app.models.subject import Subject
from app.models.faculty_log import FacultyLog
from app.models.student_feedback import StudentFeedback
from sqlalchemy import func

parent_bp = Blueprint('parent', __name__)

def parent_required(f):
    """Decorator to require parent access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_parent():
            flash('Access denied. Parent privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@parent_bp.route('/dashboard')
@login_required
@parent_required
def dashboard():
    """Parent dashboard showing child's data"""
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    
    if not parent:
        flash('Parent profile not found. Please contact administrator.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Get children for this parent
    mappings = ParentStudentMapping.query.filter_by(parent_id=parent.id)\
        .filter_by(is_primary=True).all()
    
    if not mappings:
        flash('No children linked to your account. Please contact administrator.', 'warning')
        return render_template('parent/dashboard.html', children=None)
    
    # Get primary child (first one for simplicity)
    primary_mapping = mappings[0]
    student = Student.query.get(primary_mapping.student_id)
    
    if not student:
        flash('Student data not found. Please contact administrator.', 'danger')
        return render_template('parent/dashboard.html', children=None)
    
    # Get class information
    class_info = Class.query.get(student.class_id)
    
    # Get subjects for student's class
    subjects = Subject.query.filter_by(class_id=student.class_id).all()
    
    # Get syllabus progress
    progress_data = db.session.query(
        Subject.name,
        func.avg(FacultyLog.completion_percentage)
    ).join(FacultyLog).filter(FacultyLog.class_id == student.class_id)\
        .group_by(Subject.id).all()
    
    # Get student's confidence levels
    confidence_data = db.session.query(
        Subject.name,
        StudentFeedback.confidence_level,
        func.count(StudentFeedback.id)
    ).join(StudentFeedback).filter(StudentFeedback.student_id == student.id)\
        .group_by(Subject.id, StudentFeedback.confidence_level).all()
    
    # Get faculty remarks
    faculty_logs = FacultyLog.query.filter_by(class_id=student.class_id)\
        .order_by(FacultyLog.date.desc()).limit(10).all()
    
    # Get revision recommendations
    revision_requests = StudentFeedback.query.filter_by(student_id=student.id, need_revision=True)\
        .order_by(StudentFeedback.date.desc()).limit(10).all()
    
    # Calculate overall learning health
    overall_progress = 0
    if progress_data:
        overall_progress = sum([p[1] for p in progress_data if p[1]]) / len(progress_data)
    
    # Calculate confidence score
    high_confidence = sum([c[2] for c in confidence_data if c[1] == 'High'])
    medium_confidence = sum([c[2] for c in confidence_data if c[1] == 'Medium'])
    low_confidence = sum([c[2] for c in confidence_data if c[1] == 'Low'])
    total_feedback = high_confidence + medium_confidence + low_confidence
    
    confidence_score = 0
    if total_feedback > 0:
        confidence_score = ((high_confidence * 3) + (medium_confidence * 2) + (low_confidence * 1)) / (total_feedback * 3)
    
    return render_template('parent/dashboard.html',
                         student=student,
                         class_info=class_info,
                         subjects=subjects,
                         progress_data=progress_data,
                         confidence_data=confidence_data,
                         faculty_logs=faculty_logs,
                         revision_requests=revision_requests,
                         overall_progress=round(overall_progress, 1),
                         confidence_score=round(confidence_score * 100, 1),
                         high_confidence=high_confidence,
                         medium_confidence=medium_confidence,
                         low_confidence=low_confidence)

@parent_bp.route('/child/<int:student_id>')
@login_required
@parent_required
def child_details(student_id):
    """View detailed information for a specific child"""
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    
    # Verify this child belongs to the parent
    mapping = ParentStudentMapping.query.filter_by(parent_id=parent.id, student_id=student_id).first()
    
    if not mapping:
        flash('Access denied. This child is not linked to your account.', 'danger')
        return redirect(url_for('parent.dashboard'))
    
    student = Student.query.get(student_id)
    class_info = Class.query.get(student.class_id)
    
    # Get detailed progress
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
    
    # Get student feedback
    feedbacks = StudentFeedback.query.filter_by(student_id=student.id)\
        .order_by(StudentFeedback.date.desc()).all()
    
    return render_template('parent/child_details.html',
                         student=student,
                         class_info=class_info,
                         progress_details=progress_details,
                         feedbacks=feedbacks)

@parent_bp.route('/profile')
@login_required
@parent_required
def profile():
    """View parent profile"""
    parent = Parent.query.filter_by(user_id=current_user.id).first()
    
    # Get children
    mappings = ParentStudentMapping.query.filter_by(parent_id=parent.id).all()
    children = []
    for mapping in mappings:
        student = Student.query.get(mapping.student_id)
        if student:
            class_info = Class.query.get(student.class_id)
            children.append({
                'student': student,
                'class_info': class_info,
                'relationship': mapping.relationship,
                'is_primary': mapping.is_primary
            })
    
    return render_template('parent/profile.html', parent=parent, children=children)
