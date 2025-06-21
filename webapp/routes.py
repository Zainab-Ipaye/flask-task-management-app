from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from webapp import db, bcrypt
from webapp.models import User, Task, Project
from webapp.audit import log_activity
from webapp.forms import (
    RegistrationForm,
    LoginForm,
    TaskForm,
    ProjectForm,
)


bp = Blueprint("main", __name__)


# Public home route - no login required
@bp.route("/")
def home():
    # If the user is logged in, redirect to the task board
    if current_user.is_authenticated:
        return redirect(url_for("main.list_tasks"))
    # If the user is not logged in, show the login/register page
    return render_template("home.html")


# Registration route
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )  # Hash password with bcrypt
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
        )

        # Add user to the database
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("main.login"))  # Redirect after successful registration

    # If form submission is invalid or on initial page load, render the form again
    return render_template("register.html", form=form)


# Login route
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            log_activity("User logged in")
            print("User logged in successfully")
            flash(f"Welcome, {current_user.username}!", "success")
            return redirect(url_for("main.list_tasks"))
        else:
            print("Login failed - bad credentials")
            flash("Login failed. Check email and/or password.", "danger")
    else:
        print("Form validation errors:", form.errors)
    return render_template("login.html", form=form)


# Logout route
@bp.route("/logout")
def logout():
    log_activity("User logged out")
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.home"))


# TASKS ROUTES


# Task board route for logged-in users
@bp.route("/tasks/create", methods=["GET", "POST"])
@login_required
def create_task():
    form = TaskForm()

    form.assigned_to.choices = [("", "Select User")] + [
        (user.id, user.username) for user in User.query.all()
    ]
    form.project_id.choices = [("", "Select Project")] + [
        (project.id, project.name) for project in Project.query.all()
    ]

    if form.validate_on_submit():

        task = Task(
            title=form.title.data,
            description=form.description.data,
            hours_allocated=form.hours_allocated.data,
            status=form.status.data,
            hours_remaining=form.hours_remaining.data,
            assigned_to=form.assigned_to.data,
            project_id=form.project_id.data,
            created_by=current_user.id,
        )

        db.session.add(task)
        db.session.commit()

        log_activity(f"Created task: {task.title}")

        flash("Task created successfully!", "success")
        return redirect(url_for("main.list_tasks"))
    return render_template("create_task.html", form=form)


# Edit Task Route
@bp.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    form = TaskForm(obj=task)

    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]
    form.project_id.choices = [("", "Select Project")] + [
        (project.id, project.name) for project in Project.query.all()
    ]

    if form.validate_on_submit():

        task.title = form.title.data
        task.description = form.description.data
        task.hours_allocated = form.hours_allocated.data
        task.status = form.status.data
        task.hours_remaining = form.hours_remaining.data
        task.project_id = form.project_id.data
        task.assigned_to = form.assigned_to.data

        print(f"Task Updated: {task.title}, {task.project_id}")

        db.session.commit()
        log_activity(f"Edited task: {task.title}")

        flash("Task updated successfully!", "success")
        return redirect(url_for("main.list_tasks"))
    return render_template("edit_task.html", form=form, task=task)


# Delete task route - admin only, login required
@bp.route("/task/<int:task_id>/delete", methods=["POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role == "admin":
        db.session.delete(task)
        db.session.commit()

        log_activity(f"Deleted task: {task.title}")

        flash("Task has been deleted.", "success")
    else:
        flash("You do not have permission to delete tasks.", "danger")
    return redirect(url_for("main.list_tasks"))


@bp.route("/tasks", methods=["GET"])
@login_required
def list_tasks():

    page = request.args.get("page", 1, type=int)
    per_page = 5

    assignee_id = request.args.get("assignee", type=int)
    project_id = request.args.get("project", type=int)

    # Base query
    tasks_query = Task.query

    # Apply filters
    if assignee_id:
        tasks_query = tasks_query.filter(Task.assigned_to == assignee_id)
    if project_id:
        tasks_query = tasks_query.filter(Task.project_id == project_id)

    pagination = tasks_query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items

    # Get distinct assigned user IDs from *all* tasks (not just paginated tasks)
    assigned_user_ids = (
        db.session.query(Task.assigned_to)
        .distinct()
        .filter(Task.assigned_to.isnot(None))
        .all()
    )
    assigned_user_ids = [uid[0] for uid in assigned_user_ids]

    # Get users with tasks
    users = User.query.filter(User.id.in_(assigned_user_ids)).all()

    # Get distinct assigned project IDs from *all* tasks
    assigned_project_ids = (
        db.session.query(Task.project_id)
        .distinct()
        .filter(Task.project_id.isnot(None))
        .all()
    )
    assigned_project_ids = [pid[0] for pid in assigned_project_ids]

    # Get projects with tasks
    projects = Project.query.filter(Project.id.in_(assigned_project_ids)).all()

    return render_template(
        "list_tasks.html",
        tasks=tasks,
        users=users,
        projects=projects,
        pagination=pagination,
    )


# PROJECT ROUTES


@bp.route("/projects/create", methods=["GET", "POST"])
@login_required
def create_project():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
        )

        db.session.add(project)
        db.session.commit()

        log_activity(f"Created project: {project.name}")

        flash("Project created successfully!", "success")
        return redirect(url_for("main.list_projects"))
    else:
        if form.errors:
            print("Form errors:", form.errors)

    return render_template("create_project.html", form=form)


# Edit Project Route
@bp.route("/project/<int:project_id>/edit", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.status = form.status.data
        db.session.commit()

        log_activity(f"Edited task: {project.name}")

        flash("Project updated successfully!", "success")
        return redirect(url_for("main.list_projects"))
    else:
        if form.errors:
            print("Form errors:", form.errors)

    return render_template("edit_project.html", form=form, project=project)


# Delete Project Route
@bp.route("/project/<int:project_id>/delete", methods=["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)

    if current_user.role == "admin":
        Task.query.filter_by(project_id=project_id).delete()
        db.session.delete(project)
        db.session.commit()

        log_activity(f"Deleted project: {project.name}")

        flash("Project has been deleted.", "success")
    else:
        flash("You do not have permission to delete this project.", "danger")

    return redirect(url_for("main.list_projects"))


@bp.route("/projects", methods=["GET"])
@login_required
def list_projects():

    project_id_filter = request.args.get("project", type=int)
    status_filter = request.args.get("status", type=str)

    # Get all projects for filter dropdowns
    all_projects = Project.query.order_by(Project.name).all()
    all_statuses = list(set(p.status for p in all_projects))

    # Build filtered query for results
    query = Project.query
    if project_id_filter:
        query = query.filter(Project.id == project_id_filter)
    if status_filter:
        query = query.filter(Project.status == status_filter)

    # Pagination
    page = request.args.get("page", 1, type=int)
    per_page = 5
    pagination = query.order_by(Project.start_date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    projects = pagination.items

    return render_template(
        "list_projects.html",
        projects=projects,
        pagination=pagination,
        all_projects=all_projects,
        all_statuses=all_statuses,
        project_id_filter=project_id_filter,
        status_filter=status_filter,
    )


# PROFILE ROUTES


@bp.route("/profile")
def profile():
    # Fetch user details from the database
    user = User.query.get(current_user.id)  # assuming current_user is logged in
    return render_template("profile.html", user=user)


@bp.route("/update_profile", methods=["POST"])
def update_profile():
    # Get the current logged-in user
    user = User.query.get(current_user.id)

    # Update the user's details
    user.username = request.form["username"]
    user.email = request.form["email"]

    # Commit the changes to the database
    db.session.commit()

    log_activity("Updated profile")

    flash("Profile updated successfully", "success")

    # Redirect to the profile page after updating
    return redirect(url_for("main.profile"))


# MANAGER USER ROUTES


@bp.route("/admin/users", methods=["GET", "POST"])
@login_required
def manage_users():

    print("Current user in /admin/users:", current_user)
    print("Is authenticated?", current_user.is_authenticated)
    print("Role:", getattr(current_user, "role", None))

    if current_user.role != "admin":
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for("main.list_tasks"))

    username_filter = request.args.get("username", "").lower()
    all_users = User.query.all()  # Fetch all users from the database

    if username_filter:
        users = [user for user in all_users if username_filter in user.username.lower()]
    else:
        users = all_users

    return render_template("admin_users.html", users=users)


@bp.route("/admin/user/<int:user_id>/update_role", methods=["POST"])
@login_required
def update_role(user_id):
    if current_user.role != "admin":
        flash("You do not have permission to update these records.", "danger")
        return redirect(url_for("main.manage_users"))

    user = User.query.get_or_404(user_id)
    user.role = request.form["role"]
    db.session.commit()

    log_activity("Updated role")

    flash("User role has been updated.", "success")
    return redirect(url_for("main.manage_users"))
