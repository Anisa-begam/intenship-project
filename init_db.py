"""
Database initialization script for Campus Progress Tracker
Creates tables and inserts sample data for testing
"""

from app import create_app, db
from app.models.user import User
from app.models.student import Student
from app.models.parent import Parent
from app.models.faculty import Faculty
from app.models.class_model import Class
from app.models.subject import Subject
from app.models.faculty_log import FacultyLog
from app.models.student_feedback import StudentFeedback
from app.models.parent_student_mapping import ParentStudentMapping
from datetime import datetime, date

def init_database():
    """Initialize database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Drop all tables and recreate
        db.drop_all()
        db.create_all()
        
        print("Creating sample data...")
        
        # Create Classes
        class1 = Class(name='10th Grade - A', grade='10th', section='A', academic_year='2024-2025')
        class2 = Class(name='10th Grade - B', grade='10th', section='B', academic_year='2024-2025')
        class3 = Class(name='11th Grade - A', grade='11th', section='A', academic_year='2024-2025')
        db.session.add_all([class1, class2, class3])
        db.session.commit()
        
        # Create Admin User
        admin_user = User(
            username='admin',
            email='admin@campus.edu',
            full_name='System Administrator',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        
        # Create Faculty Users
        faculty1_user = User(
            username='faculty',
            email='faculty1@campus.edu',
            full_name='Dr. John Smith',
            role='faculty'
        )
        faculty1_user.set_password('faculty123')
        db.session.add(faculty1_user)
        db.session.commit()
        
        faculty2_user = User(
            username='faculty2',
            email='faculty2@campus.edu',
            full_name='Prof. Sarah Johnson',
            role='faculty'
        )
        faculty2_user.set_password('faculty123')
        db.session.add(faculty2_user)
        db.session.commit()
        
        # Create Faculty Profiles
        faculty1 = Faculty(
            user_id=faculty1_user.id,
            employee_id='FAC001',
            department='Mathematics',
            qualification='Ph.D. Mathematics',
            phone='555-0101',
            joining_date=date(2020, 1, 15)
        )
        faculty2 = Faculty(
            user_id=faculty2_user.id,
            employee_id='FAC002',
            department='Science',
            qualification='M.Sc. Physics',
            phone='555-0102',
            joining_date=date(2021, 6, 1)
        )
        db.session.add_all([faculty1, faculty2])
        db.session.commit()
        
        # Set class teachers
        class1.class_teacher_id = faculty1.id
        class2.class_teacher_id = faculty2.id
        db.session.commit()
        
        # Create Student Users
        student1_user = User(
            username='student',
            email='student1@campus.edu',
            full_name='Alice Williams',
            role='student'
        )
        student1_user.set_password('student123')
        db.session.add(student1_user)
        db.session.commit()
        
        student2_user = User(
            username='student2',
            email='student2@campus.edu',
            full_name='Bob Brown',
            role='student'
        )
        student2_user.set_password('student123')
        db.session.add(student2_user)
        db.session.commit()
        
        student3_user = User(
            username='student3',
            email='student3@campus.edu',
            full_name='Charlie Davis',
            role='student'
        )
        student3_user.set_password('student123')
        db.session.add(student3_user)
        db.session.commit()
        
        # Create Student Profiles
        student1 = Student(
            user_id=student1_user.id,
            roll_number='2024-001',
            class_id=class1.id,
            date_of_birth=date(2008, 5, 15),
            admission_date=date(2024, 4, 1),
            phone='555-0201',
            address='123 Main St, City'
        )
        student2 = Student(
            user_id=student2_user.id,
            roll_number='2024-002',
            class_id=class1.id,
            date_of_birth=date(2008, 8, 20),
            admission_date=date(2024, 4, 1),
            phone='555-0202',
            address='456 Oak Ave, City'
        )
        student3 = Student(
            user_id=student3_user.id,
            roll_number='2024-003',
            class_id=class2.id,
            date_of_birth=date(2008, 3, 10),
            admission_date=date(2024, 4, 1),
            phone='555-0203',
            address='789 Pine Rd, City'
        )
        db.session.add_all([student1, student2, student3])
        db.session.commit()
        
        # Create Parent Users
        parent1_user = User(
            username='parent',
            email='parent1@campus.edu',
            full_name='Michael Williams',
            role='parent'
        )
        parent1_user.set_password('parent123')
        db.session.add(parent1_user)
        db.session.commit()
        
        parent2_user = User(
            username='parent2',
            email='parent2@campus.edu',
            full_name='Jennifer Brown',
            role='parent'
        )
        parent2_user.set_password('parent123')
        db.session.add(parent2_user)
        db.session.commit()
        
        # Create Parent Profiles
        parent1 = Parent(
            user_id=parent1_user.id,
            phone='555-0301',
            occupation='Engineer'
        )
        parent2 = Parent(
            user_id=parent2_user.id,
            phone='555-0302',
            occupation='Doctor'
        )
        db.session.add_all([parent1, parent2])
        db.session.commit()
        
        # Create Parent-Student Mappings
        mapping1 = ParentStudentMapping(
            parent_id=parent1.id,
            student_id=student1.id,
            relationship='Father',
            is_primary=True
        )
        mapping2 = ParentStudentMapping(
            parent_id=parent2.id,
            student_id=student2.id,
            relationship='Mother',
            is_primary=True
        )
        db.session.add_all([mapping1, mapping2])
        db.session.commit()
        
        # Create Subjects
        subject1 = Subject(
            name='Mathematics',
            code='MATH101',
            class_id=class1.id,
            total_units=5,
            description='Advanced Mathematics for 10th Grade'
        )
        subject2 = Subject(
            name='Physics',
            code='PHY101',
            class_id=class1.id,
            total_units=4,
            description='Physics for 10th Grade'
        )
        subject3 = Subject(
            name='Chemistry',
            code='CHEM101',
            class_id=class1.id,
            total_units=4,
            description='Chemistry for 10th Grade'
        )
        subject4 = Subject(
            name='English',
            code='ENG101',
            class_id=class1.id,
            total_units=3,
            description='English Language and Literature'
        )
        subject5 = Subject(
            name='Mathematics',
            code='MATH102',
            class_id=class2.id,
            total_units=5,
            description='Advanced Mathematics for 10th Grade B'
        )
        db.session.add_all([subject1, subject2, subject3, subject4, subject5])
        db.session.commit()
        
        # Create Faculty Logs
        log1 = FacultyLog(
            faculty_id=faculty1.id,
            class_id=class1.id,
            subject_id=subject1.id,
            unit='Unit 1',
            topic='Algebra - Linear Equations',
            date=date(2024, 6, 1),
            completion_percentage=85,
            confidence_level='High',
            remarks='Students showed good understanding'
        )
        log2 = FacultyLog(
            faculty_id=faculty1.id,
            class_id=class1.id,
            subject_id=subject1.id,
            unit='Unit 2',
            topic='Quadratic Equations',
            date=date(2024, 6, 5),
            completion_percentage=70,
            confidence_level='Medium',
            remarks='Some students need additional practice'
        )
        log3 = FacultyLog(
            faculty_id=faculty2.id,
            class_id=class1.id,
            subject_id=subject2.id,
            unit='Unit 1',
            topic='Motion and Forces',
            date=date(2024, 6, 2),
            completion_percentage=90,
            confidence_level='High',
            remarks='Excellent class participation'
        )
        log4 = FacultyLog(
            faculty_id=faculty2.id,
            class_id=class1.id,
            subject_id=subject2.id,
            unit='Unit 2',
            topic='Energy and Work',
            date=date(2024, 6, 6),
            completion_percentage=60,
            confidence_level='Low',
            remarks='Complex topic, needs revision'
        )
        db.session.add_all([log1, log2, log3, log4])
        db.session.commit()
        
        # Create Student Feedback
        feedback1 = StudentFeedback(
            student_id=student1.id,
            class_id=class1.id,
            subject_id=subject1.id,
            topic='Quadratic Equations',
            confidence_level='Medium',
            need_revision=True,
            comment='I need more practice with factoring',
            date=date(2024, 6, 5)
        )
        feedback2 = StudentFeedback(
            student_id=student2.id,
            class_id=class1.id,
            subject_id=subject2.id,
            topic='Energy and Work',
            confidence_level='Low',
            need_revision=True,
            comment='Very difficult to understand',
            date=date(2024, 6, 6)
        )
        feedback3 = StudentFeedback(
            student_id=student1.id,
            class_id=class1.id,
            subject_id=subject2.id,
            topic='Motion and Forces',
            confidence_level='High',
            need_revision=False,
            comment='Interesting topic, understood well',
            date=date(2024, 6, 2)
        )
        db.session.add_all([feedback1, feedback2, feedback3])
        db.session.commit()
        
        print("Database initialized successfully!")
        print("\nDemo Credentials:")
        print("Admin: username='admin', password='admin123'")
        print("Faculty: username='faculty', password='faculty123'")
        print("Student: username='student', password='student123'")
        print("Parent: username='parent', password='parent123'")

if __name__ == '__main__':
    init_database()
