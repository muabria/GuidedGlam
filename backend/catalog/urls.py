from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

# trailing_slash=False keeps the same URLs as the Express app: /api/faceshape/1
router = SimpleRouter(trailing_slash=False)
router.register('faceshape', views.FaceShapeViewSet)
router.register('skintone', views.SkinToneViewSet)
router.register('skintype', views.SkinTypeViewSet)

urlpatterns = [
    path('test', views.test),
    *router.urls,
]
