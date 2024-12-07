# app/routes.py
from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from .models import db, Assignment, Subject
from datetime import datetime
from sqlalchemy import text


main = Blueprint('main', __name__)

@main.route('/')
def home():
    # return render_template('home.html')
    return redirect(url_for('main.get_assignments'))

@main.route('/select_role', methods=['POST'])
def select_role():
    role = request.form.get('role')
    if role == 'teacher':
        return redirect(url_for('main.get_assignments')) 
    elif role == 'student':
        return redirect(url_for('main.student_dashboard'))
    else:
        return redirect(url_for('home')) 


# Route to get assignments
@main.route('/assignments', methods=['GET'])
def get_assignments():
    subject_id = request.args.get('subject_id')
    sort_order = request.args.get('sort', 'asc')

    if sort_order not in ['asc', 'desc']:
        return jsonify({"error": "Invalid sort order. Use 'asc' or 'desc'"}), 400
    subject_list = Subject.query.all()
    query = "SELECT * FROM assignments"
    params = {}

    if subject_id and subject_id != "all":
        query += " WHERE subject_id = :subject_id"
        params["subject_id"] = subject_id

    query += f" ORDER BY due_date {sort_order.upper()}"

    assignments_list = db.session.execute(text(query), params).fetchall()
    return render_template('assignments.html', assignments=assignments_list, subjects=subject_list)

# app/routes.py
from sqlalchemy.sql import text

#route to add assignments
@main.route('/assignments/add', methods=['POST'])
def add_assignment():
    data = request.get_json()
    print(data)
    title = data.get("title")
    description = data.get("description")
    due_date = datetime.strptime(data.get("due_date"), "%Y-%m-%d").date()
    subject_id = data.get("subject") 

    subject = Subject.query.get(subject_id)
    if not subject:
        return jsonify({"error": "Selected subject does not exist"}), 400

    print(f"Inserting: title={title}, description={description}, due_date={due_date}, subject_id={subject_id}")    

    insert_query = text("""
        INSERT INTO assignments (title, description, due_date, subject_id)
        VALUES (:title, :description, :due_date, :subject_id)
        RETURNING id
    """)
    result = db.session.execute(insert_query, {
        "title": title,
        "description": description,
        "due_date": due_date,
        "subject_id": subject_id
    })
    new_id = result.fetchone()[0]
    db.session.commit()


    return jsonify({
        "id": new_id,
        "title": title,
        "description": description,
        "due_date": due_date.strftime("%Y-%m-%d"),
        "subject_id": subject_id
    })


#Route to delete assignments
@main.route('/assignments/<int:assignmentId>/delete', methods=['DELETE'])
def deleteAssignment(assignmentId):
    print("Assignment being deleted", assignmentId)
    assignment = Assignment.query.get(assignmentId)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"success": True, "message": "Assignment deleted"})

#Route to edit assignments
@main.route('/assignments/<int:assignment_id>/edit', methods=['PATCH'])
def edit_assignment(assignment_id):
    data = request.get_json()
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "Assignment not found"}), 404

    if "description" in data:
        assignment.description = data["description"]
    if "due_date" in data:
        assignment.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d")

    db.session.commit()
    return jsonify({
        "id": assignment.id,
        "description": assignment.description,
        "due_date": assignment.due_date.strftime("%Y-%m-%d")
    })

#Route to get add subjects
@main.route('/add_subject', methods=['POST'])
def add_subject():
    data = request.get_json()
    subject_name = data.get('name')

    existing_subject = Subject.query.filter_by(name=subject_name).first()
    if existing_subject:
        return jsonify({"error": "Subject already exists"}), 400

    new_subject = Subject(name=subject_name)
    db.session.add(new_subject)
    db.session.commit()

    return jsonify({"id": new_subject.id, "name": new_subject.name}), 201

#Route to see details of assignments
@main.route('/assignments/<int:assignment_id>', methods=['GET'])
def assignment_detail(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return render_template('404.html'), 404  

    completions = assignment.completions  
    return render_template(
        'assignment_detail.html',
        assignment=assignment,
        completions=completions
    )

#Route to filter by subject
@main.route('/assignments/filter', methods=['GET'])
def filter_assignments():
    subject_id = request.args.get('subject_id', type=int)
    
    if subject_id:
        assignments = db.session.execute(
            text("SELECT * FROM assignments WHERE subject_id = :subject_id"),
            {"subject_id": subject_id}
        ).fetchall()
    else:
        assignments = db.session.execute(
            text("SELECT * FROM assignments")
        ).fetchall()

    return jsonify([
        {
            "id": assignment.id,
            "title": assignment.title,
            "description": assignment.description,
            "due_date": assignment.due_date,
            "subject_id": assignment.subject_id
        }
        for assignment in assignments
    ])



