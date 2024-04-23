from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/tasks_daily', methods=['GET', 'POST'])
@login_required
def tasks_daily():
    if request.method == 'POST':
        task_content = request.form.get('task')
        print(f"Received task content: {task_content}")  # Debug print

        if len(task_content) < 1:
            flash('Task is too short!', category='error')
            print("Error: Task is too short")  # Debug print
        else:
            new_task = Task(type='daily', data=task_content, user_id=current_user.id)
            db.session.add(new_task)
            try:
                db.session.commit()
                flash('Daily task added!', category='success')
                print(f"Task added successfully: {new_task}")  # Debug print
            except Exception as e:
                db.session.rollback()
                print(f"Error adding task to database: {e}")  # Debug print

    # Retrieve all tasks for the current user to display
    tasks = Task.query.filter_by(user_id=current_user.id, type='daily').all()
    print(f"Tasks retrieved for display: {tasks}")  # Debug print
    return render_template("tasks_daily.html", user=current_user, tasks=tasks)

@views.route('/tasks_weekly', methods=['GET', 'POST'])
@login_required
def tasks_weekly():
    if request.method == 'POST':
        task_content = request.form.get('task')
        if len(task_content) < 1:
            flash('Task is too short!', category='error')
        else:
            new_task = Task(type='weekly', data=task_content, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Weekly task added!', category='success')
    return render_template("tasks_weekly.html", user=current_user)

@views.route('/tasks_monthly', methods=['GET', 'POST'])
@login_required
def tasks_monthly():
    if request.method == 'POST':
        task_content = request.form.get('task')
        if len(task_content) < 1:
            flash('Task is too short!', category='error')
        else:
            new_task = Task(type='monthly', data=task_content, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            flash('Monthly task added!', category='success')
    return render_template("tasks_monthly.html", user=current_user)

@views.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:  # Check task ownership
        db.session.delete(task)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403