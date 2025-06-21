# Rewriting test_tasks.py with fixes for date handling and log_activity usage
from datetime import date

import unittest
from webapp import create_app, db, bcrypt
from webapp.models import User, Project
from webapp.audit import log_activity
import os


class TaskTests(unittest.TestCase):
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
            hashed = bcrypt.generate_password_hash("pass1234").decode("utf-8")
            user = User(
                username="test", email="test@test.com", password=hashed, role="user"
            )
            db.session.add(user)

            project = Project(
                name="Test Project",
                description="desc",
                start_date=date(2024, 1, 1),
                end_date=date(2024, 12, 31),
                status="Active",
            )
            db.session.add(project)
            db.session.commit()

    from flask_login import login_user

    def test_create_task(self):
        with self.app.app_context():
            user = User.query.filter_by(email="test@test.com").first()

            # Bypass login by manually logging in the user
            @self.app.login_manager.request_loader
            def load_user_from_request(request):
                return user

            with self.client as client:
                with client.session_transaction() as sess:
                    sess["_user_id"] = str(user.id)

                project = Project.query.first()

                response = client.post(
                    "/tasks/create",
                    data=dict(
                        title="Test Task",
                        description="This is a test task.",
                        hours_allocated="5",
                        status="In Progress",
                        hours_remaining="5",
                        assigned_to=user.id,
                        project_id=project.id,
                    ),
                    follow_redirects=True,
                )

                print("CREATE TASK RESPONSE:\n", response.get_data(as_text=True))
                self.assertIn(b"your task has been created", response.data.lower())

    def test_log_activity_writes_to_file(self):
        log_file = "audit.log"
        if os.path.exists(log_file):
            os.remove(log_file)

        try:
            log_activity("TEST_EVENT")
        except Exception as e:
            print("Log activity failed:", e)

        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r") as f:
            contents = f.read()
            self.assertIn("[TEST_EVENT]", contents)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
