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
                "LOGIN_DISABLED": False,
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

        self.user_password = "UserPass123!"
        self.admin_password = "AdminPass123!"

        self.user = self.create_user(
            "user", "user@example.com", self.user_password, "user"
        )
        self.admin = self.create_user(
            "admin", "admin@example.com", self.admin_password, "admin"
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

    def test_create_project_form_renders(self):
        self.login_as(self.user)
        response = self.client.get("/projects/create", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertIn("Project Name", html)
        self.assertIn('name="name"', html)
        self.assertIn("Description", html)
        self.assertIn('name="description"', html)
        self.assertIn("Start Date", html)
        self.assertIn('name="start_date"', html)
        self.assertIn("End Date", html)
        self.assertIn('name="end_date"', html)
        self.assertIn("Status", html)
        self.assertIn('name="status"', html)

    def test_edit_project_form_renders_with_data(self):
        self.login_as(self.user)

        with self.app_context:
            project = Project(
                name="Sample Project",
                description="A sample description",
                start_date=datetime(2023, 1, 1),
                end_date=datetime(2023, 12, 31),
                status="Not Started",
            )
            db.session.add(project)
            db.session.commit()

        response = self.client.get(f"/project/{project.id}/edit", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertIn("Project Name", html)
        self.assertIn('value="Sample Project"', html)
        self.assertIn("Description", html)
        self.assertIn("A sample description", html)
        self.assertIn('value="2023-01-01"', html)
        self.assertIn('value="2023-12-31"', html)
        self.assertIn('name="status"', html)

    def test_delete_project_confirmation_present(self):
        self.login_as(self.admin)

        with self.app_context:
            project = Project(
                name="Delete Me",
                description="desc",
                start_date=datetime(2022, 12, 12),
                end_date=datetime(2024, 12, 12),
                status="Completed",
            )
            db.session.add(project)
            db.session.commit()

        response = self.client.get("/projects", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertIn('class=".btn-delete-project"', html)
        self.assertIn(f'action="/project/{project.id}/delete"', html)
        self.assertIn('method="POST"', html)


if __name__ == "__main__":
    unittest.main()
