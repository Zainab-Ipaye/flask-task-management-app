import unittest
from webapp import create_app
from webapp.forms import RegistrationForm, ProjectForm, TaskForm


class FormValidationTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,  # Optional if disabling CSRF
            'SECRET_KEY': 'testkey'
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_valid_form(self):
        with self.app.test_request_context():
            form = RegistrationForm(data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password': 'Testpass123!',
                'confirm_password': 'Testpass123!',
                'role': ' '
            })
            self.assertFalse(form.validate())
            self.assertIn('Role is required', form.role.errors)


    def test_password_mismatch(self):
        with self.app.test_request_context():
            form = RegistrationForm(data={
                'username': 'user2',
                'email': 'user2@example.com',
                'password': 'pass1',
                'confirm_password': 'pass2',
                'role': 'user'
            })
            self.assertFalse(form.validate())
            self.assertIn('Password must match', form.confirm_password.errors)

    def test_missing_email(self):
        with self.app.test_request_context():
            form = RegistrationForm(data={
                'username': 'user3',
                'email': '',
                'password': 'pass',
                'confirm_password': 'pass',
                'role': 'user'
            })
            self.assertFalse(form.validate())
            self.assertIn('Email is required', form.email.errors)

    def test_missing_projectname(self):
        with self.app.test_request_context():
            form = ProjectForm(data={
                'name': '',
                'description': 'this project is a test',
                'start_date': '2024-12-01',
                'end_date': '2025-9-01',
                'status':'In Progress'
            })
            print(form.name.errors)

            self.assertFalse(form.validate())
            self.assertIn('Name is required', form.name.errors)
     