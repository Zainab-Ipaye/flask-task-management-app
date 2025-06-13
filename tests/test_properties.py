# tests/test_properties.py
import unittest
from hypothesis import given, strategies as st
from webapp import create_app, db, bcrypt
from webapp.models import User

class PropertyTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    @given(st.text(min_size=5, max_size=30), st.emails())
    def test_user_registration_property(self, username, email):
        with self.app.app_context():
            password = bcrypt.generate_password_hash('Test123!').decode('utf-8')
            user = User(username=username, email=email, password=password, role='user')
            db.session.add(user)
            db.session.commit()
            self.assertIsNotNone(User.query.filter_by(email=email).first())

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
