# Flask Task Management App

A task and project management web app built with Flask, featuring user authentication, role-based access control, and Dockerized deployment with Heroku and JawsDB.

## Features

- User registration and login (all new users default to `user` role)
- Admin user created automatically from environment variables
- Create, update, delete projects and tasks
- Assign tasks to users
- Pagination and filtering on lists
- Role-based access control (admin vs user)
- Secure password hashing with bcrypt
- CSRF protection and security headers (Flask-Talisman)
- Dockerized for local and Heroku deployment
- Automated tests with coverage reports
- CI/CD pipeline with linting, tests, security scanning, and deploy

## Setup & Run Locally

### 1. Clone the repository

bash
git clone https://github.com/Zainab-Ipaye/flask-task-management-app.git
cd flask-task-management-app

### 2. Create and activate a virtual environment (optional but recommended)

bash
python -m venv venv

For Windows
venv\Scripts\activate

For macOS/Linux
source venv/bin/activate

### 3. Install Dependencies

bash
pip install -r requirements.txt

### 4. Set environment variables

Create a .env file in the root directory with your admin user credentials:

Copy
ADMIN_USERNAME=admin
ADMIN_EMAIL=adminemail@test.com
ADMIN_PASSWORD=AdminPassworTest1!
SECRET_KEY=your-secret-key
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///site.db

!! Important: Do not commit your .env file to version control !!

### 5. Initialize the database

bash
flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade

### 6. Run the app

bash
flask --app run.py run

## Docker Local Setup

### Build and run

bash
docker build -t flask-task-management-app .
docker run -p 5000:5000 --env-file .env flask-task-management-app

### Running Database Migrations in Docker

To run database migrations inside the running container, first find the container ID:
bash
docker ps

bash
docker exec -it <container_id> flask db upgrade

Open http://localhost:5000 in your browser.

## Heroku Deployment with JawsDB

### 1. Create Heroku app

bash
heroku create your-app-name

### 2. Add JawsDB MySQL addon

bash
heroku addons:create jawsdb:kitefin --app your-app-name

### 3. Set config vars

heroku config:set SQLALCHEMY_DATABASE_URI=$(heroku config:get JAWSDB_URL --app your-app-name) --app your-app-name
heroku config:set ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=AdminPassword123! SECRET_KEY=your-development-secret-key FLASK_ENV=development --app your-app-name

### 4. Build and push Docker image

bash
docker build -t registry.heroku.com/your-app-name/web .
docker push registry.heroku.com/your-app-name/web
heroku container:release web --app your-app-name

### 5. Run database migrations on heroku

bash
heroku run flask db upgrade --app your-app-name

### 6. Open your deployed app

heroku open --app your-app-name

## Running Tests

bash
powershell
coverage run -m pytest tests/

## CI/CD Pipeline

Linting - flake8 for code style enforcement.

Testing - Automated test runs with coverage reports.

Security Scanning - Bandit for static security checks.

Deployment - Fully automated Docker build and Heroku deploy via GitHub Actions on push.

## Important Notes

User registration does not allow selecting roles; all new users are assigned the user role by default.

The admin user is created automatically from environment variables if none exists.

Always keep .env and secrets out of version control.

Run database migrations whenever you change models or deploy to a new environment.

## Troubleshooting 


### App Fails to Start Locally -

Ensure all dependencies are installed with pip install < requirements.txt.

Check that the virtual environment is activated.

### Database Issues -

Ensure migrations are applied: flask db migrate and flask db upgrade.

### Deployment Errors on Heroku -

Verify that the Procfile and requirements.txt include necessary configurations.

Check Heroku logs for errors using heroku logs --tail.

### Cannot Log In -

Ensure you have registered your account.
Verify your credentials are correct.

### Records Not Saving - 
Check that all fields are completed correctly.
Ensure your internet connection is stable.

### Access Denied for Admin Features - 
Verify you are logged in as an admin user.

### CSRF Toke Missing Error -
Set SECRET_KEY in Heroku and local env correctly

## Acknowledgements:

Flask Documentation - https://flask.palletsprojects.com/

Heroku - https://devcenter.heroku.com/

GitHub Actions Docs - https://docs.github.com/en/actions

Flask-WTF - https://flask-wtf.readthedocs.io/en/1.2.x/

Bandit Security Scanner - https://bandit.readthedocs.io/en/latest/