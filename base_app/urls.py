from django.urls import path, include

from base_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/login/', views.NotFound.as_view(), name='not_groups'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('filial-detail/<slug:slug>/', views.FilialDetail.as_view(), name='filial-detail'),

    path('krd/', include('krd.urls', namespace='krd')),
    path('rnd/', include('rnd.urls', namespace='rnd')),
    path('vlg/', include('vlg.urls', namespace='vlg')),
]