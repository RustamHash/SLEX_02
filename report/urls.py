from django.urls import path

from report import views

app_name = "reports"

urlpatterns = [
    path("", views.index, name="index"),
    path("biiling/", views.billing, name="billing"),
]
