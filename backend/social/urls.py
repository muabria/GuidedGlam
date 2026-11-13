from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register('post', views.PostViewSet, basename='post')

urlpatterns = [
    path('comment/<int:pk>', views.delete_comment),
    *router.urls,
]
