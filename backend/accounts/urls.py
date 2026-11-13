from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('account', views.account),
    path('account/<int:pk>/edit', views.edit_account),
    path('users', views.users),
    path('user/<int:pk>', views.delete_user),
    path('admin/<int:pk>', views.set_admin),
]
