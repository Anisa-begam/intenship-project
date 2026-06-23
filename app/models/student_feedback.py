"""
Student Feedback model
"""

from app import db
from datetime import datetime

class StudentFeedback(db.Model):
    """Student feedback on topics"""
    __tablename__ = 'student_feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    confidence_level = db.Column(db.String(20), nullable=False)  # 'Low', 'Medium', 'High'
    need_revision = db.Column(db.Boolean, default=False)
    comment = db.Column(db.Text)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    class_info = db.relationship('Class', backref='student_feedbacks')
    
    def __repr__(self):
        return f'<StudentFeedback {self.student_id} - {self.topic}>'
