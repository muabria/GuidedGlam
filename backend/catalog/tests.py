from django.core.management import call_command
from rest_framework.test import APITestCase

from accounts.models import User

from .models import (
    Category, ColorSeason, FaceShape, MakeupProduct, PaletteColor, SkinTone, SkinType, Undertone,
)


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

    def test_guide_tables_are_read_only(self):
        for path in ['category', 'undertone', 'colorseason', 'product']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(f'/api/{path}').status_code, 200)
                self.assertEqual(self.client.post(f'/api/{path}', {'name': 'x'}).status_code, 405)


class SeedAndGuideTests(APITestCase):
    def setUp(self):
        call_command('seed', verbosity=0)

    def test_seed_is_safe_to_run_twice(self):
        counts = lambda: [m.objects.count() for m in (FaceShape, SkinTone, SkinType, Category, Undertone, ColorSeason, PaletteColor)]
        before = counts()
        call_command('seed', verbosity=0)
        self.assertEqual(counts(), before)
        self.assertEqual(before[:6], [6, 11, 4, 15, 4, 4])

    def test_season_comes_with_its_color_guide(self):
        autumn = ColorSeason.objects.get(name='Autumn')
        data = self.client.get(f'/api/colorseason/{autumn.id}').data
        self.assertEqual(data['name'], 'Autumn')
        self.assertEqual({color['use'] for color in data['palette']}, {'clothing', 'blush', 'contour', 'eyeshadow', 'jewelry'})
        self.assertIn({'use': 'blush', 'name': 'Terracotta', 'hex': '#C8674B'}, data['palette'])

    def test_undertone_gives_jewelry(self):
        names = {u['name']: u['jewelry'] for u in self.client.get('/api/undertone').data}
        self.assertIn('Silver', names['Cool'])

    def test_product_filters_keep_product_type_and_personal_tags_separate(self):
        blush, foundation = Category.objects.get(name='Blush'), Category.objects.get(name='Foundation')
        oily, cool = SkinType.objects.get(name='Oily'), Undertone.objects.get(name='Cool')
        rosy = MakeupProduct.objects.create(name='Rosy blush', price='12.00')
        rosy.categories.add(blush); rosy.undertones.add(cool)
        matte = MakeupProduct.objects.create(name='Matte foundation', price='24.50')
        matte.categories.add(foundation); matte.skin_types.add(oily)

        names = lambda url: [p['name'] for p in self.client.get(url).data]
        self.assertEqual(names('/api/product'), ['Matte foundation', 'Rosy blush'])
        self.assertEqual(names(f'/api/product?category={blush.id}'), ['Rosy blush'])
        self.assertEqual(names(f'/api/product?category={blush.id}&undertone={cool.id}'), ['Rosy blush'])
        self.assertEqual(names(f'/api/product?category={blush.id}&skinType={oily.id}'), [])
        self.assertEqual(names('/api/product?search=matte'), ['Matte foundation'])
        self.assertEqual(names('/api/product?category=abc'), ['Matte foundation', 'Rosy blush'])
