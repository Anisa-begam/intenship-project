import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson.objectid import ObjectId
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['campus_tracker']

def clear_collections():
    """Clear all collections before seeding"""
    db.users.delete_many({})
    db.faculty_logs.delete_many({})
    db.student_feedback.delete_many({})
    db.parent_mapping.delete_many({})
    db.revision_requests.delete_many({})
    print("Collections cleared")

def seed_users():
    """Seed users with different roles"""
    users = [
        {
            'email': 'admin@campus.edu',
            'password': generate_password_hash('admin123'),
            'name': 'Admin User',
            'role': 'Admin',
            'department': 'Administration',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'faculty1@campus.edu',
            'password': generate_password_hash('faculty123'),
            'name': 'Dr. John Smith',
            'role': 'Faculty',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'faculty2@campus.edu',
            'password': generate_password_hash('faculty123'),
            'name': 'Prof. Sarah Johnson',
            'role': 'Faculty',
            'department': 'Computer Science',
            'class': '3rd Year',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'student1@campus.edu',
            'password': generate_password_hash('student123'),
            'name': 'Alice Williams',
            'role': 'Student',
            'student_id': 'STU001',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'student2@campus.edu',
            'password': generate_password_hash('student123'),
            'name': 'Bob Brown',
            'role': 'Student',
            'student_id': 'STU002',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'student3@campus.edu',
            'password': generate_password_hash('student123'),
            'name': 'Charlie Davis',
            'role': 'Student',
            'student_id': 'STU003',
            'department': 'Computer Science',
            'class': '3rd Year',
            'created_at': datetime.utcnow()
        },
        {
            'email': 'parent1@campus.edu',
            'password': generate_password_hash('parent123'),
            'name': 'Mary Williams',
            'role': 'Parent',
            'department': None,
            'class': None,
            'created_at': datetime.utcnow()
        },
        {
            'email': 'parent2@campus.edu',
            'password': generate_password_hash('parent123'),
            'name': 'James Brown',
            'role': 'Parent',
            'department': None,
            'class': None,
            'created_at': datetime.utcnow()
        }
    ]
    
    result = db.users.insert_many(users)
    print(f"Seeded {len(result.inserted_ids)} users")
    return {user['email']: str(id) for user, id in zip(users, result.inserted_ids)}

def seed_parent_mapping(user_ids):
    """Seed parent-student mappings"""
    mappings = [
        {
            'parent_id': user_ids['parent1@campus.edu'],
            'student_id': user_ids['student1@campus.edu'],
            'student_name': 'Alice Williams',
            'department': 'Computer Science',
            'class': '2nd Year'
        },
        {
            'parent_id': user_ids['parent2@campus.edu'],
            'student_id': user_ids['student2@campus.edu'],
            'student_name': 'Bob Brown',
            'department': 'Computer Science',
            'class': '2nd Year'
        }
    ]
    
    result = db.parent_mapping.insert_many(mappings)
    print(f"Seeded {len(result.inserted_ids)} parent mappings")

def seed_faculty_logs(user_ids):
    """Seed faculty progress logs"""
    faculty_id = user_ids['faculty1@campus.edu']
    
    logs = [
        {
            'faculty_id': faculty_id,
            'faculty_name': 'Dr. John Smith',
            'class': '2nd Year',
            'department': 'Computer Science',
            'subject': 'Data Structures',
            'unit': 'Unit 1',
            'topic': 'Arrays and Linked Lists',
            'completion_percentage': 95,
            'remarks': 'Students showed good understanding',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'faculty_id': faculty_id,
            'faculty_name': 'Dr. John Smith',
            'class': '2nd Year',
            'department': 'Computer Science',
            'subject': 'Data Structures',
            'unit': 'Unit 2',
            'topic': 'Stacks and Queues',
            'completion_percentage': 80,
            'remarks': 'Need more practice on queue operations',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'faculty_id': faculty_id,
            'faculty_name': 'Dr. John Smith',
            'class': '2nd Year',
            'department': 'Computer Science',
            'subject': 'Algorithms',
            'unit': 'Unit 1',
            'topic': 'Sorting Algorithms',
            'completion_percentage': 70,
            'remarks': 'Complex topic, needs more time',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'faculty_id': faculty_id,
            'faculty_name': 'Dr. John Smith',
            'class': '2nd Year',
            'department': 'Computer Science',
            'subject': 'Algorithms',
            'unit': 'Unit 2',
            'topic': 'Searching Algorithms',
            'completion_percentage': 85,
            'remarks': 'Good progress on binary search',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'faculty_id': user_ids['faculty2@campus.edu'],
            'faculty_name': 'Prof. Sarah Johnson',
            'class': '3rd Year',
            'department': 'Computer Science',
            'subject': 'Database Systems',
            'unit': 'Unit 1',
            'topic': 'SQL Basics',
            'completion_percentage': 90,
            'remarks': 'Students grasped concepts quickly',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ]
    
    result = db.faculty_logs.insert_many(logs)
    print(f"Seeded {len(result.inserted_ids)} faculty logs")

def seed_student_feedback(user_ids):
    """Seed student feedback"""
    student1_id = user_ids['student1@campus.edu']
    student2_id = user_ids['student2@campus.edu']
    student3_id = user_ids['student3@campus.edu']
    
    feedback = [
        {
            'student_id': student1_id,
            'student_name': 'Alice Williams',
            'subject': 'Data Structures',
            'topic': 'Arrays and Linked Lists',
            'confidence_level': 'High',
            'remarks': 'I understand this topic well',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student1_id,
            'student_name': 'Alice Williams',
            'subject': 'Data Structures',
            'topic': 'Stacks and Queues',
            'confidence_level': 'Medium',
            'remarks': 'Need more practice on queue operations',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student1_id,
            'student_name': 'Alice Williams',
            'subject': 'Algorithms',
            'topic': 'Sorting Algorithms',
            'confidence_level': 'Low',
            'remarks': 'This is very difficult for me',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student2_id,
            'student_name': 'Bob Brown',
            'subject': 'Data Structures',
            'topic': 'Arrays and Linked Lists',
            'confidence_level': 'High',
            'remarks': 'Easy to understand',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student2_id,
            'student_name': 'Bob Brown',
            'subject': 'Data Structures',
            'topic': 'Stacks and Queues',
            'confidence_level': 'Low',
            'remarks': 'Confused about stack operations',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student2_id,
            'student_name': 'Bob Brown',
            'subject': 'Algorithms',
            'topic': 'Sorting Algorithms',
            'confidence_level': 'Medium',
            'remarks': 'Can implement but not fully understand',
            'department': 'Computer Science',
            'class': '2nd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student3_id,
            'student_name': 'Charlie Davis',
            'subject': 'Database Systems',
            'topic': 'SQL Basics',
            'confidence_level': 'High',
            'remarks': 'Very interesting topic',
            'department': 'Computer Science',
            'class': '3rd Year',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': student3_id,
            'student_name': 'Charlie Davis',
            'subject': 'Database Systems',
            'topic': 'Advanced SQL',
            'confidence_level': 'Medium',
            'remarks': 'Joins are tricky',
            'department': 'Computer Science',
            'class': '3rd Year',
            'created_at': datetime.utcnow()
        }
    ]
    
    result = db.student_feedback.insert_many(feedback)
    print(f"Seeded {len(result.inserted_ids)} student feedback entries")

def seed_revision_requests(user_ids):
    """Seed revision requests"""
    requests = [
        {
            'student_id': user_ids['student1@campus.edu'],
            'student_name': 'Alice Williams',
            'subject': 'Algorithms',
            'topic': 'Sorting Algorithms',
            'reason': 'I need help understanding quicksort algorithm',
            'type': 'revision_request',
            'status': 'pending',
            'created_at': datetime.utcnow()
        },
        {
            'student_id': user_ids['student2@campus.edu'],
            'student_name': 'Bob Brown',
            'subject': 'Data Structures',
            'topic': 'Stacks and Queues',
            'reason': 'Please revise stack operations with examples',
            'type': 'revision_request',
            'status': 'approved',
            'created_at': datetime.utcnow()
        }
    ]
    
    result = db.revision_requests.insert_many(requests)
    print(f"Seeded {len(result.inserted_ids)} revision requests")

def main():
    print("Starting database seeding...")
    print("=" * 50)
    
    try:
        clear_collections()
        user_ids = seed_users()
        seed_parent_mapping(user_ids)
        seed_faculty_logs(user_ids)
        seed_student_feedback(user_ids)
        seed_revision_requests(user_ids)
        
        print("=" * 50)
        print("Database seeding completed successfully!")
        print("\nLogin credentials:")
        print("=" * 50)
        print("Admin: admin@campus.edu / admin123")
        print("Faculty: faculty1@campus.edu / faculty123")
        print("Student: student1@campus.edu / student123")
        print("Parent: parent1@campus.edu / parent123")
        print("=" * 50)
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
