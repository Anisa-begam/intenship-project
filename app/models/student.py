"""
Student model
"""

from app import db
from datetime import datetime

class Student(db.Model):
    """Student model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    date_of_birth = db.Column(db.Date)
    admission_date = db.Column(db.Date, default=datetime.utcnow)
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    
    # Relationships
    class_info = db.relationship('Class', backref='students')
    feedbacks = db.relationship('StudentFeedback', backref='student', cascade='all, delete-orphan')
    parent_mappings = db.relationship('ParentStudentMapping', backref='student', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.roll_number}>'
