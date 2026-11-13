from django.contrib.auth.models import AbstractUser
from django.db import models


def initials(name):
    """'Tan Dark' -> 'TD'"""
    return ''.join(word[0].upper() for word in name.split())


class User(AbstractUser):
    """Django's built-in user (username, hashed password, is_staff, ...)
    plus the GuidedGlam profile.

    `is_staff` plays the role of `isAdmin` in the old Express code.
    """

    email = models.EmailField(unique=True)

    # The three sign-up questions. The sign-up route requires them; they are
    # only optional here so admin accounts can exist without them.
    skin_tone = models.ForeignKey('catalog.SkinTone', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    skin_type = models.ForeignKey('catalog.SkinType', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    face_shape = models.ForeignKey('catalog.FaceShape', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

    # Optional extras shown on the profile page.
    undertone = models.ForeignKey('catalog.Undertone', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    color_season = models.ForeignKey('catalog.ColorSeason', null=True, blank=True, on_delete=models.SET_NULL, related_name='users')

    # People this user follows. `user.followers` gives the other direction.
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')

    def _badge_parts(self):
        return [tag.name for tag in (self.skin_tone, self.skin_type, self.face_shape) if tag]

    @property
    def badge(self):
        """Shown next to the username: 'Tan, Dry, Heart'."""
        return ', '.join(self._badge_parts())

    @property
    def badge_short(self):
        """First-initial version: 'T, D, H'."""
        return ', '.join(initials(name) for name in self._badge_parts())
