from django.urls import path

from . import views

app_name = "api_v1"

urlpatterns = [
    path("filials/", views.FilialsAPIView.as_view()),
    path("contracts/", views.FilialsAPIView.as_view()),
]
