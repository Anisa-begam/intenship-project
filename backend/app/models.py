from datetime import datetime
from flask_pymongo import PyMongo
from app import mongo

class User:
    @staticmethod
    def create_user(data):
        return mongo.db.users.insert_one(data)
    
    @staticmethod
    def find_by_email(email):
        return mongo.db.users.find_one({'email': email})
    
    @staticmethod
    def find_by_id(user_id):
        return mongo.db.users.find_one({'_id': user_id})
    
    @staticmethod
    def find_all():
        return list(mongo.db.users.find({}, {'password': 0}))
    
    @staticmethod
    def update_user(user_id, data):
        return mongo.db.users.update_one({'_id': user_id}, {'$set': data})
    
    @staticmethod
    def delete_user(user_id):
        return mongo.db.users.delete_one({'_id': user_id})

class FacultyLog:
    @staticmethod
    def create_log(data):
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        return mongo.db.faculty_logs.insert_one(data)
    
    @staticmethod
    def find_by_faculty(faculty_id):
        return list(mongo.db.faculty_logs.find({'faculty_id': faculty_id}))
    
    @staticmethod
    def find_by_class(class_name):
        return list(mongo.db.faculty_logs.find({'class': class_name}))
    
    @staticmethod
    def find_all():
        return list(mongo.db.faculty_logs.find())
    
    @staticmethod
    def update_log(log_id, data):
        data['updated_at'] = datetime.utcnow()
        return mongo.db.faculty_logs.update_one({'_id': log_id}, {'$set': data})
    
    @staticmethod
    def delete_log(log_id):
        return mongo.db.faculty_logs.delete_one({'_id': log_id})
    
    @staticmethod
    def get_completion_stats():
        pipeline = [
            {'$group': {
                '_id': '$subject',
                'avg_completion': {'$avg': '$completion_percentage'},
                'total_units': {'$sum': 1}
            }}
        ]
        return list(mongo.db.faculty_logs.aggregate(pipeline))

class StudentFeedback:
    @staticmethod
    def create_feedback(data):
        data['created_at'] = datetime.utcnow()
        return mongo.db.student_feedback.insert_one(data)
    
    @staticmethod
    def find_by_student(student_id):
        return list(mongo.db.student_feedback.find({'student_id': student_id}))
    
    @staticmethod
    def find_by_subject(subject):
        return list(mongo.db.student_feedback.find({'subject': subject}))
    
    @staticmethod
    def find_all():
        return list(mongo.db.student_feedback.find())
    
    @staticmethod
    def get_confidence_stats():
        pipeline = [
            {'$group': {
                '_id': '$confidence_level',
                'count': {'$sum': 1}
            }}
        ]
        return list(mongo.db.student_feedback.aggregate(pipeline))
    
    @staticmethod
    def get_weak_topics():
        pipeline = [
            {'$match': {'confidence_level': 'Low'}},
            {'$group': {
                '_id': {'subject': '$subject', 'topic': '$topic'},
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}},
            {'$limit': 10}
        ]
        return list(mongo.db.student_feedback.aggregate(pipeline))

class ParentMapping:
    @staticmethod
    def create_mapping(data):
        return mongo.db.parent_mapping.insert_one(data)
    
    @staticmethod
    def find_by_parent(parent_id):
        return list(mongo.db.parent_mapping.find({'parent_id': parent_id}))
    
    @staticmethod
    def find_by_student(student_id):
        return mongo.db.parent_mapping.find_one({'student_id': student_id})
    
    @staticmethod
    def find_all():
        return list(mongo.db.parent_mapping.find())
