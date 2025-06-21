import unittest
from datetime import datetime
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
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

    def test_create_project(self):
        self.login_as(self.user)

        response = self.client.post(
            "/projects/create",
            data={
                "name": "Project 1",
                "description": "This project is a test",
                "start_date": "2024-12-01",
                "end_date": "2025-09-01",
                "status": "In Progress",
                "submit": "Create Project",
            },
            follow_redirects=True,
        )
        self.assertIn(
            "project created successfully!", response.get_data(as_text=True).lower()
        )

        # self.assertIn('Project created successfully!', response.get_data(as_text=True))

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

        self.assertIn(
            "project updated successfully!", response.get_data(as_text=True).lower()
        )
        updated_project = db.session.get(Project, project.id)
        self.assertEqual(updated_project.name, "Updated Project")

    def test_delete_project(self):
        self.login_as(self.admin)  # Only admin can delete

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
        self.assertIn(
            "project has been deleted.", response.get_data(as_text=True).lower()
        )
        deleted = db.session.get(Project, project.id)
        self.assertIsNone(deleted)
