# populate_data.py
from app import create_app
from app.models import db, Subject, Assignment, Student, AssignmentCompletion
from datetime import datetime

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    math = Subject(name="Mathematics")
    science = Subject(name="Science")
    db.session.add_all([math, science])
    db.session.commit()

    assignment1 = Assignment(title="Algebra Homework", description="Complete all exercises in Chapter 3", due_date=datetime(2024, 11, 1), grade_level="10th Grade", subject=math)
    assignment2 = Assignment(title="Biology Lab Report", description="Write a report on the plant cell structure", due_date=datetime(2024, 11, 5), grade_level="10th Grade", subject=science)
    db.session.add_all([assignment1, assignment2])
    db.session.commit()

    student1 = Student(name="Alice Johnson", grade_level="10th Grade")
    student2 = Student(name="Bob Smith", grade_level="10th Grade")
    db.session.add_all([student1, student2])
    db.session.commit()

    completion1 = AssignmentCompletion(assignment_id=assignment1.id, student_id=student1.id, completion_time=datetime(2024, 10, 28, 15, 30), status="completed")
    completion2 = AssignmentCompletion(assignment_id=assignment2.id, student_id=student2.id, completion_time=datetime(2024, 10, 28, 16, 45), status="completed")
    db.session.add_all([completion1, completion2])
    db.session.commit()

    print("Data populated successfully.")
