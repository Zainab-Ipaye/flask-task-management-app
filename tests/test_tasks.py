import unittest
from webapp import create_app, db, bcrypt
from webapp.models import User, Task
from datetime import datetime


class TaskTests(unittest.TestCase):
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

        from webapp.models import Project

        self.project = Project(
            name="Project 1",
            description="Test project",
            start_date=datetime.today(),
            end_date=datetime.today(),
            status="Not Started",
        )
        db.session.add(self.project)
        db.session.commit()

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

    def test_create_task_form(self):
        self.login_as(self.user)
        response = self.client.get("/tasks/create", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertIn("Task Title", html)
        self.assertIn('name="title"', html)
        self.assertIn("Description", html)
        self.assertIn('name="description"', html)
        self.assertIn("Hours Allocated", html)
        self.assertIn('name="hours_allocated"', html)
        self.assertIn("Assigned To", html)
        self.assertIn('name="assigned_to"', html)
        self.assertIn("Status", html)
        self.assertIn('name="status"', html)
        self.assertIn("Hours Remaining", html)
        self.assertIn('name="hours_remaining"', html)
        self.assertIn("Project", html)
        self.assertIn('name="project_id"', html)

    def test_edit_task_form(self):
        self.login_as(self.user)

        with self.app_context:
            task = Task(
                title="Sample Task",
                description="A sample description",
                hours_allocated=6,
                status="In Progress",
                assigned_to=self.user.id,
                project_id=self.project.id,
                hours_remaining=6,
                created_by=self.user.id,
            )
            db.session.add(task)
            db.session.commit()

        response = self.client.get(f"/task/{task.id}/edit", follow_redirects=True)
        html = response.get_data(as_text=True).lower()

        self.assertIn("task title", html)
        self.assertIn('value="sample task"', html)
        self.assertIn("description", html)
        self.assertIn("a sample description", html)
        self.assertIn("hours allocated", html)
        self.assertIn('value="6"', html)
        self.assertIn("assigned to", html)
        self.assertIn(f'value="{self.user.id}"', html)
        self.assertIn("status", html)
        self.assertIn('value="in progress"', html)
        self.assertIn("hours remaining", html)
        self.assertIn('value="6"', html)
        self.assertIn("project", html)
        self.assertIn(f'value="{self.project.id}"', html)

    def test_delete_task_confirmation_present(self):
        self.login_as(self.admin)

        with self.app_context:
            task = Task(
                title="Sample Task",
                description="A sample description",
                hours_allocated=6,
                status="In Progress",
                assigned_to=self.user.id,
                project_id=self.project.id,
                hours_remaining=6,
                created_by=self.admin.id,
            )
            db.session.add(task)
            db.session.commit()

        response = self.client.get("/tasks", follow_redirects=True)
        html = response.get_data(as_text=True)

        self.assertIn('class="btn-delete"', html)
        self.assertIn(f'action="/task/{task.id}/delete"', html)
        self.assertIn('method="POST"', html)


if __name__ == "__main__":
    unittest.main()
