"""
Admin routes for dashboard and analytics
"""

from flask import Blueprint, render_template, jsonify, request, Response
from flask_login import login_required, current_user
from functools import wraps
import csv
import io
from datetime import datetime
from app import db
from app.models.user import User
from app.models.student import Student
from app.models.faculty import Faculty
from app.models.parent import Parent
from app.models.subject import Subject
from app.models.class_model import Class
from app.models.faculty_log import FacultyLog
from app.models.student_feedback import StudentFeedback
from app.models.parent_student_mapping import ParentStudentMapping
from sqlalchemy import func, and_

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            from flask import flash, redirect, url_for
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with analytics"""
    # Get overall statistics
    total_students = Student.query.count()
    total_faculty = Faculty.query.count()
    total_parents = Parent.query.count()
    total_classes = Class.query.count()
    total_subjects = Subject.query.count()
    
    # Get syllabus completion
    avg_completion = db.session.query(func.avg(FacultyLog.completion_percentage)).scalar() or 0
    
    # Get confidence distribution
    confidence_data = db.session.query(
        FacultyLog.confidence_level,
        func.count(FacultyLog.id)
    ).group_by(FacultyLog.confidence_level).all()
    
    confidence_dict = dict(confidence_data)
    
    # Get subject-wise completion
    subject_completion = db.session.query(
        Subject.name,
        func.avg(FacultyLog.completion_percentage)
    ).join(Subject.logs).group_by(Subject.id).all()
    
    # Get class-wise confidence
    class_confidence = db.session.query(
        Class.name,
        FacultyLog.confidence_level,
        func.count(FacultyLog.id)
    ).join(Class.faculty_logs).group_by(Class.id, FacultyLog.confidence_level).all()
    
    # Get low confidence alerts
    low_confidence_logs = FacultyLog.query.filter_by(confidence_level='Low').order_by(FacultyLog.date.desc()).limit(10).all()
    
    # Get faculty activity
    faculty_activity = db.session.query(
        User.full_name,
        func.count(FacultyLog.id)
    ).join(Faculty, User.id == Faculty.user_id).join(FacultyLog, Faculty.id == FacultyLog.faculty_id).group_by(User.id).all()
    
    # Get revision requests
    revision_requests = StudentFeedback.query.filter_by(need_revision=True).order_by(StudentFeedback.date.desc()).limit(10).all()
    
    # Parent visibility summary
    parent_visibility = db.session.query(
        func.count(ParentStudentMapping.id)
    ).scalar() or 0
    
    return render_template('admin/dashboard.html',
                         total_students=total_students,
                         total_faculty=total_faculty,
                         total_parents=total_parents,
                         total_classes=total_classes,
                         total_subjects=total_subjects,
                         avg_completion=round(avg_completion, 1),
                         confidence_dict=confidence_dict,
                         subject_completion=subject_completion,
                         class_confidence=class_confidence,
                         low_confidence_logs=low_confidence_logs,
                         faculty_activity=faculty_activity,
                         revision_requests=revision_requests,
                         parent_visibility=parent_visibility)

@admin_bp.route('/api/analytics')
@login_required
@admin_required
def analytics_api():
    """API endpoint for chart data"""
    # Subject-wise completion
    subject_data = db.session.query(
        Subject.name,
        func.avg(FacultyLog.completion_percentage)
    ).join(Subject.logs).group_by(Subject.id).all()
    
    # Confidence distribution
    confidence_data = db.session.query(
        FacultyLog.confidence_level,
        func.count(FacultyLog.id)
    ).group_by(FacultyLog.confidence_level).all()
    
    # Class-wise completion
    class_data = db.session.query(
        Class.name,
        func.avg(FacultyLog.completion_percentage)
    ).join(Class.faculty_logs).group_by(Class.id).all()
    
    return jsonify({
        'subject_completion': [{'name': name, 'value': round(value, 1)} for name, value in subject_data],
        'confidence_distribution': [{'level': level, 'count': count} for level, count in confidence_data],
        'class_completion': [{'name': name, 'value': round(value, 1)} for name, value in class_data]
    })

@admin_bp.route('/students')
@login_required
@admin_required
def students():
    """View all students"""
    students = Student.query.join(User, Student.user_id == User.id).join(Class, Student.class_id == Class.id).all()
    return render_template('admin/students.html', students=students)

@admin_bp.route('/faculty')
@login_required
@admin_required
def faculty():
    """View all faculty"""
    faculty_list = Faculty.query.join(User).all()
    return render_template('admin/faculty.html', faculty_list=faculty_list)

@admin_bp.route('/parents')
@login_required
@admin_required
def parents():
    """View all parents"""
    parents_list = Parent.query.join(User).all()
    return render_template('admin/parents.html', parents_list=parents_list)

@admin_bp.route('/classes')
@login_required
@admin_required
def classes():
    """View all classes"""
    classes_list = Class.query.all()
    return render_template('admin/classes.html', classes_list=classes_list)

@admin_bp.route('/subjects')
@login_required
@admin_required
def subjects():
    """View all subjects"""
    subjects_list = Subject.query.join(Class, Subject.class_id == Class.id).all()
    return render_template('admin/subjects.html', subjects_list=subjects_list)

@admin_bp.route('/export/<data_type>')
@login_required
@admin_required
def export_data(data_type):
    """Export data as CSV"""
    output = io.StringIO()
    writer = csv.writer(output)
    
    if data_type == 'students':
        writer.writerow(['ID', 'Name', 'Roll Number', 'Class', 'Email', 'Phone', 'Admission Date'])
        students = Student.query.join(User, Student.user_id == User.id).join(Class, Student.class_id == Class.id).all()
        for student in students:
            writer.writerow([
                student.id,
                student.user.full_name,
                student.roll_number,
                student.class_info.name,
                student.user.email,
                student.phone,
                student.admission_date.strftime('%Y-%m-%d')
            ])
        filename = f'students_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    elif data_type == 'faculty':
        writer.writerow(['ID', 'Name', 'Employee ID', 'Department', 'Qualification', 'Email', 'Phone', 'Joining Date'])
        faculty_list = Faculty.query.join(User).all()
        for faculty in faculty_list:
            writer.writerow([
                faculty.id,
                faculty.user.full_name,
                faculty.employee_id,
                faculty.department,
                faculty.qualification,
                faculty.user.email,
                faculty.phone,
                faculty.joining_date.strftime('%Y-%m-%d')
            ])
        filename = f'faculty_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    elif data_type == 'faculty_logs':
        writer.writerow(['ID', 'Faculty', 'Class', 'Subject', 'Unit', 'Topic', 'Date', 'Completion %', 'Confidence', 'Remarks'])
        logs = FacultyLog.query.join(Faculty, FacultyLog.faculty_id == Faculty.id).join(Subject, FacultyLog.subject_id == Subject.id).join(Class, FacultyLog.class_id == Class.id).all()
        for log in logs:
            writer.writerow([
                log.id,
                log.faculty.user.full_name,
                log.class_obj.name,
                log.subject.name,
                log.unit,
                log.topic,
                log.date.strftime('%Y-%m-%d'),
                log.completion_percentage,
                log.confidence_level,
                log.remarks
            ])
        filename = f'faculty_logs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    elif data_type == 'student_feedback':
        writer.writerow(['ID', 'Student', 'Class', 'Subject', 'Topic', 'Confidence', 'Needs Revision', 'Comment', 'Date'])
        feedback = StudentFeedback.query.join(Student, StudentFeedback.student_id == Student.id).join(Subject, StudentFeedback.subject_id == Subject.id).join(Class, StudentFeedback.class_id == Class.id).all()
        for fb in feedback:
            writer.writerow([
                fb.id,
                fb.student.user.full_name,
                fb.student.class_info.name,
                fb.subject.name,
                fb.topic,
                fb.confidence_level,
                'Yes' if fb.need_revision else 'No',
                fb.comment,
                fb.date.strftime('%Y-%m-%d')
            ])
        filename = f'student_feedback_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    else:
        return jsonify({'error': 'Invalid data type'}), 400
    
    output.seek(0)
    return Response(
        output,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
