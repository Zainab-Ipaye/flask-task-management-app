# tests/test_security.py
import unittest
from webapp import create_app

class SecurityTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app({'TESTING': True, 'WTF_CSRF_ENABLED': True})
        self.client = self.app.test_client()

    def test_csrf_protection_active(self):
        response = self.client.post('/login', data={
            'email': 'user@example.com',
            'password': 'pass'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'csrf', response.data.lower())

    def test_xss_protection(self):
        response = self.client.get('/?search=<script>alert(1)</script>')
        self.assertNotIn(b'<script>', response.data)

    def test_talisman_security_headers(self):
        with self.client as client:
            response = client.get('/')
            headers = response.headers

            assert 'Content-Security-Policy' in headers
            assert 'X-Frame-Options' in headers
            assert 'Strict-Transport-Security' in headers or 'X-Content-Type-Options' in headers


