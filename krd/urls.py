from django.urls import path

from krd import views

app_name = 'krd'

urlpatterns = [
    path('', views.home, name='home'),
    path('contracts/', views.view_contracts, name='contracts'),
    path('contracts/<slug:slug>', views.contract, name='contract'),
    # path('contracts/<slug:contr_slug>/load_file/', views.load_order, name='load_order'),
    # path('contracts/load_file/', views.load_order, name='load_order'),
]
