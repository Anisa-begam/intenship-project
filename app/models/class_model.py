"""
Class model
"""

from app import db

class Class(db.Model):
    """Class model"""
    __tablename__ = 'classes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)  # e.g., "10th Grade - A"
    grade = db.Column(db.String(20), nullable=False)  # e.g., "10th"
    section = db.Column(db.String(10))  # e.g., "A"
    academic_year = db.Column(db.String(20), nullable=False)
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('faculty.id'))
    
    # Relationships
    class_teacher = db.relationship('Faculty', backref='managed_classes')
    
    def __repr__(self):
        return f'<Class {self.name}>'
