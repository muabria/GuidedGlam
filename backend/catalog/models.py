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


class Category(NamedTag):
    class Meta(NamedTag.Meta):
        verbose_name_plural = 'categories'


class SkinTone(NamedTag):
    pass


class SkinType(NamedTag):
    pass


class FaceShape(NamedTag):
    pass


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

    def __str__(self):
        return self.name


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    products = models.ManyToManyField(MakeupProduct, blank=True, related_name='comments')

    def __str__(self):
        return self.content[:50]
