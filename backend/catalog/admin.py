from django.contrib import admin

from .models import Category, Comment, FaceShape, MakeupProduct, SkinTone, SkinType


@admin.register(Category, FaceShape, SkinTone, SkinType)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(MakeupProduct)
class MakeupProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'user']
    list_filter = ['categories', 'skin_types', 'skin_tones', 'face_shapes']
    search_fields = ['name', 'description']
    filter_horizontal = ['categories', 'face_shapes', 'skin_tones', 'skin_types']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['content']
    filter_horizontal = ['products']
