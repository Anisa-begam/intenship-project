"""
Database models package
"""

from app.models.user import User
from app.models.student import Student
from app.models.parent import Parent
from app.models.faculty import Faculty
from app.models.subject import Subject
from app.models.class_model import Class
from app.models.faculty_log import FacultyLog
from app.models.student_feedback import StudentFeedback
from app.models.parent_student_mapping import ParentStudentMapping

__all__ = [
    'User', 'Student', 'Parent', 'Faculty', 'Subject', 'Class',
    'FacultyLog', 'StudentFeedback', 'ParentStudentMapping'
]
