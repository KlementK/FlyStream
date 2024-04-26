# views.py

from flask import Blueprint, render_template, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from .models import Task
from .svg_paths import svg_paths
from . import db

views = Blueprint('views', __name__)

# context processor to make `svg_paths` global
@views.app_context_processor
def inject_svg_paths():
    return dict(svgs=svg_paths)

@views.route('/about', methods=['GET'])
def about():
    return render_template("about.html", user=current_user)

@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/tasks_daily', methods=['GET', 'POST'])
@login_required
def tasks_daily():
    if request.method == 'POST':
        task_content = request.form.get('task')
        add_task(current_user.id, task_content, 'daily')
    tasks = get_tasks(current_user.id, 'daily')
    return render_template("tasks_daily.html", user=current_user, tasks=tasks)

@views.route('/tasks_weekly', methods=['GET', 'POST'])
@login_required
def tasks_weekly():
    if request.method == 'POST':
        task_content = request.form.get('task')
        add_task(current_user.id, task_content, 'weekly')
    tasks = get_tasks(current_user.id, 'weekly')
    return render_template("tasks_weekly.html", user=current_user, tasks=tasks)

@views.route('/tasks_monthly', methods=['GET', 'POST'])
@login_required
def tasks_monthly():
    if request.method == 'POST':
        task_content = request.form.get('task')
        add_task(current_user.id, task_content, 'monthly')
    tasks = get_tasks(current_user.id, 'monthly')
    return render_template("tasks_monthly.html", user=current_user, tasks=tasks)



@views.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:  # Check task owner
        db.session.delete(task)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 403

#

def get_tasks(user_id, task_type):
    return Task.query.filter_by(user_id=user_id, type=task_type).all()

def add_task(user_id, task_content, task_type):
    if len(task_content) < 1:
        flash('Task is too short!', category='error')
        return False
    new_task = Task(type=task_type, data=task_content, user_id=user_id)
    db.session.add(new_task)
    try:
        db.session.commit()
        flash('Task added successfully!', category='success')
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error adding task to database: {e}")
        return False