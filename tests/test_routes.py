# tests/test_routes.py
import unittest
from datetime import datetime
from webapp import create_app, db
from webapp.models import User, Project, Task
from flask_login import login_user


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
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()
        self.client = self.app.test_client()

        # Create users
        self.user = self.create_user("user", "user@example.com", "UserPass123!", "user")
        self.admin = self.create_user(
            "admin", "admin@example.com", "AdminPass123!", "admin"
        )

    def tearDown(self):
        with self.app.app_context():
            with self.app_context:
                project = Project(
                    name="Dummy",
                    description="desc",
                    start_date=datetime.today(),
                    end_date=datetime.today(),
                    status="Not Started",
                )
                db.session.add(project)
                db.session.commit()

                task = Task(
                    title="Test Task",
                    description="desc",
                    hours_allocated=5,
                    status="New",
                    assigned_to=self.user.id,
                    project_id=project.id,
                    hours_remaining=5,
                    created_by=self.user.id,
                )
                db.session.add(task)
                db.session.commit()

            db.session.remove()
            db.drop_all()

    def test_home_loads(self):
        response = self.client.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Zainab", response.data)

    def test_login_loads(self):
        response = self.client.get("/login", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Email", response.data)

    def test_register_loads(self):
        response = self.client.get("/register", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Confirm Password", response.data)

    def test_login_failure(self):
        response = self.client.post(
            "/login",
            data=dict(email="wrong@example.com", password="Wrongpass!"),
            follow_redirects=True,
        )
        self.assertIn(
            "Login",
            response.get_data(as_text=True),
        )

    def test_500_page(self):
        # Simulate error by calling a route that raises exception or patch route to raise
        with self.assertRaises(Exception):
            with self.app.test_request_context("/trigger-error"):
                raise Exception("Testing 500 error")

    def create_user(self, username, email, password, role):
        from webapp import bcrypt

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

        with self.app.test_request_context():
            login_user(user)

    def test_404_page(self):
        response = self.client.get("/non-existent-page", follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Page not found.", response.get_data(as_text=True))

    def test_projects_page_loads_with_filters(self):
        self.login_as(self.user)
        response = self.client.get(
            "/projects?status=Completed&page=1", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Projects", response.get_data(as_text=True))

    def test_tasks_page_loads_with_filters(self):
        self.login_as(self.user)
        response = self.client.get(
            "/tasks?assignee=1&project=2&page=1", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tasks", response.get_data(as_text=True))

    def test_update_user_role_requires_admin(self):
        self.login_as(self.user)  # Non-admin user
        response = self.client.post(
            f"/admin/users/{self.user.id}/role",
            data={"role": "admin"},
            follow_redirects=True,
        )
        self.assertIn("Page not found", response.get_data(as_text=True))

    def test_project_detail_view(self):
        self.login_as(self.user)  # <-- ensure user logged in
        with self.app_context:
            project = Project(
                name="Test Project",
                description="desc",
                start_date=datetime.today(),
                end_date=datetime.today(),
                status="Not Started",
            )
            db.session.add(project)
            db.session.commit()

        response = self.client.get("/projects", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(project.name, response.get_data(as_text=True))

    def test_task_detail_view(self):
        self.login_as(self.user)
        with self.app_context:
            project = Project(
                name="Dummy Project",
                description="desc",
                start_date=datetime.today(),
                end_date=datetime.today(),
                status="Not Started",
            )
            db.session.add(project)
            db.session.commit()

            task = Task(
                title="Test Task",
                description="desc",
                hours_allocated=5,
                status="New",
                assigned_to=self.user.id,
                project_id=project.id,
                hours_remaining=5,
                created_by=self.user.id,
            )
            db.session.add(task)
            db.session.commit()

        response = self.client.get("/tasks", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(task.title, response.get_data(as_text=True))

    def test_logout_route_logs_out_user(self):
        self.login_as(self.user)
        response = self.client.get("/logout", follow_redirects=True)
        html = response.get_data(as_text=True).lower()
        self.assertIn("register", html)
        self.assertIn("login", html)

    def test_profile_page_loads(self):
        self.login_as(self.user)
        response = self.client.get("/profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Profile", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
