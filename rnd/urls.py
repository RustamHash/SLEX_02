from django.urls import path

from rnd import views

app_name = 'rnd'

urlpatterns = [
    path('', views.home, name='home')
]
