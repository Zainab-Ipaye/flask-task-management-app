from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from webapp import db, bcrypt 
from webapp.models import User, Task, Project #, Sprint
from webapp.forms import RegistrationForm, LoginForm, TaskForm, ProjectForm #, SprintForm
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('main', __name__)



# Public home route - no login required
@bp.route('/')
def home():
    # If the user is logged in, redirect to the task board
    if current_user.is_authenticated:
        return redirect(url_for('main.list_tasks'))
    # If the user is not logged in, show the login/register page
    return render_template('home.html')



@bp.route('/profile')
def profile():
    # Fetch user details from the database
    user = User.query.get(current_user.id)  # assuming current_user is logged in
    return render_template('profile.html', user=user)


@bp.route('/update_profile', methods=['POST'])
def update_profile():
    # Get the current logged-in user
    user = User.query.get(current_user.id)
    
    # Update the user's details
    user.username = request.form['username']
    user.email = request.form['email']

    # Commit the changes to the database
    db.session.commit()
    flash('Profile updated successfully', 'success')

    # Redirect to the profile page after updating
    return redirect(url_for('main.profile'))











@bp.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = ProjectForm()  

    if form.validate_on_submit():
        # Save task to the database
        project = Project(
            name=form.name.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data)

        db.session.add(project)
        db.session.commit()

        flash('Project created successfully!', 'success')
        return redirect(url_for('main.list_projects'))

    return render_template('create_project.html', form=form)


@bp.route('/project/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    form = ProjectForm(obj=project)  
    if form.validate_on_submit():
        project.name=form.name.data
        project.start_date=form.start_date.data
        project.end_date=form.end_date.data
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.list_projects'))

    return render_template('edit_project.html', form=form, project=project)

@bp.route('/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user.role == 'admin':
        db.session.delete(project)
        db.session.commit()

        flash('Project has been deleted.', 'success')
    else:
        flash('You do not have permission to delete this project.', 'danger')

    return redirect(url_for('main.list_projects'))

@bp.route('/projects', methods=['GET'])
@login_required
def list_projects():
    projects = Project.query.all()
    return render_template('list_projects.html', projects=projects )











# Task board route for logged-in users

@bp.route('/tasks/create', methods=['GET','POST'])
@login_required
def create_task():
    form = TaskForm()  
    
 #   sprints = Sprint.query.filter_by(project=form.task_project.data).all()
  #  form.task_sprint.choices = [(sprint.id, sprint.name) for sprint in sprints]
   # form.task_sprint.choices = []

    form.assigned_to.choices = [('', 'Select User')] + [(user.id, user.username) for user in User.query.all()]
    form.project_id.choices = [('', 'Select Project')] + [(project.id, project.name) for project in Project.query.all()]
   # form.task_sprint.choices = [('', 'Select Sprint')] + [(sprint.id, sprint.name) for sprint in Sprint.query.all()]
    

    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            description=form.description.data,
            hours_allocated=form.hours_allocated.data,
            status=form.status.data, 
            hours_remaining=form.hours_remaining.data, 
            assigned_to=form.assigned_to.data,
            project_id=form.project_id.data,
         #   sprint_id=form.task_sprint.data,   
            created_by=current_user.id)
        
        db.session.add(task)
        db.session.commit()
        flash('Your task has been created!', 'success')
        return redirect(url_for('main.list_tasks'))
    return render_template('create_task.html', form=form)


@bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
 
    form = TaskForm(obj=task)  
    #project_id = task.project.id if task.project else None

    #sprint_id = task.sprint.id if task.sprint else None
    #sprints = Sprint.query.filter_by(project=project_id).all() if project_id else []

    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]  # Users for the 'assigned_to' field
    #form.project_id.choices = [(project.id, project.name) for project in Project.query.all()] 
    form.project_id.choices = [('', 'Select Project')] + [(project.id, project.name) for project in Project.query.all()]
 # Projects for the 'task_project' field
    #form.task_sprint.choices = [(sprint.id, sprint.name) for sprint in sprints]
    #form.task_sprint.data = sprint_id
#selected_sprint = task.sprint.id if task.sprint else None
    #form.task_project.data = task.project.id if task.project else None  # Set the pre-selected project
    #form.task_sprint.data = task.sprint.id if task.sprint else None
    
    if form.validate_on_submit():

        task.title = form.title.data
        task.description = form.description.data
        task.hours_allocated = form.hours_allocated.data
        task.status=form.status.data
        task.hours_remaining=form.hours_remaining.data
        task.project_id = form.project_id.data  # This should update the project_id field
        #task.task_sprint=form.task_sprint.data
        task.assigned_to=form.assigned_to.data

        print(f"Task Updated: {task.title}, {task.project_id}")

        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.list_tasks'))
    return render_template('edit_task.html', form=form, task=task) #, selected_sprint=selected_sprint)

# Delete task route - admin only, login required
@bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role == 'admin':
        db.session.delete(task)
        db.session.commit()
        flash('Task has been deleted.', 'success')
    else:
        flash('You do not have permission to delete tasks.', 'danger')
    return redirect(url_for('main.list_tasks'))

@bp.route('/tasks', methods=['GET'])
@login_required
def list_tasks():
    assignee_id = request.args.get('assignee', type=int)
    project_id = request.args.get('project', type=int)
    #sprint_id = request.args.get('sprint', type=int)

    # Base query
    tasks_query = Task.query

    # Apply filters
    if assignee_id:
        tasks_query = tasks_query.filter(Task.assigned_to == assignee_id)
    if project_id:
        tasks_query = tasks_query.filter(Task.project_id == project_id)
   # if sprint_id:
    #    tasks_query = tasks_query.filter(Task.sprint_id == sprint_id)


    tasks = tasks_query.all()

    # Fetch users and projects for the filters
    users = User.query.all()
    projects = Project.query.all()
   # sprints = Sprint.query.all()

    users_with_tasks = set(task.assignee for task in tasks if task.assignee)
    projects_with_tasks = set(task.project for task in tasks if task.project)
    
    users = User.query.filter(User.id.in_([user.id for user in users_with_tasks])).all()
    projects = Project.query.filter(Project.id.in_([project.id for project in projects_with_tasks])).all()


    return render_template('list_tasks.html', tasks=tasks, users=users, projects=projects) #, sprints=sprints)








# Registration route 
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# Login route 
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('main.list_tasks'))
        else:
            flash('Login failed. Check email and/or password.', 'danger')
    return render_template('login.html', form=form)

# Logout route
@bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))




@bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))

    users = User.query.all()
    return render_template('admin_users.html', users=users)



@bp.route('/admin/user/<int:user_id>/update_role', methods=['POST'])
@login_required
def update_role(user_id):
    if current_user.role != 'admin':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('main.home'))

    user = User.query.get_or_404(user_id)
    user.role = request.form['role']
    db.session.commit()
    flash('User role has been updated.', 'success')
    return redirect(url_for('main.manage_users'))