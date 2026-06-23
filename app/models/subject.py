"""
Subject model
"""

from app import db

class Subject(db.Model):
    """Subject model"""
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    total_units = db.Column(db.Integer, default=1)
    description = db.Column(db.Text)
    
    # Relationships
    class_info = db.relationship('Class', backref='subjects')
    logs = db.relationship('FacultyLog', backref='subject', cascade='all, delete-orphan')
    feedbacks = db.relationship('StudentFeedback', backref='subject', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Subject {self.code} - {self.name}>'
