from django.contrib import admin

from .models import Comment, Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'author', 'created_at']
    search_fields = ['caption', 'author__username']
    filter_horizontal = ['products', 'likes', 'saves']
    inlines = [PostImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'post', 'created_at']
    search_fields = ['content']
