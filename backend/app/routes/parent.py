from flask import Blueprint, jsonify
from app import mongo
from app.middleware.auth import token_required, role_required, get_current_user
from app.models import FacultyLog, StudentFeedback, ParentMapping

parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/child-progress', methods=['GET'])
@token_required
@role_required('Parent')
def get_child_progress():
    user = get_current_user()
    
    # Find child mapping
    mapping = ParentMapping.find_by_parent(user['_id'])
    if not mapping:
        return jsonify({'error': 'No child found'}), 404
    
    child_id = mapping[0]['student_id']
    
    # Get child's syllabus progress
    progress = list(mongo.db.faculty_logs.find({
        'class': mapping[0].get('class'),
        'department': mapping[0].get('department')
    }))
    
    for item in progress:
        item['_id'] = str(item['_id'])
    
    return jsonify(progress), 200

@parent_bp.route('/child-confidence', methods=['GET'])
@token_required
@role_required('Parent')
def get_child_confidence():
    user = get_current_user()
    
    # Find child mapping
    mapping = ParentMapping.find_by_parent(user['_id'])
    if not mapping:
        return jsonify({'error': 'No child found'}), 404
    
    child_id = mapping[0]['student_id']
    
    # Get child's feedback
    feedback = StudentFeedback.find_by_student(child_id)
    
    for item in feedback:
        item['_id'] = str(item['_id'])
    
    # Calculate confidence stats
    confidence_levels = [f['confidence_level'] for f in feedback]
    high_confidence = confidence_levels.count('High')
    medium_confidence = confidence_levels.count('Medium')
    low_confidence = confidence_levels.count('Low')
    
    return jsonify({
        'feedback': feedback,
        'confidence_stats': {
            'high': high_confidence,
            'medium': medium_confidence,
            'low': low_confidence
        }
    }), 200

@parent_bp.route('/child-remarks', methods=['GET'])
@token_required
@role_required('Parent')
def get_child_remarks():
    user = get_current_user()
    
    # Find child mapping
    mapping = ParentMapping.find_by_parent(user['_id'])
    if not mapping:
        return jsonify({'error': 'No child found'}), 404
    
    child_id = mapping[0]['student_id']
    
    # Get faculty remarks from logs
    remarks = list(mongo.db.faculty_logs.find({
        'class': mapping[0].get('class'),
        'department': mapping[0].get('department')
    }, {'remarks': 1, 'subject': 1, 'topic': 1, 'faculty_name': 1}))
    
    for item in remarks:
        item['_id'] = str(item['_id'])
    
    return jsonify(remarks), 200

@parent_bp.route('/revision-suggestions', methods=['GET'])
@token_required
@role_required('Parent')
def get_revision_suggestions():
    user = get_current_user()
    
    # Find child mapping
    mapping = ParentMapping.find_by_parent(user['_id'])
    if not mapping:
        return jsonify({'error': 'No child found'}), 404
    
    child_id = mapping[0]['student_id']
    
    # Get low confidence topics
    weak_topics = list(mongo.db.student_feedback.find({
        'student_id': child_id,
        'confidence_level': 'Low'
    }))
    
    for item in weak_topics:
        item['_id'] = str(item['_id'])
    
    return jsonify(weak_topics), 200

@parent_bp.route('/dashboard', methods=['GET'])
@token_required
@role_required('Parent')
def parent_dashboard():
    user = get_current_user()
    
    # Find child mapping
    mapping = ParentMapping.find_by_parent(user['_id'])
    if not mapping:
        return jsonify({'error': 'No child found'}), 404
    
    child_id = mapping[0]['student_id']
    child_info = mongo.db.users.find_one({'_id': child_id}, {'password': 0})
    
    # Get syllabus progress
    progress = list(mongo.db.faculty_logs.find({
        'class': mapping[0].get('class'),
        'department': mapping[0].get('department')
    }))
    
    # Get confidence levels
    feedback = StudentFeedback.find_by_student(child_id)
    confidence_levels = [f['confidence_level'] for f in feedback]
    
    # Calculate learning health
    avg_completion = sum(p.get('completion_percentage', 0) for p in progress) / len(progress) if progress else 0
    high_confidence = confidence_levels.count('High')
    total_feedback = len(feedback)
    confidence_ratio = (high_confidence / total_feedback * 100) if total_feedback > 0 else 0
    
    # Determine learning health
    if avg_completion > 70 and confidence_ratio > 60:
        health_status = 'Excellent'
    elif avg_completion > 50 and confidence_ratio > 40:
        health_status = 'Good'
    elif avg_completion > 30 and confidence_ratio > 20:
        health_status = 'Needs Improvement'
    else:
        health_status = 'Critical'
    
    return jsonify({
        'child_info': child_info,
        'syllabus_progress': progress[:10],
        'confidence_levels': {
            'high': confidence_levels.count('High'),
            'medium': confidence_levels.count('Medium'),
            'low': confidence_levels.count('Low')
        },
        'learning_health': {
            'status': health_status,
            'completion_percentage': round(avg_completion, 2),
            'confidence_ratio': round(confidence_ratio, 2)
        },
        'faculty_remarks': [p for p in progress if p.get('remarks')][:5]
    }), 200
