from rest_framework.test import APITestCase

from catalog.models import ColorSeason, FaceShape, SkinTone, SkinType, Undertone

from .models import User

PASSWORD = 'lipstick-shade-42'


class AuthTests(APITestCase):
    def setUp(self):
        self.tone = SkinTone.objects.create(name='Tan Dark')
        self.type = SkinType.objects.create(name='Dry')
        self.shape = FaceShape.objects.create(name='Heart')

    def register(self, username='bri', email='bri@example.com', **extra):
        answers = {'skinTone': self.tone.id, 'skinType': self.type.id, 'faceShape': self.shape.id}
        return self.client.post('/auth/register', {
            'username': username, 'email': email, 'password': PASSWORD, **answers, **extra,
        })

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

    def test_register_requires_the_three_questions(self):
        response = self.client.post('/auth/register', {
            'username': 'bri', 'email': 'bri@example.com', 'password': PASSWORD, 'skinTone': self.tone.id,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.data), {'skinType', 'faceShape'})
        self.assertFalse(User.objects.exists())
        self.assertEqual(self.register(skinTone=999).status_code, 400)

    def test_badge_next_to_username(self):
        self.register()
        user = User.objects.get(username='bri')
        self.assertEqual(user.badge, 'Tan Dark, Dry, Heart')
        self.assertEqual(user.badge_short, 'TD, D, H')
        self.assertEqual(User(username='admin').badge, '')

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
        data = self.client.get('/auth/account').data
        self.assertEqual(data['email'], 'bri@example.com')
        self.assertEqual(data['isAdmin'], False)
        self.assertEqual(data['badge'], 'Tan Dark, Dry, Heart')
        self.assertEqual(data['skinTone'], {'id': self.tone.id, 'name': 'Tan Dark'})

    def test_public_profile_shows_undertone_and_season_but_not_email(self):
        warm = Undertone.objects.create(name='Warm', jewelry='Gold')
        autumn = ColorSeason.objects.create(name='Autumn')
        self.register(undertone=warm.id, colorSeason=autumn.id)
        self.client.credentials()
        data = self.client.get('/auth/profile/bri').data
        self.assertEqual(data['badge'], 'Tan Dark, Dry, Heart')
        self.assertEqual(data['undertone'], {'id': warm.id, 'name': 'Warm', 'jewelry': 'Gold'})
        self.assertEqual(data['colorSeason'], {'id': autumn.id, 'name': 'Autumn'})
        self.assertNotIn('email', data)
        self.assertEqual(self.client.get('/auth/profile/nobody').status_code, 404)

    def test_edit_account_changes_password_and_profile(self):
        user = User.objects.create_user('bri', 'bri@example.com', PASSWORD, skin_tone=self.tone)
        oily = SkinType.objects.create(name='Oily')
        winter = ColorSeason.objects.create(name='Winter')
        self.login_as(user)
        response = self.client.patch(f'/auth/account/{user.id}/edit', {
            'password': 'new-mascara-99x', 'email': 'new@example.com',
            'skinType': oily.id, 'colorSeason': winter.id,
        })
        self.assertEqual(response.status_code, 200)
        user.refresh_from_db()
        self.assertTrue(user.check_password('new-mascara-99x'))
        self.assertEqual((user.email, user.skin_type, user.color_season, user.skin_tone), ('new@example.com', oily, winter, self.tone))

    def test_follow_and_unfollow(self):
        bri = User.objects.create_user('bri', 'bri@example.com', PASSWORD)
        mua = User.objects.create_user('mua', 'mua@example.com', PASSWORD)
        self.assertEqual(self.client.post('/auth/profile/mua/follow').status_code, 401)
        self.login_as(bri)
        self.assertEqual(self.client.post('/auth/profile/bri/follow').status_code, 400)

        followed = self.client.post('/auth/profile/mua/follow').data
        self.assertEqual((followed['followerCount'], followed['isFollowing']), (1, True))
        self.assertEqual(self.client.get('/auth/profile/bri').data['followingCount'], 1)
        self.assertFalse(mua.following.exists())  # following is one-way

        unfollowed = self.client.delete('/auth/profile/mua/follow').data
        self.assertEqual((unfollowed['followerCount'], unfollowed['isFollowing']), (0, False))

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
