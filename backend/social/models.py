from django.conf import settings
from django.db import models


class Post(models.Model):
    """A photo post, like on Lemon8 or Instagram."""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField('catalog.MakeupProduct', blank=True, related_name='posts')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts')
    saves = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='saved_posts')

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f'{self.author.username}: {self.caption[:40]}'


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/%Y/%m/')

    class Meta:
        ordering = ['id']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at', 'id']

    def __str__(self):
        return self.content[:50]
