from django.urls import path

from krd import views

app_name = 'krd'

urlpatterns = [
    path('', views.home, name='home')
]
