from django.urls import path

from tander import views

app_name = "reports"

urlpatterns = [
    path("", views.index, name="index"),
    # path("biiling/", views.billing, name="billing"),
]
