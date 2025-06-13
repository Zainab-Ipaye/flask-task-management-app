from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, DateTimeField, DateField, validators, ValidationError, BooleanField
from wtforms.validators import DataRequired, InputRequired, Length, Email, EqualTo, ValidationError
from .models import User, Project #, Sprint
from flask import current_app
import re

def coerce_to_int_or_none(value):
    if value is None or value == '':
        return None
    return int(value)


#Project Form Fields & Validation
class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired("Name is required"), Length(min=5, max=100, message="Username must be at least 5 characters.")])
    description = TextAreaField('Description', validators=[DataRequired("Description is required"), Length(min=5, max=1000, message="Description must have at least 5 characters and must not exceed 1000 characters")])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired("Start Date is required")])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired("End Date is required")])
    status = SelectField('Status', choices=[('Not Started', 'Not Started'), 
                                             ('In Progress', 'In Progress'), 
                                             ('Completed', 'Completed')], 
                        default='Not Started', validators=[DataRequired("Status is required")])
    submit = SubmitField('Create Project')

    def validate_end_date(self, field):
        """
        Custom validator to ensure end_date is after start_date.
        """
        if self.start_date.data and field.data and field.data <= self.start_date.data:
            raise ValidationError("End Date must be after the Start Date.")


def validate_password(form,field):
        password=field.data
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        if not re.search(r"\d", password):
            raise ValidationError('Password must contain at least 1 number.')
        if not re.search(r"[A-Z]", password):
            raise ValidationError('Password must contain at least one upper case letter.')
        if not re.search(r"[a-z]", password):
            raise ValidationError('Password must contain at least one lower case letter.')
        if not re.search(r"[!@#$%^&*(),.?\/:{}<>|]", password):
            raise ValidationError('Password must contain at least one special character.')


#Registration Form Fields & Validation
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("Username is required"), Length(min=5, max=100, message="Username must be at least 5 characters.")])
    email = StringField('Email', validators=[DataRequired("Email is required"), Email(message="Invalid email address.")])
    password = PasswordField('Password', validators=[validators.DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message="Please confirm your password."), EqualTo('password', message="Password must match")])
    role  = SelectField('Role', choices=[('user'), ('admin')], default='user', validators=[DataRequired("Role is required")])
    
    submit = SubmitField('Sign Up')

#Login Form Fields & Validation
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Email is required"), Email(message="Invalid email address.")])
    password = PasswordField('Password', validators=[DataRequired("Password is required")])
    submit = SubmitField('Login')

#Task Form Fields & Validation
class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired("Title is required"), Length(min=5, max=100, message="Title must have at least 5 characters")])
    description = TextAreaField('Description', validators=[DataRequired("Description is required"), Length(min=5, max=1000, message="Description must have at least 5 characters and must not exceed 1000 characters")])
    hours_allocated = IntegerField('Hours Allocated', validators=[DataRequired("Hours Allocated is required")])
    status = SelectField('Status', choices=[('New', 'New'), 
                                             ('In Progress', 'In Progress'), 
                                             ('Completed', 'Completed'), 
                                             ('Removed', 'Removed')], 
                         default='new', validators=[DataRequired("Status is required")])
    
    assigned_to = SelectField('Assigned To', coerce=coerce_to_int_or_none, validators=[DataRequired("Assigned To is required")])  
    project_id = SelectField('Project', coerce=coerce_to_int_or_none, validators=[DataRequired("Project is required")])

    
    hours_remaining = IntegerField(
        'Hours Remaining', 
        validators=[
            InputRequired("Hours Remaining is required")  # Replace DataRequired with InputRequired
        ]
    )

    submit = SubmitField('Create Task')

#Setting Up Assigned To Lookup Field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with current_app.app_context():

            self.assigned_to.choices = [(None, 'Select User')] + [
                (user.id, user.username) for user in User.query.all()
            ]

#Setting Up Project Lookup Field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with current_app.app_context():

            self.project_id.choices = [(None, 'Select Project')] + [
                (project.id, project.name) for project in Project.query.all()
            ]

