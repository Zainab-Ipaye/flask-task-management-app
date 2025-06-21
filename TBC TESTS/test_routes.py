# tests/test_routes.py
import unittest
from webapp import create_app, db, bcrypt
from webapp.models import User
from webapp.forms import RegistrationForm


class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,
                "SECRET_KEY": "testkey",
            }
        )
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            password = bcrypt.generate_password_hash("Password123!").decode("utf-8")
            user = User(
                username="testuser",
                email="test@example.com",
                password=password,
                role="user",
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_home_loads(self):
        response = self.client.get("/", follow_redirects=True)
        # self.assertEqual(response.status_code, 200)
        self.assertIn(b"Zainab", response.data)

    def test_login_loads(self):
        response = self.client.get("/login", follow_redirects=True)
        # self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email", response.data)

    def test_register_loads(self):
        response = self.client.get("/register", follow_redirects=True)
        # self.assertEqual(response.status_code, 200)
        self.assertIn(b"Confirm Password", response.data)

    def test_register_login_logout_flow(self):
        response = self.client.post(
            "/register",
            data=dict(
                username="demo",
                email="demo@example.com",
                password="Password123!",
                confirm_password="Password123!",
                role="user",
            ),
            follow_redirects=True,
        )
        self.assertIn(
            b"your account has been created", response.get_data(as_text=True).lower()
        )

        response = self.client.post(
            "/login",
            data=dict(email="demo@example.com", password="Password123!"),
            follow_redirects=True,
        )
        self.assertIn(b"welcome", response.get_data(as_text=True).lower())

        response = self.client.get("/logout", follow_redirects=True)
        self.assertIn(b"logged out", response.get_data(as_text=True).lower())

    def test_login_failure(self):
        response = self.client.post(
            "/login",
            data=dict(email="wrong@example.com", password="Wrongpass!"),
            follow_redirects=True,
        )
        self.assertIn(
            b"Login failed. Check email and/or password.",
            response.get_data(as_text=True).lower(),
        )

    def test_invalid_register_shows_errors(self):
        response = self.client.post(
            "/register",
            data=dict(
                username="",  # invalid
                email="bademail",
                password="short",
                confirm_password="mismatch",
                role="user",
            ),
            follow_redirects=True,
        )
        self.assertIn(b"Username is required", response.get_data(as_text=True))
