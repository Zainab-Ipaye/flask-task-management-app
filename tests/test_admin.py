import unittest
from flask import session
from webapp import create_app, db, bcrypt
from webapp.models import User

class AdminRouteTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'WTF_CSRF_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SECRET_KEY': 'test_secret_key'
        })

        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()
        self.admin = self.create_user('admin', 'admin@example.com', 'AdminPass123!', 'admin')
        self.user = self.create_user('user', 'user@example.com', 'UserPass123!', 'user')

    def create_user(self, username, email, password, role):
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def login_as(self, user):
        """Simulate a logged-in user by setting the session manually."""
        with self.client.session_transaction() as sess:
            sess['_user_id'] = str(user.id)
            sess['_fresh'] = True

    def test_admin_can_access_admin_users(self):
        self.login_as(self.admin)
        response = self.client.get('/admin/users', follow_redirects=True)
        print("Admin redirected response:", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'update role', response.data.lower())


    def test_user_cannot_access_admin_users(self):
        self.login_as(self.user)
        response = self.client.get('/admin/users', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'you do not have permission', response.data.lower())

    def test_bypass_login_logic_still_blocks_unauthorized(self):
        """Ensure no session = no access"""
        response = self.client.get('/admin/users', follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'unauthorized', response.data.lower())


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

if __name__ == '__main__':
    unittest.main()