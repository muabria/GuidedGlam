from django.conf import settings
from django.db import models


class NamedTag(models.Model):
    """Shared shape for the simple lookup tables below: just a unique name."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True
        ordering = ['id']

    def __str__(self):
        return self.name


# ---- What kind of product is it? -------------------------------------------

class Category(NamedTag):
    """Product type: Foundation, Concealer, Blush, ..."""

    class Meta(NamedTag.Meta):
        verbose_name_plural = 'categories'


# ---- Who is it for? (personal attributes) ----------------------------------
# The first three are the questions every user answers at sign-up.

class SkinTone(NamedTag):
    pass


class SkinType(NamedTag):
    pass


class FaceShape(NamedTag):
    pass


class Undertone(NamedTag):
    """Warm, Cool, Neutral... and the jewelry metals that suit it."""

    jewelry = models.CharField(max_length=200, blank=True, help_text='e.g. "Gold, rose gold"')


class ColorSeason(NamedTag):
    """Spring, Summer, Autumn, Winter. Its colors live in PaletteColor."""


class PaletteColor(models.Model):
    """One recommended color for a season, e.g. Autumn / Blush / Terracotta."""

    class Use(models.TextChoices):
        CLOTHING = 'clothing', 'Clothing'
        BLUSH = 'blush', 'Blush'
        CONTOUR = 'contour', 'Contour'
        EYESHADOW = 'eyeshadow', 'Eyeshadow'
        JEWELRY = 'jewelry', 'Jewelry'

    season = models.ForeignKey(ColorSeason, on_delete=models.CASCADE, related_name='palette')
    use = models.CharField(max_length=20, choices=Use.choices)
    name = models.CharField(max_length=100)
    hex = models.CharField(max_length=7, blank=True, help_text='Optional color code, e.g. #B7410E')

    class Meta:
        ordering = ['season_id', 'use', 'id']
        constraints = [
            models.UniqueConstraint(fields=['season', 'use', 'name'], name='unique_color_per_season_use'),
        ]

    def __str__(self):
        return f'{self.season} / {self.get_use_display()} / {self.name}'


# ---- Products ---------------------------------------------------------------

class MakeupProduct(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='products',
    )
    categories = models.ManyToManyField(Category, blank=True, related_name='products')
    face_shapes = models.ManyToManyField(FaceShape, blank=True, related_name='products')
    skin_tones = models.ManyToManyField(SkinTone, blank=True, related_name='products')
    skin_types = models.ManyToManyField(SkinType, blank=True, related_name='products')
    undertones = models.ManyToManyField(Undertone, blank=True, related_name='products')
    color_seasons = models.ManyToManyField(ColorSeason, blank=True, related_name='products')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
