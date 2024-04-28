from django.urls import path, include

from base_app import views

urlpatterns = [
    path('', views.home, name='home'),
]