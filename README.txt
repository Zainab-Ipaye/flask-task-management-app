Zainab's Task Management App: A Comprehensive Guide

Overview:

Zainab's Task Management App is a web task management application built using the Python language and the Flask framework. The web app was deployed to Heroku for user accessibility. It provides a smooth and user-friendly interface for users to manage their tasks and for administrators to oversee and control the system. This guide details the steps to set up, run, and use the application effectively.


Main Features:

User Registration/Authentication: Admin/User can log in securely

Task Management: CRUD (Create, Read, Update, Delete) operations for tasks for admins and CRU (Create, Read, Update) operations for users.

Admin Features: Manage users and oversee system activity.

Real-time Updates: All modifications are updated immediately and in real-time

Notifications: Users receive validations throughout the app after completing actions e.g., creating task, deleting a project


Setup Instructions:

Prerequisites -

Python installed on your machine.

Git for cloning the repository (compressed source code file is attached).

Heroku CLI for hosting - Follow the installation guide.


Steps to Set Up Locally:

Clone the Repository -

In your command prompt enter cd <nameoftheprojectfile>

Create a Virtual Environment - 

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

All dependencies can be found in the requirements.txt file which is included in the source code file.


Set Up the Database - 

Initialize the SQLite database:

flask --app run.py db init
flask --app run.py db migrate -m "Initial migration"
flask --app run.py db upgrade

Run the Application -

Run the 'run.py' file

Access the app at http://<localhost>:5000/.

Update MySQL Connection:

Create or log into Heroku

Create an app and fill out the requirements e.g., app name

Create a new add-on for JawsDB

A MySQL login will be assigned to your app name - this can be used to monitor data changes

Update the config.py file with the new MySQL login details provided by JawsDB


Deployment on Heroku:

Log into your Heroku Account via command prompt

Prepare the Application - add final touches and save files

Add a new file 'Procfile' containing:

web: gunicorn "webapp:create_app()"

Add Heroku-specific dependencies in requirements.txt if it's not already in there e.g., gunicorn


Deploy to Heroku by entering the following in command prompt:

heroku login (if you haven't already)
git add.
git commit -m "NameYourDeployment/migration"
git push heroku master

Access the Deployed App

Visit https://<your-app-name>.herokuapp.com/ in your browser.


Using the Application:

1. Registration and Login

New users can sign up through the registration page.

Use your credentials to log in to access task management features.

2. Task Management

Regular users can -

CRU tasks, the following fields are required - Title, Description, Hours Allocated, Assigned To, Status, Hours Remaining and Project

Filter tasks by the following fields - 'Assigned To', 'Project'

CRU projects, the following fields are required - Name, Start Date, End Date 

Admin users can -

CRUD Tasks - 

CRUD Projects - 

Manage Users Security Roles

3. Notifications

Confirmation messages appear for successful actions like task creation, updates, and deletions.

4. Error Handling

Validation ensures correct data entry, such as preventing empty task titles and ensuring project end dates are later than project start dates.



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


Acknowledgements

Flask Documentation for web framework access.

Heroku Documentation for deployment and hosting services.


