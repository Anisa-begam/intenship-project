"""
Faculty Log model for daily syllabus tracking
"""

from app import db
from datetime import datetime

class FacultyLog(db.Model):
    """Faculty log for daily syllabus progress"""
    __tablename__ = 'faculty_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    unit = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    completion_percentage = db.Column(db.Integer, nullable=False)  # 0-100
    confidence_level = db.Column(db.String(20), nullable=False)  # 'Low', 'Medium', 'High'
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    class_info = db.relationship('Class', backref='faculty_logs')
    
    def __repr__(self):
        return f'<FacultyLog {self.faculty_id} - {self.topic}>'
