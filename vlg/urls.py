from django.urls import path

from vlg import views

app_name = 'vlg'

urlpatterns = [
    path('', views.home, name='home')
]
