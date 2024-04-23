from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # 'daily', 'weekly', 'monthly'
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Task {self.type} {self.data}>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    tasks = db.relationship('Task')
