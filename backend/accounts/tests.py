from rest_framework.test import APITestCase

from .models import User

PASSWORD = 'lipstick-shade-42'


class AuthTests(APITestCase):
    def register(self, username='bri', email='bri@example.com'):
        return self.client.post('/auth/register', {'username': username, 'email': email, 'password': PASSWORD})

    def login_as(self, user):
        token = self.client.post('/auth/login', {'username': user.username, 'password': PASSWORD}).data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_register_hashes_password_and_returns_token(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        user = User.objects.get(username='bri')
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))

    def test_register_rejects_duplicate_email(self):
        self.register()
        self.assertEqual(self.register(username='other').status_code, 400)

    def test_login_errors(self):
        self.register()
        missing = self.client.post('/auth/login', {'username': 'nobody', 'password': PASSWORD})
        wrong = self.client.post('/auth/login', {'username': 'bri', 'password': 'nope'})
        self.assertEqual((missing.status_code, missing.data), (401, 'There is no user with that username.'))
        self.assertEqual((wrong.status_code, wrong.data), (401, 'Incorrect password.'))

    def test_account_requires_token(self):
        self.assertEqual(self.client.get('/auth/account').status_code, 401)
        token = self.register().data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/auth/account')
        self.assertEqual(response.data, {'id': response.data['id'], 'username': 'bri', 'email': 'bri@example.com', 'isAdmin': False})

    def test_edit_account_changes_password(self):
        user = User.objects.create_user('bri', 'bri@example.com', PASSWORD)
        self.login_as(user)
        response = self.client.patch(f'/auth/account/{user.id}/edit', {'password': 'new-mascara-99x', 'email': 'new@example.com'})
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password('new-mascara-99x'))
        self.assertEqual(user.email, 'new@example.com')

    def test_admin_routes(self):
        user = User.objects.create_user('bri', 'bri@example.com', PASSWORD)
        admin = User.objects.create_user('boss', 'boss@example.com', PASSWORD, is_staff=True)

        self.login_as(user)
        self.assertEqual(self.client.get('/auth/users').status_code, 403)
        self.assertEqual(self.client.delete(f'/auth/user/{admin.id}').status_code, 403)

        self.login_as(admin)
        self.assertEqual(len(self.client.get('/auth/users').data), 2)
        promoted = self.client.patch(f'/auth/admin/{user.id}', {'isAdmin': True}, format='json')
        self.assertTrue(promoted.data['isAdmin'])
        self.assertEqual(self.client.delete(f'/auth/user/{user.id}').status_code, 200)
        self.assertFalse(User.objects.filter(id=user.id).exists())
