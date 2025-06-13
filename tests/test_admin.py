import unittest
from webapp import create_app, db, bcrypt
from webapp.models import User



class AdminRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False,
            'SECRET_KEY': 'testkey'
        })
        print("CSRF enabled:", self.app.config['WTF_CSRF_ENABLED']) 

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.drop_all()
        db.create_all()

        self.client = self.app.test_client()
        self.register_accounts()  


    def register_accounts(self):
        hashed_admin_pw = bcrypt.generate_password_hash('AdminPass123!').decode('utf-8')
        hashed_user_pw = bcrypt.generate_password_hash('UserPass123!').decode('utf-8')


        admin = User(username='admin', email='admin@example.com', password=hashed_admin_pw, role='admin')
        user = User(username='user', email='user@example.com', password=hashed_user_pw, role='user')

        db.session.add(admin)
        db.session.add(user)
        db.session.commit()


    def login(self, email, password):
        #with self.client:
            response = self.client.post('/login', data={
                'email': email,
                'password': password,
                'submit': True  
            }, follow_redirects=True)

            print("Login response status:", response.status_code)
            print(response.data.decode())
            self.assertIn(b'Task', response.data)
            return response


    def test_non_admin_cannot_access_admin_users(self):
        with self.client:
            self.login('user@example.com', 'UserPass123!')
            response = self.client.get('/admin/users', follow_redirects=True)
            print("Response after unauthorized access:", response.data.decode())
            self.assertIn( 'Unauthorized', response.get_data(as_text=True))

    def test_admin_can_access_admin_users(self):
        with self.client :

            self.login('admin@example.com', 'AdminPass123!')      
            with self.app.app_context():
                admin_user = User.query.filter_by(email='admin@example.com').first()
                if admin_user:
                    admin_user.role = 'Admin'
                    db.session.commit()     
            response = self.client.get('/admin/users', follow_redirects=True)
            print("Admin Users Page HTML:", response.data.decode())  
            self.assertIn('Update Role', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
