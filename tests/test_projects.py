import unittest
from datetime import datetime
from webapp import create_app, db, bcrypt
from webapp.models import User, Project
import re

class ProjectTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False,
            'SECRET_KEY': 'testkey'
        })

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

        self.client = self.app.test_client()
        self.register_accounts()

    def register_accounts(self):
        hashed_user_pw = bcrypt.generate_password_hash('UserPass123!').decode('utf-8')
        user = User(username='user', email='user@example.com', password=hashed_user_pw, role='user')
        db.session.add(user)
        db.session.commit()
        
  
    def login(self, client, email, password):
        response = client.post('/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

        # Debug output
        print("Login response HTML:\n", response.get_data(as_text=True))

        # Adjust this check to what your post-login page contains
        self.assertEqual(response.status_code, 200)
        self.assertIn('Create', response.get_data(as_text=True))  
        return response



    def test_create_project(self):
        with self.client as client:
            self.login(client, 'user@example.com', 'UserPass123!')

            response = client.post('/projects/create', data={
                'name': 'project 1',
                'description': 'this project is a test',
                'start_date': '2024-12-01',
                'end_date': '2025-09-01',
                'status': 'In Progress'
            }, follow_redirects=True)

            self.assertIn('Project created successfully!', response.get_data(as_text=True))

                
    def test_edit_project(self):
        with self.client as client:
            self.login(client, 'user@example.com', 'UserPass123!')

            start_date = datetime.strptime('2023-01-01', '%Y-%m-%d').date()
            end_date = datetime.strptime('2023-12-31', '%Y-%m-%d').date()

            with self.app_context:
                project = Project(
                    name='Original Project',
                    description='Original description',
                    start_date=start_date,
                    end_date=end_date,
                    status='Not Started'
                )
                db.session.add(project)
                db.session.commit()

            response = client.post(f'/project/{project.id}/edit', data={
                'name': 'Updated Project',
                'description': 'Updated description',
                'start_date': '2023-02-01',
                'end_date': '2023-11-30',
                'status': 'Completed'
            }, follow_redirects=True)

            self.assertIn('Project updated successfully!', response.get_data(as_text=True))

            updated_project = Project.query.get(project.id)
            self.assertEqual(updated_project.name, 'Updated Project')


    def test_delete_project(self):
        with self.client as client:
            self.login(client, 'user@example.com', 'UserPass123!')

            start_date = datetime.strptime('2022-12-12', '%Y-%m-%d').date()
            end_date = datetime.strptime('2024-12-12', '%Y-%m-%d').date()

            with self.app_context:
                project = Project(
                    name='My Project',
                    description='desc',
                    start_date=start_date,
                    end_date=end_date,
                    status='Active'
                )
                db.session.add(project)
                db.session.commit()

            response = client.post(f'/project/{project.id}/delete', follow_redirects=True)
            self.assertIn('Project has been deleted.', response.get_data(as_text=True))

            deleted = Project.query.get(project.id)
            self.assertIsNone(deleted)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
