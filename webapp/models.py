from datetime import datetime
from webapp import db, bcrypt 
from flask_login import UserMixin


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # Relationship with Sprint
  #  sprints = db.relationship('Sprint', backref='parent_project', lazy=True)
    tasks = db.relationship('Task', backref='project', lazy=True)


    def __repr__(self):
        return f'<Project {self.name}>'

#class Sprint(db.Model):
 #   __tablename__ = 'sprints'
  #  id = db.Column(db.Integer, primary_key=True)
   # name = db.Column(db.String(100), nullable=False)
    #start_date = db.Column(db.Date, nullable=False)
    #end_date = db.Column(db.Date, nullable=False)
    
    # Foreign key linking Sprint to Project
    #project = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    #projectlookup = db.relationship('Project', foreign_keys=[project], backref='project_lookup')

    #tasks = db.relationship('Task', backref='sprint', lazy=True)



    #def __repr__(self):
     #   return f'<Sprint {self.name}>'

    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='user')  
    
    tasks = db.relationship('Task', foreign_keys='Task.created_by', backref='author', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

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
    status = db.Column(db.String(20), default='new', nullable=False)
    hours_remaining = db.Column(db.Integer, nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Owner of the task

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  
    projectlookupfortasks = db.relationship('Project', foreign_keys=[project_id], backref='project_lookup_for_tasks')

   # sprint_id = db.Column(db.Integer, db.ForeignKey('sprints.id'), nullable=True)  
    #sprintlookup = db.relationship('Sprint', foreign_keys=[sprint_id], backref='tasks_in_sprint')

    # Relationship for creator (created_by) - specify the foreign key
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_tasks')
    
    # Relationship for assignee (assigned_to) - specify the foreign key
    assignee = db.relationship('User', foreign_keys=[assigned_to], backref='assigned_tasks')

    def __repr__(self):
        return f'<Task {self.title}>'
