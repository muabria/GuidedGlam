from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ['username', 'badge', 'email', 'is_staff']
    fieldsets = DjangoUserAdmin.fieldsets + (
        ('GuidedGlam profile', {
            'fields': ['skin_tone', 'skin_type', 'face_shape', 'undertone', 'color_season', 'following'],
        }),
    )
    filter_horizontal = [*DjangoUserAdmin.filter_horizontal, 'following']
