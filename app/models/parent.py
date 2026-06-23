"""
Parent model
"""

from app import db

class Parent(db.Model):
    """Parent model"""
    __tablename__ = 'parents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone = db.Column(db.String(15))
    occupation = db.Column(db.String(100))
    
    # Relationships
    student_mappings = db.relationship('ParentStudentMapping', backref='parent', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Parent {self.id}>'
