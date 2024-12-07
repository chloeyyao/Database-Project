# app/models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationship with Assignment
    assignments = db.relationship('Assignment', back_populates='subject')

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, index=True)
    completions = db.relationship(
        "AssignmentCompletion",
        back_populates="assignment",
        cascade="all, delete-orphan"
    )

    # Relationship to subject
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), index=True)
    subject = db.relationship('Subject', back_populates='assignments')

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class AssignmentCompletion(db.Model):
    __tablename__ = 'assignment_completions'
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id', ondelete="CASCADE"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    completion_time = db.Column(db.DateTime)
    status = db.Column(db.String(20)) 

    # Relationships to Assignment and Student
    assignment = db.relationship("Assignment", back_populates="completions")
    student = db.relationship('Student', backref=db.backref('assignments', lazy=True))
