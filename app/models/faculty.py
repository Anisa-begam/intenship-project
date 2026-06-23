"""
Faculty model
"""

from app import db

class Faculty(db.Model):
    """Faculty model"""
    __tablename__ = 'faculty'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    department = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    joining_date = db.Column(db.Date)
    
    # Relationships
    logs = db.relationship('FacultyLog', backref='faculty', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Faculty {self.employee_id}>'
