import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from accounts.models import User
from catalog.models import Category, FaceShape, MakeupProduct, SkinTone, SkinType

from .models import Comment, Post

MEDIA = tempfile.mkdtemp()


def photo(name='look.png'):
    buffer = io.BytesIO()
    Image.new('RGB', (10, 10), 'pink').save(buffer, 'PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA)
class PostTests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        tan, dry, heart = SkinTone.objects.create(name='Tan'), SkinType.objects.create(name='Dry'), FaceShape.objects.create(name='Heart')
        self.oily = SkinType.objects.create(name='Oily')
        self.dry = dry
        self.bri = User.objects.create_user('muabria', 'bri@example.com', 'pw', skin_tone=tan, skin_type=dry, face_shape=heart)
        self.other = User.objects.create_user('other', 'other@example.com', 'pw', skin_tone=tan, skin_type=self.oily, face_shape=heart)

    def make_post(self, user, caption='My look', **extra):
        self.client.force_authenticate(user)
        return self.client.post('/api/post', {'caption': caption, 'images': [photo()], **extra}, format='multipart')

    def test_create_post_shows_author_badge_and_photos(self):
        response = self.make_post(self.bri, images=[photo('a.png'), photo('b.png')])
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(response.data['author'], {
            'id': self.bri.id, 'username': 'muabria', 'badge': 'Tan, Dry, Heart', 'badgeShort': 'T, D, H',
        })
        self.assertEqual(len(response.data['images']), 2)
        self.assertTrue(response.data['images'][0].startswith('/media/posts/'))
        saved_file = Post.objects.get().images.first().image
        self.assertTrue(saved_file.storage.exists(saved_file.name))

    def test_post_needs_login_and_a_photo(self):
        self.assertEqual(self.client.post('/api/post', {'caption': 'x', 'images': [photo()]}, format='multipart').status_code, 401)
        self.client.force_authenticate(self.bri)
        self.assertEqual(self.client.post('/api/post', {'caption': 'x'}, format='multipart').status_code, 400)
        not_a_photo = SimpleUploadedFile('x.png', b'hello', content_type='image/png')
        self.assertEqual(self.client.post('/api/post', {'images': [not_a_photo]}, format='multipart').status_code, 400)
        self.assertFalse(Post.objects.exists())

    def test_only_author_can_edit_or_delete(self):
        pk = self.make_post(self.bri).data['id']
        self.client.force_authenticate(self.other)
        self.assertEqual(self.client.patch(f'/api/post/{pk}', {'caption': 'hacked'}).status_code, 403)
        self.assertEqual(self.client.delete(f'/api/post/{pk}').status_code, 403)
        self.client.force_authenticate(self.bri)
        edited = self.client.patch(f'/api/post/{pk}', {'caption': 'Edited'})
        self.assertEqual((edited.status_code, edited.data['caption'], len(edited.data['images'])), (200, 'Edited', 1))
        self.assertEqual(self.client.delete(f'/api/post/{pk}').status_code, 204)

    def test_feed_filters(self):
        blush = Category.objects.create(name='Blush')
        product = MakeupProduct.objects.create(name='Rosy blush', price='12.00')
        product.categories.add(blush)
        self.make_post(self.bri, caption='Dry skin routine', productIds=[product.id])
        self.make_post(self.other, caption='Oily skin tips')
        self.client.force_authenticate(None)

        captions = lambda url: [p['caption'] for p in self.client.get(url).data]
        self.assertEqual(captions('/api/post'), ['Oily skin tips', 'Dry skin routine'])  # newest first
        self.assertEqual(captions(f'/api/post?skinType={self.dry.id}'), ['Dry skin routine'])
        self.assertEqual(captions('/api/post?author=other'), ['Oily skin tips'])
        self.assertEqual(captions(f'/api/post?category={blush.id}'), ['Dry skin routine'])
        self.assertEqual(captions(f'/api/post?product={product.id}'), ['Dry skin routine'])
        self.assertEqual(captions('/api/post?search=tips'), ['Oily skin tips'])
        self.assertEqual(captions('/api/post?following=true'), [])
        self.assertEqual(captions('/api/post?saved=true'), [])

        self.bri.following.add(self.other)
        self.client.force_authenticate(self.bri)
        self.assertEqual(captions('/api/post?following=true'), ['Oily skin tips'])

    def test_like_and_save(self):
        pk = self.make_post(self.bri).data['id']
        self.client.force_authenticate(None)
        self.assertEqual(self.client.post(f'/api/post/{pk}/like').status_code, 401)

        self.client.force_authenticate(self.other)
        self.client.post(f'/api/post/{pk}/like')
        liked = self.client.post(f'/api/post/{pk}/like').data  # liking twice still counts once
        self.assertEqual((liked['likeCount'], liked['liked'], liked['saved']), (1, True, False))
        self.client.post(f'/api/post/{pk}/save')
        self.assertEqual([p['id'] for p in self.client.get('/api/post?saved=true').data], [pk])
        unliked = self.client.delete(f'/api/post/{pk}/like').data
        self.assertEqual((unliked['likeCount'], unliked['liked'], unliked['saved']), (0, False, True))

        self.client.force_authenticate(self.bri)
        self.assertEqual(self.client.get(f'/api/post/{pk}').data['saved'], False)

    def test_comments(self):
        pk = self.make_post(self.bri).data['id']
        self.client.force_authenticate(None)
        self.assertEqual(self.client.post(f'/api/post/{pk}/comments', {'content': 'hi'}).status_code, 401)

        self.client.force_authenticate(self.other)
        created = self.client.post(f'/api/post/{pk}/comments', {'content': 'Love this!'})
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.data['user']['badge'], 'Tan, Oily, Heart')
        listed = self.client.get(f'/api/post/{pk}/comments').data
        self.assertEqual([c['content'] for c in listed], ['Love this!'])
        self.assertEqual(self.client.get(f'/api/post/{pk}').data['commentCount'], 1)

        stranger = User.objects.create_user('stranger', 's@example.com', 'pw')
        self.client.force_authenticate(stranger)
        self.assertEqual(self.client.delete(f'/api/comment/{created.data["id"]}').status_code, 403)
        self.client.force_authenticate(self.bri)  # post author can remove comments on their post
        self.assertEqual(self.client.delete(f'/api/comment/{created.data["id"]}').status_code, 204)
        self.assertFalse(Comment.objects.exists())
