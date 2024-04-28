from django.urls import path

from pg_sql import views

app_name = 'pg_sql'

urlpatterns = [
    path('', views.home, name='home')
]
