import unittest
from webapp import create_app
from webapp.forms import RegistrationForm, ProjectForm, TaskForm, LoginForm


class FormValidationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "WTF_CSRF_ENABLED": False,
                "SECRET_KEY": "testkey",
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_valid_form(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "newuser",
                    "email": "newuser@example.com",
                    "password": "Testpass123!",
                    "confirm_password": " ",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn("Please confirm your password.", form.confirm_password.errors)

    def test_valid_registration_form(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "validuser",
                    "email": "valid@example.com",
                    "password": "StrongPass123!",
                    "confirm_password": "StrongPass123!",
                    #"role": "user",
                }
            )
            self.assertTrue(form.validate())

    def test_login_form(self):
        with self.app.test_request_context():
            form = LoginForm(
                data={"email": "valid@example.com", "password": "StrongPass123!"}
            )
            self.assertTrue(form.validate())

    def test_invalid_email_format(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user4",
                    "email": "not-an-email",
                    "password": "Pass123!",
                    "confirm_password": "Pass123!",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn("Invalid email address.", form.email.errors)

    def test_project_start_after_end(self):
        with self.app.test_request_context():
            form = ProjectForm(
                data={
                    "name": "Test Project",
                    "description": "Logic check",
                    "start_date": "2025-12-01",
                    "end_date": "2025-01-01",
                    "status": "In Progress",
                }
            )
            self.assertFalse(form.validate())

    def test_task_form_missing_title(self):
        with self.app.test_request_context():
            form = TaskForm()

            form.status.choices = [
                ("New", "New"),
                ("In Progress", "In Progress"),
                ("Completed", "Completed"),
                ("Removed", "Removed"),
            ]

            form.project_id.choices = [("1", "Project 1"), ("2", "Project 2")]
            form.assigned_to.choices = [("1", "Tester"), ("2", "Developer")]

            form.process(
                data={
                    "title": "",
                    "description": "Do something",
                    "hours_allocated": "6",
                    "status": "New",
                    "assigned_to": "1",
                    "project_id": "1",
                    "hours_remaining": "6",
                }
            )

            self.assertFalse(form.validate())
            self.assertIn("Title is required", form.title.errors)

    def test_password_mismatch(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "pass1",
                    "confirm_password": "pass2",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn("Password must match", form.confirm_password.errors)

    def test_password_length(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "pass1",
                    "confirm_password": "pass1",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must be at least 8 characters long.", form.password.errors
            )

    def test_password_specialcharacter(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "pass10111",
                    "confirm_password": "pass10111",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must contain at least one upper case letter.",
                form.password.errors,
            )

    def test_password_missing_number(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "Passwords",
                    "confirm_password": "Passwords",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must contain at least 1 number.", form.password.errors
            )

    def test_password_upper_case(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user2",
                    "email": "user2@example.com",
                    "password": "Passwords1",
                    "confirm_password": "Passwords1",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn(
                "Password must contain at least one special character.",
                form.password.errors,
            )

    def test_missing_email(self):
        with self.app.test_request_context():
            form = RegistrationForm(
                data={
                    "username": "user3",
                    "email": "",
                    "password": "pass",
                    "confirm_password": "pass",
                    #"role": "user",
                }
            )
            self.assertFalse(form.validate())
            self.assertIn("Email is required", form.email.errors)

    def test_missing_projectname(self):
        with self.app.test_request_context():
            form = ProjectForm(
                data={
                    "name": "",
                    "description": "this project is a test",
                    "start_date": "2024-12-01",
                    "end_date": "2025-9-01",
                    "status": "In Progress",
                }
            )
            print(form.name.errors)

            self.assertFalse(form.validate())
            self.assertIn("Name is required", form.name.errors)
