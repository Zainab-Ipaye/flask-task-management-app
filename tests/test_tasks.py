# tests/test_tasks.py
import unittest
from webapp import create_app, db, bcrypt
from webapp.models import User, Task
from webapp.audit import log_activity

class TaskTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False,
            'SECRET_KEY': 'testkey'
        })
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            hashed = bcrypt.generate_password_hash('pass1234').decode('utf-8')
            user = User(username='test', email='test@test.com', password=hashed, role='user')
            db.session.add(user)
            db.session.commit()

    def login(self):
        self.client.post('/login', data=dict(email='test@test.com', password='pass1234'), follow_redirects=True)

    def test_create_task(self):
        self.login()
        response = self.client.post('/tasks/create', data=dict(
            title='Test Task',
            description='This is a test task.'
        ), follow_redirects=True)
        self.assertIn(b'task has been created', response.data.lower())


    def test_log_activity_writes_to_file(tmp_path):
        log_file = tmp_path / "audit.log"
        log_activity("TEST_EVENT", "testuser", "success", log_path=log_file)
        assert log_file.read_text().startswith("[TEST_EVENT]")


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
