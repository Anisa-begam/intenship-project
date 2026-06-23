from flask import Blueprint, request, jsonify
from bson.objectid import ObjectId
from app import mongo
from app.middleware.auth import token_required, role_required, get_current_user
from app.models import FacultyLog, StudentFeedback

student_bp = Blueprint('student', __name__)

@student_bp.route('/feedback', methods=['POST'])
@token_required
@role_required('Student')
def submit_feedback():
    user = get_current_user()
    data = request.get_json()
    
    data['student_id'] = user['_id']
    data['student_name'] = user['name']
    data['department'] = user.get('department')
    data['class'] = user.get('class')
    
    result = StudentFeedback.create_feedback(data)
    
    return jsonify({
        'message': 'Feedback submitted successfully',
        'feedback_id': str(result.inserted_id)
    }), 201

@student_bp.route('/feedback', methods=['GET'])
@token_required
@role_required('Student')
def get_my_feedback():
    user = get_current_user()
    feedback = StudentFeedback.find_by_student(user['_id'])
    
    for item in feedback:
        item['_id'] = str(item['_id'])
    
    return jsonify(feedback), 200

@student_bp.route('/feedback/<feedback_id>', methods=['DELETE'])
@token_required
@role_required('Student')
def delete_feedback(feedback_id):
    user = get_current_user()
    
    # Verify ownership
    feedback = mongo.db.student_feedback.find_one({'_id': ObjectId(feedback_id)})
    if not feedback or feedback['student_id'] != user['_id']:
        return jsonify({'error': 'Feedback not found or unauthorized'}), 404
    
    mongo.db.student_feedback.delete_one({'_id': ObjectId(feedback_id)})
    
    return jsonify({'message': 'Feedback deleted successfully'}), 200

@student_bp.route('/revision', methods=['POST'])
@token_required
@role_required('Student')
def request_revision():
    user = get_current_user()
    data = request.get_json()
    
    data['student_id'] = user['_id']
    data['student_name'] = user['name']
    data['type'] = 'revision_request'
    data['status'] = 'pending'
    data['created_at'] = None
    
    result = mongo.db.revision_requests.insert_one(data)
    
    return jsonify({
        'message': 'Revision request submitted successfully',
        'request_id': str(result.inserted_id)
    }), 201

@student_bp.route('/syllabus-progress', methods=['GET'])
@token_required
@role_required('Student')
def get_syllabus_progress():
    user = get_current_user()
    
    # Get syllabus progress for student's class
    progress = list(mongo.db.faculty_logs.find({
        'class': user.get('class'),
        'department': user.get('department')
    }))
    
    for item in progress:
        item['_id'] = str(item['_id'])
    
    return jsonify(progress), 200

@student_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('Student')
def student_dashboard():
    user = get_current_user()
    
    # Get syllabus progress
    progress = list(mongo.db.faculty_logs.find({
        'class': user.get('class'),
        'department': user.get('department')
    }))
    
    # Get my feedback
    my_feedback = StudentFeedback.find_by_student(user['_id'])
    
    # Calculate confidence stats
    confidence_levels = [f['confidence_level'] for f in my_feedback]
    high_confidence = confidence_levels.count('High')
    medium_confidence = confidence_levels.count('Medium')
    low_confidence = confidence_levels.count('Low')
    
    # Get revision requests
    revision_requests = list(mongo.db.revision_requests.find({
        'student_id': user['_id']
    }))
    
    # Calculate overall completion
    avg_completion = sum(p.get('completion_percentage', 0) for p in progress) / len(progress) if progress else 0
    
    return jsonify({
        'syllabus_progress': progress[:10],
        'my_feedback': my_feedback[:10],
        'confidence_stats': {
            'high': high_confidence,
            'medium': medium_confidence,
            'low': low_confidence
        },
        'revision_requests': revision_requests,
        'overall_completion': round(avg_completion, 2)
    }), 200

@student_bp.route('/improvement-chart', methods=['GET'])
@token_required
@role_required('Student')
def improvement_chart():
    user = get_current_user()
    
    # Get feedback history
    feedback_history = list(mongo.db.student_feedback.find({
        'student_id': user['_id']
    }).sort('created_at', 1))
    
    # Group by subject
    subject_progress = {}
    for feedback in feedback_history:
        subject = feedback['subject']
        if subject not in subject_progress:
            subject_progress[subject] = []
        
        confidence_map = {'Low': 1, 'Medium': 2, 'High': 3}
        subject_progress[subject].append({
            'date': feedback['created_at'],
            'confidence': confidence_map.get(feedback['confidence_level'], 2)
        })
    
    return jsonify(subject_progress), 200
