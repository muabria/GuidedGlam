from django.contrib import admin

from .models import (
    Category, ColorSeason, FaceShape, MakeupProduct, PaletteColor, SkinTone, SkinType, Undertone,
)


@admin.register(Category, FaceShape, SkinTone, SkinType)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Undertone)
class UndertoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'jewelry']


class PaletteColorInline(admin.TabularInline):
    model = PaletteColor
    extra = 1


@admin.register(ColorSeason)
class ColorSeasonAdmin(admin.ModelAdmin):
    """Edit a season and its whole color guide on one page."""

    list_display = ['name']
    inlines = [PaletteColorInline]


@admin.register(MakeupProduct)
class MakeupProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'user']
    list_filter = ['categories', 'skin_types', 'skin_tones', 'face_shapes', 'undertones', 'color_seasons']
    search_fields = ['name', 'description']
    filter_horizontal = ['categories', 'face_shapes', 'skin_tones', 'skin_types', 'undertones', 'color_seasons']
