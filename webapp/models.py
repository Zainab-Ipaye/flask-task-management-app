from datetime import datetime
from webapp import db, bcrypt
from flask_login import UserMixin
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Not Started", nullable=False)

    tasks = db.relationship("Task", backref="project", lazy=True)

    def __repr__(self):
        return f"<Project {self.name}>"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")

    # A user can create many tasks
    created_tasks = db.relationship(
        "Task", foreign_keys="Task.created_by", backref="creator", lazy=True
    )

    # A user can be assigned to many tasks
    assigned_tasks = db.relationship(
        "Task", foreign_keys="Task.assigned_to", backref="assignee", lazy=True
    )

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def get_role(cls, user_id):
        return cls.query.filter_by(id=user_id).first().role


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    hours_allocated = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="new", nullable=False)
    hours_remaining = db.Column(db.Integer, nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    projectlookupfortasks = db.relationship(
        "Project", foreign_keys=[project_id], overlaps="project,tasks"
    )

    @validates("hours_allocated", "hours_remaining")
    def validate_hours(self, key, value):
        if value < 0:
            raise ValueError(f"{key.replace('_', ' ').title()} cannot be negative")
        return value

    __table_args__ = (
        CheckConstraint(
            "hours_allocated >= 0", name="check_hours_allocated_non_negative"
        ),
        CheckConstraint(
            "hours_remaining >= 0", name="check_hours_remaining_non_negative"
        ),
    )

    def __repr__(self):
        return f"<Task {self.title}>"


class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship("User", backref="activity_logs")
