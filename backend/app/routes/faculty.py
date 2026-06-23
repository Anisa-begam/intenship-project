from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app import mongo
from app.middleware.auth import token_required, role_required, get_current_user
from app.models import FacultyLog, StudentFeedback

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/logs', methods=['POST'])
@token_required
@role_required('Faculty')
def create_log():
    user = get_current_user()
    data = request.get_json()
    
    data['faculty_id'] = user['_id']
    data['faculty_name'] = user['name']
    
    result = FacultyLog.create_log(data)
    
    return jsonify({
        'message': 'Log created successfully',
        'log_id': str(result.inserted_id)
    }), 201

@faculty_bp.route('/logs', methods=['GET'])
@token_required
@role_required('Faculty')
def get_logs():
    user = get_current_user()
    logs = FacultyLog.find_by_faculty(user['_id'])
    
    for log in logs:
        log['_id'] = str(log['_id'])
    
    return jsonify(logs), 200

@faculty_bp.route('/logs/<log_id>', methods=['PUT'])
@token_required
@role_required('Faculty')
def update_log(log_id):
    user = get_current_user()
    data = request.get_json()
    
    # Verify ownership
    log = mongo.db.faculty_logs.find_one({'_id': ObjectId(log_id)})
    if not log or log['faculty_id'] != user['_id']:
        return jsonify({'error': 'Log not found or unauthorized'}), 404
    
    result = FacultyLog.update_log(ObjectId(log_id), data)
    
    return jsonify({'message': 'Log updated successfully'}), 200

@faculty_bp.route('/logs/<log_id>', methods=['DELETE'])
@token_required
@role_required('Faculty')
def delete_log(log_id):
    user = get_current_user()
    
    # Verify ownership
    log = mongo.db.faculty_logs.find_one({'_id': ObjectId(log_id)})
    if not log or log['faculty_id'] != user['_id']:
        return jsonify({'error': 'Log not found or unauthorized'}), 404
    
    FacultyLog.delete_log(ObjectId(log_id))
    
    return jsonify({'message': 'Log deleted successfully'}), 200

@faculty_bp.route('/feedback', methods=['GET'])
@token_required
@role_required('Faculty')
def get_student_feedback():
    user = get_current_user()
    
    # Get feedback for subjects taught by this faculty
    feedback = list(mongo.db.student_feedback.find({
        'department': user.get('department')
    }))
    
    for item in feedback:
        item['_id'] = str(item['_id'])
    
    return jsonify(feedback), 200

@faculty_bp.route('/analytics/weak-topics', methods=['GET'])
@token_required
@role_required('Faculty')
def get_weak_topics():
    user = get_current_user()
    
    weak_topics = list(mongo.db.student_feedback.aggregate([
        {'$match': {
            'confidence_level': 'Low',
            'department': user.get('department')
        }},
        {'$group': {
            '_id': {'subject': '$subject', 'topic': '$topic'},
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]))
    
    return jsonify(weak_topics), 200

@faculty_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('Faculty')
def faculty_dashboard():
    user = get_current_user()
    
    # Get faculty's logs
    logs = FacultyLog.find_by_faculty(user['_id'])
    
    # Calculate stats
    total_logs = len(logs)
    avg_completion = sum(log.get('completion_percentage', 0) for log in logs) / total_logs if total_logs > 0 else 0
    
    # Get feedback for faculty's department
    feedback = list(mongo.db.student_feedback.find({
        'department': user.get('department')
    }))
    
    # Weak topics
    weak_topics = StudentFeedback.get_weak_topics()
    
    return jsonify({
        'total_logs': total_logs,
        'avg_completion': round(avg_completion, 2),
        'recent_logs': logs[:5],
        'feedback_count': len(feedback),
        'weak_topics': weak_topics[:5]
    }), 200
