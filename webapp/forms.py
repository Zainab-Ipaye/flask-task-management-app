from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, DateTimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from .models import User, Project #, Sprint
from flask import current_app

def coerce_to_int_or_none(value):
    if value is None or value == '':
        return None
    return int(value)


class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired("Name is required"), Length(min=5, max=100, message="Username must be at least 5 characters.")])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired("Start Date is required")])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired("End Date is required")])
    submit = SubmitField('Create Project')


#class SprintForm(FlaskForm):
 #   name = StringField('Sprint Name', validators=[DataRequired()])
  #  start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
   # end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()])

    #project_id = SelectField('Project ID', coerce=coerce_to_int_or_none, validators=[DataRequired()])  
    #submit = SubmitField('Create Sprint')

    #def __init__(self, *args, **kwargs):
      #  super().__init__(*args, **kwargs)
      #  with current_app.app_context():
        
       #     self.project_id.choices =  [(None, 'Select Project')] + [
       #         (project.id, project.name) for project in Project.query.all()]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Username is required"), Length(min=5, max=100, message="Username must be at least 5 characters.")])
    email = StringField('Email', validators=[DataRequired("Email is required"), Email(message="Invalid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Password is required"), Length(min=8, message="Password must have at least 8 characters")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="Please confirm your password."), EqualTo('password', message="Password must match")])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Email is required"), Email(message="Invalid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Password is required"), Length(min=8, message="Password must have at least 8 characters")])
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired("Title is required"), Length(min=5, max=100, message="Title must have at least 5 characters")])
    description = TextAreaField('Description', validators=[DataRequired("Description is required"), Length(min=5, max=500, message="Description must have at least 5 characters")])
    hours_allocated = IntegerField('Hours Allocated', validators=[DataRequired("Hours Allocated is required")])
    status = SelectField('Status', choices=[('New', 'New'), 
                                             ('In Progress', 'In Progress'), 
                                             ('Completed', 'Completed'), 
                                             ('Removed', 'Removed')], 
                         default='new', validators=[DataRequired("Status is required")])
    
    assigned_to = SelectField('Assigned To', coerce=coerce_to_int_or_none, validators=[DataRequired("Assigned To is required")])  
    project_id = SelectField('Project', coerce=coerce_to_int_or_none, validators=[DataRequired("Project is required")])
    #task_sprint = SelectField('Sprint', choices=[], coerce=coerce_to_int_or_none)

    
    hours_remaining = IntegerField('Hours Remaining', validators=[DataRequired("Hours Remaining is required")])
    submit = SubmitField('Create Task')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with current_app.app_context():

            self.assigned_to.choices = [(None, 'Select User')] + [
                (user.id, user.username) for user in User.query.all()
            ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with current_app.app_context():

            self.project_id.choices = [(None, 'Select Project')] + [
                (project.id, project.name) for project in Project.query.all()
            ]

    #def __init__(self, *args, **kwargs):
     #   super().__init__(*args, **kwargs)
      #  with current_app.app_context():

 #           self.task_sprint.choices = [(None, 'Select Sprint')] + [
  #              (sprint.id, sprint.name) for sprint in Sprint.query.all()
   #         ]

