import unittest
from datetime import datetime
from flask_login import login_user
from webapp import create_app, db, bcrypt
from webapp.models import User, Project


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
                "WTF_CSRF_ENABLED": False,
                "SECRET_KEY": "testkey",
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

        self.user = self.create_user("user", "user@example.com", "UserPass123!", "user")
        self.admin = self.create_user(
            "admin", "admin@example.com", "AdminPass123!", "admin"
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_user(self, username, email, password, role):
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(username=username, email=email, password=hashed_pw, role=role)
        db.session.add(user)
        db.session.commit()
        return user

    def login_as(self, user):
        with self.app.test_request_context():
            login_user(user)
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

    def test_create_project(self):
        self.login_as(self.user)
        response = self.client.get(
            "/projects/create",
            data={
                "name": "Project 1",
                "description": "This project is a test",
                "start_date": "01-06-2024",
                "end_date": "01-09-2024",
                "status": "In Progress",
            },
            follow_redirects=True,
        )
        self.assertIn("Project created successfully!", response.get_data(as_text=True))

    def test_edit_project(self):
        self.login_as(self.user)

        with self.app_context:
            project = Project(
                name="Original Project",
                description="Original description",
                start_date=datetime(2023, 1, 1),
                end_date=datetime(2023, 12, 31),
                status="Not Started",
            )
            db.session.add(project)
            db.session.commit()

        response = self.client.post(
            f"/project/{project.id}/edit",
            data={
                "name": "Updated Project",
                "description": "Updated description",
                "start_date": "2023-02-01",
                "end_date": "2023-11-30",
                "status": "In Progress",
                "submit": "Update",
            },
            follow_redirects=True,
        )

        self.assertIn("Project updated successfully!", response.get_data(as_text=True))

        with self.app_context:
            updated_project = db.session.get(Project, project.id)
            self.assertEqual(updated_project.name, "Updated Project")

    def test_delete_project(self):
        self.login_as(self.admin)

        with self.app_context:
            project = Project(
                name="My Project",
                description="desc",
                start_date=datetime(2022, 12, 12),
                end_date=datetime(2024, 12, 12),
                status="Completed",
            )
            db.session.add(project)
            db.session.commit()

        response = self.client.post(
            f"/project/{project.id}/delete", follow_redirects=True
        )
        self.assertIn("Project has been deleted.", response.get_data(as_text=True))

        with self.app_context:
            deleted = db.session.get(Project, project.id)
            self.assertIsNone(deleted)


if __name__ == "__main__":
    unittest.main()
