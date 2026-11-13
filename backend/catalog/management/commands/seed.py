from django.core.management.base import BaseCommand

from catalog.models import (
    Category, ColorSeason, FaceShape, PaletteColor, SkinTone, SkinType, Undertone,
)

FACE_SHAPES = [
    'Diamond',
    'Heart',
    'Round',
    'Oval',
    'Square',
    'Triangle',
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
    'Sensitive',
    ]

# Product types.
CATEGORIES = [
    'Primer',
    'Foundation',
    'Concealer',
    'Powder',
    'Blush',
    'Bronzer',
    'Contour',
    'Highlighter',
    'Eyeshadow',
    'Eyeliner',
    'Mascara',
    'Brows',
    'Lipstick',
    'Lip Gloss',
    'Setting Spray',
    ]

# Undertone -> jewelry that suits it.
UNDERTONES = {
    'Warm': 'Gold, rose gold, copper',
    'Cool': 'Silver, platinum, white gold',
    'Neutral': 'Gold or silver',
    'Olive': 'Gold, antique brass',
    }

# Season -> use -> colors (name, hex code). Starter guide: edit it in the
# admin panel under "Color seasons".
PALETTES = {
    'Spring': {
        'clothing': [('Coral', '#FF7F50'), ('Warm Peach', '#FFCBA4'), ('Fresh Green', '#7BC47F'), ('Aqua', '#5FC9C1')],
        'blush': [('Peach', '#FFB07C'), ('Coral Pink', '#F88379')],
        'contour': [('Light Golden Bronze', '#C9925B')],
        'eyeshadow': [('Champagne', '#F7E7CE'), ('Golden Brown', '#996515'), ('Soft Teal', '#5F9EA0')],
        'jewelry': [('Yellow Gold', '#E6BE5A'), ('Rose Gold', '#D9A6A0')],
    },
    'Summer': {
        'clothing': [('Dusty Rose', '#C9A0A0'), ('Lavender', '#B4A7D6'), ('Powder Blue', '#A7C7E7'), ('Soft Navy', '#3B4A6B')],
        'blush': [('Soft Rose', '#E8ADAA'), ('Cool Pink', '#E7A1B0')],
        'contour': [('Cool Taupe', '#8B7E74')],
        'eyeshadow': [('Mauve', '#B784A7'), ('Slate Grey', '#708090'), ('Soft Plum', '#8E6C8A')],
        'jewelry': [('Silver', '#C0C0C0'), ('White Gold', '#E8E6E1')],
    },
    'Autumn': {
        'clothing': [('Olive', '#708238'), ('Rust', '#B7410E'), ('Mustard', '#D4A017'), ('Chocolate', '#5C3A21')],
        'blush': [('Terracotta', '#C8674B'), ('Warm Peach', '#F1A27D')],
        'contour': [('Warm Bronze', '#8C5A2B')],
        'eyeshadow': [('Copper', '#B87333'), ('Moss', '#6B7B3A'), ('Chocolate', '#5C3A21')],
        'jewelry': [('Gold', '#D4AF37'), ('Brass', '#B5A642')],
    },
    'Winter': {
        'clothing': [('True Red', '#C8102E'), ('Emerald', '#046307'), ('Royal Blue', '#1F3FBF'), ('Black', '#000000')],
        'blush': [('Berry', '#A23B6B'), ('Cool Rose', '#D4718F')],
        'contour': [('Cool Deep Taupe', '#6B5B53')],
        'eyeshadow': [('Charcoal', '#36454F'), ('Deep Plum', '#5B2A56'), ('Icy Silver', '#D5DCE2')],
        'jewelry': [('Silver', '#C0C0C0'), ('Platinum', '#E5E4E2')],
    },
    }


class Command(BaseCommand):
    help = 'Fill the starter lists (tags, product types, undertones, color seasons). Safe to run more than once.'

    def handle(self, *args, **options):
        simple_lists = [
            (FaceShape, FACE_SHAPES),
            (SkinTone, SKIN_TONES),
            (SkinType, SKIN_TYPES),
            (Category, CATEGORIES),
        ]
        for model, names in simple_lists:
            for name in names:
                model.objects.get_or_create(name=name)

        for name, jewelry in UNDERTONES.items():
            Undertone.objects.get_or_create(name=name, defaults={'jewelry': jewelry})

        for season_name, uses in PALETTES.items():
            season, _ = ColorSeason.objects.get_or_create(name=season_name)
            for use, colors in uses.items():
                for color_name, hex_code in colors:
                    PaletteColor.objects.get_or_create(
                        season=season, use=use, name=color_name, defaults={'hex': hex_code},
                    )

        for model in [FaceShape, SkinTone, SkinType, Category, Undertone, ColorSeason, PaletteColor]:
            self.stdout.write(f'{model.__name__}: {model.objects.count()} rows')
        self.stdout.write(self.style.SUCCESS('Seeded database!'))
