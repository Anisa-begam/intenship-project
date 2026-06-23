"""
Parent-Student mapping model
"""

from app import db

class ParentStudentMapping(db.Model):
    """Mapping between parents and students"""
    __tablename__ = 'parent_student_mappings'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    relationship = db.Column(db.String(20), nullable=False)  # 'Father', 'Mother', 'Guardian'
    is_primary = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<ParentStudentMapping {self.parent_id} - {self.student_id}>'
