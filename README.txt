Zainab's Task Management App: A Comprehensive Guide


Overview:

Zainab's Task Management App is a secure, containerized Flask web application for managing projects and tasks. It supports user registration, login, role-based access, and real-time task and project management. The app incorporates modern DevOps practices, including CI/CD pipelines with GitHub Actions, static code analysis, security scanning, and Dockerized deployment to Heroku.

This README details setup, usage, testing, deployment, and troubleshooting.



Main Features:

User Registration & Authentication: Secure login with role-based access (admin/user).

Task Management: Users can create, read, update tasks; admins can also delete.

Project Management: Users and admins can manage projects with key fields (name, start/end date, status).

Admin Controls: Admins can manage users and security roles.

Real-time Updates & Notifications: Flash messages and validations appear on task/project actions.

Security: CSRF protection, secure password hashing, environment-based secret management.

DevOps: Automated linting, testing, security scanning, and Docker-based deployment.



Setup Instructions:

Prerequisites -

Python 3.11+

Git

Docker

Heroku CLI

(Optional) Virtual environment tool




Steps to Set Up Locally

Clone the repository

bash
git clone <repository-url>
cd <repository-folder>
Create a Virtual Environment

bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
Install Dependencies

bash
pip install -r requirements.txt
Set Up the Database

bash
flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade
Run the Application

bash
python run.py
Access the App

Open http://localhost:5000 in your browser.

All dependencies can be found in the requirements.txt file which is included in the source code file.


MySQL Setup with JawsDB on Heroku (Docker Deployment)
Steps
Create Heroku app and add JawsDB

bash
heroku create <your-app-name>
heroku addons:create jawsdb:kitefin --app <your-app-name>
Retrieve JawsDB URL

bash
heroku config:get JAWSDB_URL --app <your-app-name>
Set the database URL environment variable for your app

Your app expects SQLALCHEMY_DATABASE_URI, so set it like this:

bash
heroku config:set SQLALCHEMY_DATABASE_URI=$(heroku config:get JAWSDB_URL --app <your-app-name>) --app <your-app-name>
Set other necessary environment variables

bash
heroku config:set SECRET_KEY=your-production-secret-key --app <your-app-name>
heroku config:set FLASK_ENV=production --app <your-app-name>
Deploy your Docker container

Use your GitHub Actions pipeline or manually:

bash
docker build -t registry.heroku.com/<your-app-name>/web .
docker push registry.heroku.com/<your-app-name>/web
heroku container:release web --app <your-app-name>
Run database migrations

You can run migrations inside the Heroku container:

bash
heroku run flask db upgrade --app <your-app-name>
Access your deployed app

bash
heroku open --app <your-app-name>



Docker Setup (Optional but Recommended)

Build the Docker image

bash
docker build -t task-manager-app .
Run the container locally

bash
docker run -p 5000:5000 task-manager-app
Access at http://localhost:5000

Update config.py to contain the following -
SECRET_KEY=your-local-secret-key
SQLALCHEMY_DATABASE_URI=sqlite:///site.db
FLASK_ENV=development
WTF_CSRF_ENABLED=False




Running Database Migrations in Docker

To run database migrations inside the running container, first find the container ID:

bash
docker ps
Then run:

bash
docker exec -it <container_id> flask db upgrade



Deployment on Heroku
With Docker

Login to Heroku

bash
heroku login
heroku container:login
Build and push Docker image

bash
docker build -t registry.heroku.com/<your-app-name>/web .
docker push registry.heroku.com/<your-app-name>/web
Release the container

bash
heroku container:release web --app <your-app-name>
Set environment variables

bash
heroku config:set SECRET_KEY=<your-secret-key> --app <your-app-name>
heroku config:set FLASK_ENV=production --app <your-app-name>
Open the app

bash
heroku open --app <your-app-name>





Using the Application:

1. Registration and Login

New users can sign up through the registration page.

Use your credentials to log in to access task management features.

Admin users have elvated permissions.

2. Task Management

Regular users can -

CRU tasks, the following fields are required - Title, Description, Hours Allocated, Assigned To, Status, Hours Remaining and Project

Filter tasks by the following fields - 'Assigned To', 'Project'

Admin users can -

CRUD Tasks 

CRUD Projects 

Manage Users Security Roles

3. Project Management

CRU projects, the following fields are required - Name, Start Date, End Date 

Filter projects by the following fields - project name, status 

Admin users can -

CRUD Projects 

Manage Users Security Roles

Manage Users Security Roles

4. Notifications

Confirmation messages appear for successful and unsuccessful actions like task creation, updates, and deletions.

5 Error Handling

Validation ensures correct data entry, such as preventing empty task titles and ensuring project end dates are later than project start dates.

6.Security

Passwords are hashed securely.

CSRF protection enforced on forms.

Secure cookies and session management.





Testing

Tests written with unittest and pytest.

Code coverage measured with coverage.py.

Run all tests with:

bash
pytest --cov=webapp tests/

OR 
powershell
coverage run -m pytest tests/



CI/CD Pipeline:

Linting - flake8 for code style enforcement.

Testing - Automated test runs with coverage reports.

Security Scanning - Bandit for static security checks.

Deployment - Fully automated Docker build and Heroku deploy via GitHub Actions on push.




Troubleshooting:

App Fails to Start Locally -

Ensure all dependencies are installed with pip install < requirements.txt.

Check that the virtual environment is activated.

Database Issues -

Ensure migrations are applied: flask db migrate and flask db upgrade.

Deployment Errors on Heroku -

Verify that the Procfile and requirements.txt include necessary configurations.

Check Heroku logs for errors using heroku logs --tail.

Cannot Log In -

Ensure you have registered your account.
Verify your credentials are correct.

Records Not Saving - 
Check that all fields are completed correctly.
Ensure your internet connection is stable.

Access Denied for Admin Features - 
Verify you are logged in as an admin user.

CSRF Toke Missing Error -
Set SECRET_KEY in Heroku and local env correctly



Acknowledgements:

Flask Documentation - https://flask.palletsprojects.com/

Heroku - https://devcenter.heroku.com/

GitHub Actions Docs - https://docs.github.com/en/actions

Flask-WTF - https://flask-wtf.readthedocs.io/en/1.2.x/

Bandit Security Scanner - https://bandit.readthedocs.io/en/latest/

