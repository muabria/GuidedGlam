from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

# trailing_slash=False keeps the same URLs as the Express app: /api/faceshape/1
router = SimpleRouter(trailing_slash=False)
router.register('faceshape', views.FaceShapeViewSet)
router.register('skintone', views.SkinToneViewSet)
router.register('skintype', views.SkinTypeViewSet)
router.register('undertone', views.UndertoneViewSet)
router.register('colorseason', views.ColorSeasonViewSet)
router.register('category', views.CategoryViewSet)
router.register('product', views.ProductViewSet, basename='product')

urlpatterns = [
    path('test', views.test),
    *router.urls,
]
