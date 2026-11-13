from django.core.management import call_command
from rest_framework.test import APITestCase

from accounts.models import User

from .models import FaceShape, MakeupProduct, SkinTone, SkinType


class TagApiTests(APITestCase):
    def test_api_test_route(self):
        self.assertEqual(self.client.get('/api/test').data, {'message': 'API is working!'})

    def test_crud_for_each_tag(self):
        for path in ['faceshape', 'skintone', 'skintype']:
            with self.subTest(path=path):
                created = self.client.post(f'/api/{path}', {'name': 'Oval'})
                self.assertEqual(created.status_code, 201)
                pk = created.data['id']
                self.assertEqual(self.client.get(f'/api/{path}').data, [{'id': pk, 'name': 'Oval'}])
                self.assertEqual(self.client.get(f'/api/{path}/{pk}').data['name'], 'Oval')
                self.assertEqual(self.client.put(f'/api/{path}/{pk}', {'name': 'Round'}).data['name'], 'Round')
                self.assertEqual(self.client.patch(f'/api/{path}/{pk}', {'name': 'Heart'}).data['name'], 'Heart')
                self.assertEqual(self.client.get(f'/api/{path}/999').status_code, 404)
                self.assertEqual(self.client.post(f'/api/{path}', {'name': 'Heart'}).status_code, 400)

    def test_only_skintype_can_be_deleted_and_only_when_logged_in(self):
        shape = FaceShape.objects.create(name='Oval')
        skin_type = SkinType.objects.create(name='Dry')
        self.assertEqual(self.client.delete(f'/api/faceshape/{shape.id}').status_code, 405)
        self.assertEqual(self.client.delete(f'/api/skintype/{skin_type.id}').status_code, 401)

        self.client.force_authenticate(User.objects.create_user('bri', 'bri@example.com', 'pw'))
        self.assertEqual(self.client.delete(f'/api/skintype/{skin_type.id}').status_code, 204)
        self.assertFalse(SkinType.objects.exists())


class ModelTests(APITestCase):
    def test_product_links_and_seed(self):
        call_command('seed', verbosity=0)
        call_command('seed', verbosity=0)  # running twice must not duplicate
        self.assertEqual((FaceShape.objects.count(), SkinTone.objects.count(), SkinType.objects.count()), (6, 11, 4))

        product = MakeupProduct.objects.create(name='Matte foundation', price='24.50')
        product.skin_types.add(SkinType.objects.get(name='Oily'))
        self.assertEqual(SkinType.objects.get(name='Oily').products.get(), product)
