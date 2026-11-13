from django.core.management.base import BaseCommand

from catalog.models import FaceShape, SkinTone, SkinType

FACE_SHAPES = [
    'Diamond', 
    'Heart', 
    'Round', 
    'Oval', 
    'Square', 
    'Triangle'
    ]

SKIN_TONES = [
    'Fair', 
    'Fair Light', 
    'Light', 
    'Light Medium', 
    'Medium', 
    'Medium Tan',
    'Tan', 
    'Tan Dark', 
    'Dark', 
    'Dark Deep', 
    'Deep',
    ]
SKIN_TYPES = [
    'Dry', 
    'Combo', 
    'Oily', 
    'Sensitive'
    ]


class Command(BaseCommand):
    help = 'Fill the face shape, skin tone and skin type tables. Safe to run more than once.'

    def handle(self, *args, **options):
        for model, names in [(FaceShape, FACE_SHAPES), (SkinTone, SKIN_TONES), (SkinType, SKIN_TYPES)]:
            for name in names:
                model.objects.get_or_create(name=name)
            self.stdout.write(f'{model.__name__}: {model.objects.count()} rows')
        self.stdout.write(self.style.SUCCESS('Seeded database!'))
