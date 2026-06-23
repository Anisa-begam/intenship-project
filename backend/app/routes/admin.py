from flask import Blueprint, jsonify
from app import mongo
from app.middleware.auth import token_required, role_required
from app.models import FacultyLog, StudentFeedback

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('Admin')
def admin_dashboard():
    # Overall syllabus completion
    completion_stats = FacultyLog.get_completion_stats()
    
    # Student confidence analytics
    confidence_stats = StudentFeedback.get_confidence_stats()
    
    # Total counts
    total_students = mongo.db.users.count_documents({'role': 'Student'})
    total_faculty = mongo.db.users.count_documents({'role': 'Faculty'})
    total_parents = mongo.db.users.count_documents({'role': 'Parent'})
    
    # Faculty update status
    faculty_updates = list(mongo.db.faculty_logs.aggregate([
        {'$group': {
            '_id': '$faculty_id',
            'last_update': {'$max': '$updated_at'},
            'update_count': {'$sum': 1}
        }},
        {'$lookup': {
            'from': 'users',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'faculty'
        }},
        {'$unwind': '$faculty'},
        {'$project': {
            'faculty_name': '$faculty.name',
            'last_update': '$last_update',
            'update_count': '$update_count'
        }}
    ]))
    
    # Low confidence alerts
    low_confidence = list(mongo.db.student_feedback.find(
        {'confidence_level': 'Low'}
    ))
    
    # Subject-wise performance
    subject_performance = list(mongo.db.faculty_logs.aggregate([
        {'$group': {
            '_id': '$subject',
            'avg_completion': {'$avg': '$completion_percentage'},
            'total_topics': {'$sum': 1}
        }}
    ]))
    
    # Class-wise performance
    class_performance = list(mongo.db.faculty_logs.aggregate([
        {'$group': {
            '_id': '$class',
            'avg_completion': {'$avg': '$completion_percentage'},
            'total_topics': {'$sum': 1}
        }}
    ]))
    
    return jsonify({
        'completion_stats': completion_stats,
        'confidence_stats': confidence_stats,
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_parents': total_parents,
        'faculty_updates': faculty_updates,
        'low_confidence_alerts': len(low_confidence),
        'subject_performance': subject_performance,
        'class_performance': class_performance
    }), 200

@admin_bp.route('/users', methods=['GET'])
@token_required
@role_required('Admin')
def get_all_users():
    users = list(mongo.db.users.find({}, {'password': 0}))
    for user in users:
        user['_id'] = str(user['_id'])
    return jsonify(users), 200

@admin_bp.route('/analytics/confidence', methods=['GET'])
@token_required
@role_required('Admin')
def confidence_analytics():
    confidence_data = StudentFeedback.get_confidence_stats()
    weak_topics = StudentFeedback.get_weak_topics()
    
    return jsonify({
        'confidence_distribution': confidence_data,
        'weak_topics': weak_topics
    }), 200

@admin_bp.route('/analytics/completion', methods=['GET'])
@token_required
@role_required('Admin')
def completion_analytics():
    completion_stats = FacultyLog.get_completion_stats()
    return jsonify(completion_stats), 200

@admin_bp.route('/faculty/status', methods=['GET'])
@token_required
@role_required('Admin')
def faculty_status():
    faculty_status = list(mongo.db.users.find({'role': 'Faculty'}, {'password': 0}))
    for faculty in faculty_status:
        faculty['_id'] = str(faculty['_id'])
        # Get recent updates
        recent_updates = list(mongo.db.faculty_logs.find(
            {'faculty_id': faculty['_id']}
        ).sort('updated_at', -1).limit(5))
        faculty['recent_updates'] = len(recent_updates)
    
    return jsonify(faculty_status), 200
